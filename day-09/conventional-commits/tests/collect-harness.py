"""Extract and verify evidence from 15 fresh Codex CLI sessions.

Pass IDs for 1-original 1-slim through 5-original 5-slim, then 5-baseline and t1–t4.
The default sessions directory is ~/.codex/sessions. The registries must come
from `skills/list` under the session-local configurations used for the runs.
"""

import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path
import re

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parents[2]
HARNESS = TESTS / "harness"
SKILLS = {"original": ROOT / "day-01/conventional-commits/SKILL.md",
          "slim": TESTS.parent / "SKILL.md"}
CASES = [f"{n}-{v}" for n in range(1, 6) for v in SKILLS] + ["5-baseline", "t1", "t2", "t3", "t4"]
CALLS = {"function_call", "custom_tool_call"}
RESULTS = {"function_call_output", "custom_tool_call_output"}


def digest(data):
    return sha256(data).hexdigest()


def json_bytes(value, *, indent=None):
    return (json.dumps(value, ensure_ascii=False, indent=indent) + "\n").encode()


def tool_text(output):
    if isinstance(output, str):
        if output.lstrip().startswith(("[", "{")):
            for decode in (json.loads, ast.literal_eval):
                try:
                    value = decode(output)
                except (ValueError, SyntaxError):
                    continue
                yield from tool_text(value)
                return
        yield output.replace("\r\n", "\n")
    elif isinstance(output, list):
        for item in output:
            yield from tool_text(item)
    elif isinstance(output, dict):
        if output.get("isError") or output.get("exit_code") not in (None, 0):
            return
        for key in ("text", "content", "output", "result"):
            if key in output:
                yield from tool_text(output[key])


def path_text(text):
    return re.sub(r"[\\/]+", "/", text).casefold()


def fixture_for(case):
    return f"trigger-{case}.md" if case.startswith("t") else f"input-{case[0]}.md"


def only(rows, predicate, description):
    matched = [(number, row) for number, row in rows if predicate(row)]
    if len(matched) != 1:
        raise ValueError(f"expected exactly one {description}, found {len(matched)}")
    return matched[0]


def collect(case, source, registry, docs):
    raw = source.read_bytes()
    rows = [(n, json.loads(line)) for n, line in enumerate(raw.splitlines(), 1)]
    context = only(rows, lambda row: row["type"] == "turn_context", "turn context")[1]["payload"]
    cwd = Path(context["cwd"])
    prompt_line, prompt_row = only(
        rows,
        lambda row: row["type"] == "response_item" and row["payload"].get("role") == "user"
        and not row["payload"]["content"][0]["text"].startswith("<environment_context>"),
        "user prompt",
    )
    prompt = prompt_row["payload"]["content"][0]["text"]
    final_line, final_row = only(
        rows, lambda row: row["type"] == "event_msg" and row["payload"]["type"] == "task_complete",
        "completed turn",
    )
    final = final_row["payload"]["last_agent_message"]
    if not final:
        raise ValueError(f"{case}: missing final answer")

    is_trigger = case.startswith("t")
    baseline = case == "5-baseline"
    version = "slim" if is_trigger else case.split("-")[1]
    expected_path = Path(registry["trigger"]["enabled"][0]["path"]) if is_trigger else SKILLS.get(version)
    if is_trigger:
        expected_cwd = Path(registry["trigger"]["cwd"])
    elif case.startswith("5-"):
        expected_cwd = Path(registry["raw_diff"]["cwd"])
    elif case.startswith("4-"):
        expected_cwd = Path(registry["empty_diff_cwd"])
    else:
        expected_cwd = ROOT
    fixture = (TESTS / fixture_for(case)).read_text(encoding="utf-8").rstrip()
    expected_prompt = fixture if is_trigger or baseline else (
        f"Use the instructions in {expected_path.as_posix()} for this request.\n\n{fixture}"
    )
    if cwd != expected_cwd or prompt != expected_prompt:
        raise ValueError(f"{case}: unexpected working directory or user prompt")
    if is_trigger and re.search(r"conventional[- ]commits|\bskills?\b|SKILL\.md|\btests?\b", prompt, re.I):
        raise ValueError(f"{case}: trigger prompt names the skill or the test")

    excerpt = [json_bytes({"line": prompt_line, "record": prompt_row})]
    calls = {}
    reads = []
    for number, row in rows:
        if row["type"] != "response_item":
            continue
        payload = row["payload"]
        kind = payload["type"]
        if kind in CALLS:
            command = payload.get("arguments", payload.get("input", ""))
            calls[payload["call_id"]] = path_text(command)
            excerpt.append(json_bytes({"line": number, "record": row}))
        if kind not in RESULTS or payload["call_id"] not in calls:
            continue
        for read_version, contents in docs.items():
            if any(contents in part for part in tool_text(payload.get("output"))):
                reads.append({"version": read_version, "line": number, "call_id": payload["call_id"]})
                excerpt.append(json_bytes({"line": number, "record": row}))
    excerpt.append(json_bytes({"line": final_line, "record": final_row}))
    evidence = b"".join(excerpt)
    skill_attempts = sum("/conventional-commits/skill.md" in command for command in calls.values())
    activated = bool(reads)
    should_activate = case not in ("t2", "t3", "5-baseline")
    correct_file = all(read["version"] == version and path_text(str(expected_path)) in calls[read["call_id"]]
                       for read in reads)
    passed = activated == should_activate and correct_file and (should_activate or skill_attempts == 0)

    (HARNESS / f"{case}.jsonl").write_bytes(evidence)
    answer = final.encode()
    if not is_trigger:
        (TESTS / f"output-{case}.md").write_bytes(answer)
    return {"source_log": source.name, "source_sha256": digest(raw), "excerpt_sha256": digest(evidence),
            "answer_sha256": digest(answer), "model": context["model"], "tool_calls": len(calls),
            "skill_read_attempts": skill_attempts, "verified_reads": reads,
            "activated": activated, "expected_activation": should_activate, "pass": passed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sessions", nargs=len(CASES), metavar="SESSION_ID")
    parser.add_argument("--sessions-dir", type=Path, default=Path.home() / ".codex" / "sessions")
    args = parser.parse_args()
    if len(set(args.sessions)) != len(CASES):
        parser.error("every case must have a distinct session ID")

    registry = json.loads((HARNESS / "registry.json").read_bytes())
    enabled = registry["trigger"]["enabled"]
    if (len(enabled) != 1 or enabled[0]["name"] != "conventional-commits" or not enabled[0]["enabled"]
            or enabled[0]["sha256"] != digest(SKILLS["slim"].read_bytes())):
        raise ValueError("trigger registry must have a single enabled copy matching the slim skill")
    if registry["raw_diff"]["enabled"]:
        raise ValueError("raw-diff registry must have no enabled skills")
    preflight = json.loads((HARNESS / "preflight.json").read_bytes())
    inputs = {fixture_for(case) for case in CASES} | {"CHECKLIST.md"}
    if preflight != {name: digest((TESTS / name).read_bytes()) for name in inputs}:
        raise ValueError("checklist or fixtures changed after preflight")
    docs = {version: file.read_text(encoding="utf-8").strip() for version, file in SKILLS.items()}
    runs = {}
    for case, session in zip(CASES, args.sessions):
        sources = list(args.sessions_dir.rglob(f"*{session}.jsonl"))
        if len(sources) != 1:
            raise ValueError(f"{case}: expected one source log for {session}, found {len(sources)}")
        run = collect(case, sources[0], registry, docs)
        runs[case] = {"session_id": session, **run}
        state = "activated" if run["activated"] else "inactive"
        print(f"{case}: {state}, {'PASS' if run['pass'] else 'FAIL'}")
    if len({run["model"] for run in runs.values()}) != 1:
        raise ValueError("all runs must use the same model")
    manifest = {"skill_text_sha256": {version: digest(text.encode()) for version, text in docs.items()},
                "runs": runs}
    (HARNESS / "manifest.json").write_bytes(json_bytes(manifest, indent=2))
    return 0 if all(run["pass"] for run in runs.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
