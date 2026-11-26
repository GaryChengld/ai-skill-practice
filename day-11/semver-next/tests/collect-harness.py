"""Collect eight fresh Codex CLI runs from their --json streams and rollouts.

Pass a directory with CLI logs named 1-skill.jsonl, 1-baseline.jsonl, and so on.
Use --sessions-dir if the rollout logs live outside ~/.codex/sessions.
"""

import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys


TESTS = Path(__file__).resolve().parent
SKILL = TESTS.parent / "SKILL.md"
SCRIPT = TESTS.parent / "scripts/next_version.py"
HARNESS = TESTS / "harness"
PYTHON = re.compile(r"\b(?:python(?:3(?:\.\d+)?)?|py)(?:\.exe)?[\"']?\s", re.I)
FILE_READER = re.compile(r"\b(?:get-content|cat|type|rg|select-string|sed|head|tail|open|read_text|read_bytes|readfile)\b[^;|\n]*\bnext_version\.py\b", re.I)
EXIT_STATUS = re.compile(r"^Exit status: (\d+)\s*$", re.M)
SOURCE_MARKERS = ("class PrereleaseVersion(ValueError):", "def parse_version(text):",
                  "def commit_messages(text):", "def next_release(current, prefix, parts, commits):")
CALLS = {"function_call", "custom_tool_call"}
RESULTS = {"function_call_output", "custom_tool_call_output"}


def digest(data):
    return sha256(data).hexdigest()


def json_bytes(value, *, indent=None):
    return (json.dumps(value, ensure_ascii=False, indent=indent) + "\n").encode()


def records(data):
    return [(line_number, json.loads(line)) for line_number, line in enumerate(data.splitlines(), 1)]


def only(events, predicate, description):
    found = [(line, record) for line, record in events if predicate(record)]
    if len(found) != 1:
        raise ValueError(f"expected one {description}, found {len(found)}")
    return found[0]


def tool_text(value):
    if isinstance(value, str):
        if value.lstrip().startswith(("[", "{")):
            for decode in (json.loads, ast.literal_eval):
                try:
                    decoded = decode(value)
                except (ValueError, SyntaxError):
                    continue
                yield from tool_text(decoded)
                return
        yield value.replace("\r\n", "\n")
    elif isinstance(value, list):
        for item in value:
            yield from tool_text(item)
    elif isinstance(value, dict):
        if not value.get("isError") and value.get("exit_code") in (None, 0, 3):
            for key in ("text", "content", "output", "result", "value"):
                if key in value:
                    yield from tool_text(value[key])


def ran_calculator(item, fixture, version, reference):
    command = item["command"].replace("\\", "/").casefold()
    if (not PYTHON.search(command) or "scripts/next_version.py" not in re.sub(r"/+", "/", command)
            or "--current" not in command or version.casefold() not in command
            or "--commits" not in command or "--help" in command):
        return None
    if fixture not in command and not re.search(r"--commits\s+[\"']?-(?=[\"'\s]|$)", command):
        return None
    result = item.get("aggregated_output", "")
    status = item.get("exit_code")
    if "lastexitcode" in command:
        reported = EXIT_STATUS.findall(result)
        if len(reported) == 1:
            status = int(reported[0])
            result = EXIT_STATUS.sub("", result).strip()
    if status != reference.returncode:
        return None
    if reference.returncode == 3:
        return status if reference.stderr.strip().decode() in result else None
    if reference.returncode == 0:
        try:
            return status if json.loads(result) == json.loads(reference.stdout) else None
        except ValueError:
            return None
    return None


def collect(case, source, sessions_dir, registry, versions, seen):
    raw_cli = source.read_bytes()
    cli = records(raw_cli)
    session = only(cli, lambda row: row["type"] == "thread.started", "CLI session start")[1]["thread_id"]
    if session in seen:
        raise ValueError(f"{case}: duplicate session {session}")
    seen.add(session)
    only(cli, lambda row: row["type"] == "turn.completed", "CLI completion")
    sources = list(sessions_dir.rglob(f"*{session}.jsonl"))
    if len(sources) != 1:
        raise ValueError(f"{case}: expected one rollout for {session}, found {len(sources)}")
    rollout = sources[0]
    raw_rollout = rollout.read_bytes()
    events = records(raw_rollout)
    context = only(events, lambda row: row["type"] == "turn_context", "turn context")[1]["payload"]
    prompt_line, prompt = only(events, lambda row: row["type"] == "response_item"
                               and row["payload"].get("role") == "user"
                               and not row["payload"]["content"][0]["text"].startswith("<environment_context>"),
                               "user prompt")
    final_line, final = only(events, lambda row: row["type"] == "event_msg"
                             and row["payload"]["type"] == "task_complete", "completed turn")
    answer = final["payload"]["last_agent_message"].encode()
    if not answer:
        raise ValueError(f"{case}: missing final answer")
    number, variant = case.split("-")
    fixture = f"input-{number}.txt"
    version = versions[fixture]
    expected = f"What should the next release tag be? Commits since the last tag are in {fixture}, and the last tag is {version}."
    if prompt["payload"]["content"][0]["text"] != expected or Path(context["cwd"]) != Path(registry[variant]["cwd"]):
        raise ValueError(f"{case}: unexpected working directory or prompt")

    def evidence(origin, line, record):
        return json_bytes({"origin": origin, "line": line, "record": record})

    excerpt = [evidence("rollout", prompt_line, prompt)]
    commands = [(line, row) for line, row in cli if row["type"] == "item.completed"
                and row.get("item", {}).get("type") == "command_execution"]
    reference = subprocess.run([sys.executable, str(SCRIPT), "--current", version, "--commits", str(TESTS / fixture)],
                               capture_output=True, check=False)
    runs = []
    inspected = []
    skill_text = SKILL.read_text(encoding="utf-8").strip()
    reads = []
    for line, row in commands:
        item = row["item"]
        excerpt.append(evidence("cli", line, row))
        outcome = ran_calculator(item, fixture, version, reference)
        if outcome is not None:
            runs.append({"line": line, "command_id": item["id"], "exit_code": outcome})
        if FILE_READER.search(item["command"]) or any(mark in item.get("aggregated_output", "") for mark in SOURCE_MARKERS):
            inspected.append({"origin": "cli", "line": line})

    touched_skill = False
    for line, row in events:
        if row["type"] != "response_item":
            continue
        payload = row["payload"]
        kind = payload["type"]
        if kind in CALLS:
            call = payload.get("arguments", payload.get("input", ""))
            touched_skill |= bool(re.search(r"semver-next|next_version\.py", call, re.I))
            if FILE_READER.search(call):
                inspected.append({"origin": "rollout", "line": line})
            excerpt.append(evidence("rollout", line, row))
        if kind in RESULTS:
            fragments = list(tool_text(payload.get("output")))
            if any(skill_text in part for part in fragments):
                reads.append(line)
                excerpt.append(evidence("rollout", line, row))
            if any(marker in part for part in fragments for marker in SOURCE_MARKERS):
                inspected.append({"origin": "rollout", "line": line})
                excerpt.append(evidence("rollout", line, row))

    checks = {"activation": bool(reads) if variant == "skill" else not reads and not touched_skill,
              "execution": bool(runs) if variant == "skill" else not runs,
              "no_source_read": not inspected}
    excerpt.append(evidence("rollout", final_line, final))
    contents = b"".join(excerpt)
    (HARNESS / f"{case}.jsonl").write_bytes(contents)
    (TESTS / f"output-{case}.md").write_bytes(answer)
    return {"session_id": session, "model": context["model"], "rollout_log": rollout.name,
            "source_sha256": {"cli": digest(raw_cli), "rollout": digest(raw_rollout)},
            "excerpt_sha256": digest(contents), "answer_sha256": digest(answer),
            "skill_read_lines": reads, "calculator_runs": runs, "source_reads": inspected,
            "checks": checks, "pass": all(checks.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cli_dir", type=Path, help="directory with the eight Codex CLI --json logs")
    parser.add_argument("--sessions-dir", type=Path, default=Path.home() / ".codex/sessions")
    args = parser.parse_args()
    registry = json.loads((HARNESS / "registry.json").read_bytes())
    enabled = registry["skill"]["enabled"]
    if (registry["baseline"]["enabled"] or len(enabled) != 1 or not enabled[0]["enabled"]
            or enabled[0]["name"] != "semver-next" or enabled[0]["sha256"] != digest(SKILL.read_bytes())
            or enabled[0]["script_sha256"] != digest(SCRIPT.read_bytes())):
        raise ValueError("expected a single matching skill and a baseline with zero enabled skills")
    versions = json.loads((TESTS / "versions.json").read_bytes())
    seen = set()
    runs = {}
    for number in range(1, 5):
        for variant in ("skill", "baseline"):
            case = f"{number}-{variant}"
            run = collect(case, args.cli_dir / f"{case}.jsonl", args.sessions_dir, registry, versions, seen)
            runs[case] = run
            failed = [name for name, passed in run["checks"].items() if not passed]
            print(f"{case}: " + ("PASS" if not failed else "FAIL " + ", ".join(failed)))
    if len({run["model"] for run in runs.values()}) != 1:
        raise ValueError("all sessions must use the same model")
    (HARNESS / "manifest.json").write_bytes(json_bytes({"runs": runs}, indent=2))
    return 0 if all(run["pass"] for run in runs.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
