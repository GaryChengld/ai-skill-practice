"""Extract Codex CLI sessions from their JSON streams and rollouts.

Pass a directory with one CASE.jsonl per entry in CASES.
Keep the scratch workspaces for fixture integrity checks.
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
LINTER = TESTS.parent / "scripts/lint_frontmatter.py"
HARNESS = TESTS / "harness"
CASES = {"1-skill": "fixtures/19-multiple-errors", "1-baseline": "fixtures/19-multiple-errors",
         "2-skill": "fixtures/11-yaml-colon", "3-skill": "fixtures/02-full-fields",
         "4-skill": "fixtures/13-metadata-value", "4-baseline": "fixtures/13-metadata-value",
         "5-skill": "fixtures/17-name-boolean", "5-baseline": "fixtures/17-name-boolean",
         "6-skill": "fixtures/23-metadata-key", "6-baseline": "fixtures/23-metadata-key",
         "7-skill": "behavior-fixtures/07-encoding", "7-baseline": "behavior-fixtures/07-encoding"}
RUNNER = re.compile(r"\b(?:uv(?:\.exe)?[\"']?\s+run|(?:python(?:3(?:\.\d+)?)?|py)(?:\.exe)?[\"']?)\s", re.I)
FILE_READER = re.compile(r"\b(?:get-content|cat|type|rg|sed|head|tail|open|read_text|read_bytes|readfile)\b"
                         r"[^;|\n]*\blint_frontmatter\.py\b", re.I)
EXIT_STATUS = re.compile(r"^exit[ _](?:status|code)[:=][ \t]*(\d+)[ \t\r]*$", re.I | re.M)
SOURCE_MARKERS = ("class ParseFailure(Exception):", "def read_frontmatter(path, yaml):",
                  "def check_metadata(node, yaml, errors):", "def lint(path, yaml):")
CALLS = {"function_call", "custom_tool_call"}
RESULTS = {"function_call_output", "custom_tool_call_output"}


def digest(data):
    return sha256(data).hexdigest()


def json_bytes(value, *, indent=None):
    return (json.dumps(value, ensure_ascii=False, indent=indent) + "\n").encode()


def records(data):
    return [(line, json.loads(value)) for line, value in enumerate(data.splitlines(), 1)]


def only(events, predicate, description):
    found = [(line, row) for line, row in events if predicate(row)]
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
        if not value.get("isError") and value.get("exit_code") in (None, 0, 1, 3):
            for key in ("text", "content", "output", "result", "value"):
                if key in value:
                    yield from tool_text(value[key])


def ran_linter(item, target, expected_status, expected_payload):
    command = re.sub(r"[\\/]+", "/", item["command"].casefold())
    if (not RUNNER.search(command) or "scripts/lint_frontmatter.py" not in command
            or target.parent.name.casefold() not in command or "--help" in command):
        return None
    output = item.get("aggregated_output", "")
    reported = EXIT_STATUS.findall(output) if "lastexitcode" in command else []
    status = int(reported[0]) if len(reported) == 1 else item.get("exit_code")
    if status != expected_status:
        return None
    json_lines = [line for line in output.splitlines() if line.lstrip().startswith('{"results":')]
    if len(json_lines) != 1:
        return None
    try:
        data = json.loads(json_lines[0])
    except ValueError:
        return None
    return status if data == expected_payload else None


def collect(case, source, registry, sessions_dir):
    raw_cli = source.read_bytes()
    cli = records(raw_cli)
    session = only(cli, lambda row: row["type"] == "thread.started", "session start")[1]["thread_id"]
    only(cli, lambda row: row["type"] == "turn.completed", "CLI completion")
    rollouts = list(sessions_dir.rglob(f"*{session}.jsonl"))
    if len(rollouts) != 1:
        raise ValueError(f"{case}: expected one rollout for {session}")
    rollout = rollouts[0]
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
    variant = case.split("-")[1]
    cwd = Path(registry[variant]["cwd"])
    original = next((TESTS / CASES[case]).glob("*/SKILL.md"))
    target = cwd / "fixtures" / original.parent.name / "SKILL.md"
    requested = f"Can you check whether this skill's frontmatter is set up correctly? It's in fixtures/{original.parent.name}. Please report what you find."
    if Path(context["cwd"]) != cwd or prompt["payload"]["content"][0]["text"] != requested:
        raise ValueError(f"{case}: unexpected working directory or prompt")
    reference = subprocess.run([sys.executable, str(LINTER), str(original)], capture_output=True, check=False)
    expected = json.loads(reference.stdout)
    expected["results"][0]["path"] = str(target)

    def evidence(origin, line, record):
        return json_bytes({"origin": origin, "line": line, "record": record})

    excerpt = [evidence("rollout", prompt_line, prompt)]
    script_runs = []
    source_reads = []
    for line, row in cli:
        item = row.get("item", {})
        if row["type"] != "item.completed" or item.get("type") != "command_execution":
            continue
        excerpt.append(evidence("cli", line, row))
        status = ran_linter(item, target, reference.returncode, expected)
        if status is not None:
            script_runs.append({"line": line, "command_id": item["id"], "exit_code": status})
        if FILE_READER.search(item["command"]) or any(mark in item.get("aggregated_output", "") for mark in SOURCE_MARKERS):
            source_reads.append({"origin": "cli", "line": line})

    skill_text = SKILL.read_text(encoding="utf-8").strip()
    skill_reads = []
    touched_skill = False
    for line, row in events:
        if row["type"] != "response_item":
            continue
        payload = row["payload"]
        kind = payload["type"]
        if kind in CALLS:
            call = payload.get("arguments", payload.get("input", ""))
            touched_skill |= bool(re.search(r"skill-frontmatter-lint|lint_frontmatter\.py", call, re.I))
            if FILE_READER.search(call):
                source_reads.append({"origin": "rollout", "line": line})
            excerpt.append(evidence("rollout", line, row))
        if kind in RESULTS:
            fragments = list(tool_text(payload.get("output")))
            if any(skill_text in part for part in fragments):
                skill_reads.append(line)
                excerpt.append(evidence("rollout", line, row))
            if any(mark in part for part in fragments for mark in SOURCE_MARKERS):
                source_reads.append({"origin": "rollout", "line": line})
                excerpt.append(evidence("rollout", line, row))

    enabled = variant == "skill"
    checks = {"activation_as_expected": bool(skill_reads) if enabled else not skill_reads and not touched_skill,
              "execution_as_expected": bool(script_runs) == enabled, "no_source_read": not source_reads,
              "fixture_unchanged": target.is_file() and target.read_bytes() == original.read_bytes()}
    excerpt.append(evidence("rollout", final_line, final))
    saved = b"".join(excerpt)
    (HARNESS / f"{case}.jsonl").write_bytes(saved)
    (TESTS / f"output-{case}.md").write_bytes(answer)
    return {"session_id": session, "model": context["model"], "rollout_log": rollout.name,
            "source_sha256": {"cli": digest(raw_cli), "rollout": digest(raw_rollout)},
            "excerpt_sha256": digest(saved), "answer_sha256": digest(answer), "fixture_sha256": digest(original.read_bytes()),
            "skill_read_lines": skill_reads, "linter_runs": script_runs, "source_reads": source_reads,
            "checks": checks, "pass": all(checks.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cli_dir", type=Path, help="directory containing the CLI JSON logs")
    parser.add_argument("--sessions-dir", type=Path, default=Path.home() / ".codex/sessions")
    args = parser.parse_args()
    registry = json.loads((HARNESS / "registry.json").read_bytes())
    enabled = registry["skill"]["enabled"]
    if (registry["baseline"]["enabled"] or len(enabled) != 1 or not enabled[0]["enabled"]
            or enabled[0]["name"] != "skill-frontmatter-lint" or enabled[0]["sha256"] != digest(SKILL.read_bytes())
            or enabled[0]["script_sha256"] != digest(LINTER.read_bytes())):
        raise ValueError("expected the matching skill and a baseline with zero enabled skills")
    runs = {}
    for case in CASES:
        run = collect(case, args.cli_dir / f"{case}.jsonl", registry, args.sessions_dir)
        runs[case] = run
        failures = [name for name, passed in run["checks"].items() if not passed]
        print(f"{case}: " + ("PASS" if not failures else "FAIL " + ", ".join(failures)))
    if len({run["session_id"] for run in runs.values()}) != len(CASES) or len({run["model"] for run in runs.values()}) != 1:
        raise ValueError("use distinct sessions with the same model for every case")
    (HARNESS / "manifest.json").write_bytes(json_bytes({"runs": runs}, indent=2))
    return 0 if all(run["pass"] for run in runs.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
