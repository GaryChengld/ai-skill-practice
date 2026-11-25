"""Extract answers and file-read evidence from 18 fresh Codex CLI sessions.

Pass session IDs in input order (before, after, baseline per input), then T1–T3.
Supply --sessions-dir if the rollouts live outside ~/.codex/sessions.
"""

import argparse
import ast
import csv
from hashlib import sha256
import json
from pathlib import Path
import re

TESTS = Path(__file__).resolve().parent
SKILL = TESTS.parent
BEFORE = SKILL.parent / "BEFORE/migration-safety-review/SKILL.md"
HARNESS = TESTS / "harness"
VERSIONS = ("before", "after", "baseline")
CASES = [f"{n}-{version}" for n in range(1, 6) for version in VERSIONS] + ["t1", "t2", "t3"]
MATRIX = "assets/risk-matrix.csv"
TEMPLATE = "assets/review-template.md"
POSTGRES = "references/postgres.md"
MYSQL = "references/mysql.md"
DOCS = {"before": BEFORE, "after": SKILL / "SKILL.md",
        **{name: SKILL / name for name in (POSTGRES, MYSQL, TEMPLATE, MATRIX)}}
EXPECTED_ROWS = {
    "1": {"large,rewrite,High"},
    "2": {"any,execution_blocker,High", "large,sustained_write_blocking,High"},
    "3": {"large,rewrite,High", "large,online_or_metadata_only,Low"},
    "4": {"small,online_or_metadata_only,Low"},
    "5": {"large,rewrite,High", "large,online_or_metadata_only,Low"},
}
CALLS = {"function_call", "custom_tool_call"}
RESULTS = {"function_call_output", "custom_tool_call_output"}
PROCESS_ID = re.compile(r"\bsession_id[\"']?\s*:\s*(\d+)")


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
        for key in ("text", "content", "output", "result", "value"):
            if key in output:
                yield from tool_text(output[key])


def only(events, predicate, description):
    matches = [(number, record) for number, record in events if predicate(record)]
    if len(matches) != 1:
        raise ValueError(f"expected one {description}, found {len(matches)}")
    return matches[0]


def table_cells(line):
    if not line.startswith("|") or not line.endswith("|"):
        return []
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", line[1:-1])]


def matches_list(lines, marker):
    indent = 0
    for line in lines:
        if not line:
            continue
        item = re.match(marker, line)
        if item:
            indent = item.end()
        elif not indent or not line.startswith(" " * indent):
            return False
    return indent > 0


def matches_template(answer, fixture, template):
    expected = template.replace("<file name>", fixture).splitlines()
    headings = [line for line in expected if line.startswith("#")]
    actual = [line.rstrip() for line in answer.strip("\r\n").splitlines()]
    indexes = [index for index, line in enumerate(actual) if line.startswith("#")]
    if not indexes or indexes[0] != 0 or [actual[index] for index in indexes] != headings:
        return False
    title, findings, rollout, questions = indexes
    metadata = [line for line in actual[title + 1:findings] if line]
    if len(metadata) != 2 or not re.fullmatch(r"\*\*Database:\*\* (PostgreSQL|MySQL)\b.*", metadata[0]):
        return False
    if not re.fullmatch(r"\*\*Overall risk:\*\* (Low|Medium|High)", metadata[1]):
        return False
    columns = table_cells(next(line for line in expected if line.startswith("| #")))
    table = [table_cells(line) for line in "\n".join(actual[findings + 1:rollout]).strip("\n").splitlines()]
    return (len(table) >= 3 and table[0] == columns
            and all(len(row) == len(columns) and all(row) for row in table)
            and all(re.fullmatch(r":?-{3,}:?", cell) for cell in table[1])
            and matches_list(actual[rollout + 1:questions], r"\d+\. +(?=\S)")
            and matches_list(actual[questions + 1:], r"- +(?=\S)"))


def collect(case, source, registry, docs):
    raw = source.read_bytes()
    events = [(n, json.loads(line)) for n, line in enumerate(raw.splitlines(), 1)]
    context = only(events, lambda row: row["type"] == "turn_context", "turn context")[1]["payload"]
    prompt_line, prompt_row = only(events, lambda row: row["type"] == "response_item"
                                  and row["payload"].get("role") == "user"
                                  and not row["payload"]["content"][0]["text"].startswith("<environment_context>"),
                                  "user prompt")
    final_line, final_row = only(events, lambda row: row["type"] == "event_msg"
                                  and row["payload"]["type"] == "task_complete", "completed turn")
    answer = final_row["payload"]["last_agent_message"]
    if not answer:
        raise ValueError(f"{case}: no final answer")

    trigger = case.startswith("t")
    version = "after" if trigger else case.split("-")[1]
    fixture = None if trigger else f"input-{case[0]}.sql"
    expected_prompt = ((TESTS / f"trigger-{case}.md").read_text(encoding="utf-8").rstrip() if trigger else
                       f"Can you check this migration before I merge it? The file is {fixture}.")
    prompt = prompt_row["payload"]["content"][0]["text"]
    if Path(context["cwd"]) != Path(registry[version]["cwd"]) or prompt != expected_prompt:
        raise ValueError(f"{case}: incorrect working directory or prompt")
    if trigger and re.search(r"migration-safety-review|SKILL\.md|\bskills?\b|\btests?\b", prompt, re.I):
        raise ValueError(f"{case}: trigger prompt names the skill or test")

    excerpt = [json_bytes({"line": prompt_line, "record": prompt_row})]
    commands = {}
    running_commands = {}
    reads = []
    matrix_header, *matrix_rows = docs[MATRIX].splitlines()
    targets = {name: docs[name] for name in docs if name != MATRIX}
    if fixture:
        targets[fixture] = (TESTS / fixture).read_text(encoding="utf-8").strip()
    for number, row in events:
        if row["type"] != "response_item":
            continue
        payload = row["payload"]
        kind = payload["type"]
        if kind in CALLS:
            command = payload.get("arguments", payload.get("input", ""))
            continued = [running_commands.get(identifier, "") for identifier in PROCESS_ID.findall(command)]
            commands[payload["call_id"]] = "\n".join([command.casefold(), *continued])
            excerpt.append(json_bytes({"line": number, "record": row}))
            continue
        if kind not in RESULTS or payload["call_id"] not in commands:
            continue
        command = commands[payload["call_id"]]
        output = payload.get("output")
        started = PROCESS_ID.findall(str(output))
        for identifier in started:
            running_commands[identifier] = command
        fragments = list(tool_text(output))
        found = {}
        for name, contents in targets.items():
            basename = DOCS[name].name if name in DOCS else name
            if basename.lower() in command and any(contents in part for part in fragments):
                found[name] = {}
        if fixture and ".sql" in command:
            for part in fragments:
                unnumbered = re.sub(r"(?m)^\s*\d+: ", "", part)
                if fixture in part and targets[fixture] in unnumbered:
                    found[fixture] = {}
        if Path(MATRIX).name in command:
            lines = {",".join(fields) for part in fragments for fields in csv.reader(part.splitlines())}
            matched = sorted(lines.intersection(matrix_rows))
            if matched or matrix_header in lines:
                found[MATRIX] = {"header": matrix_header in lines, "rows": matched}
        if found or started or any("Failed to create unified exec process" in part for part in fragments):
            excerpt.append(json_bytes({"line": number, "record": row}))
        reads.extend({"file": name, "line": number, "call_id": payload["call_id"], **details}
                     for name, details in found.items())

    skills = {read["file"] for read in reads} & set(VERSIONS)
    wanted = set() if case in ("t2", "t3") or version == "baseline" else {version}
    resources = {read["file"] for read in reads} & {POSTGRES, MYSQL, TEMPLATE, MATRIX}
    selected = set() if version != "after" or trigger else {MYSQL if case[0] == "3" else POSTGRES, TEMPLATE, MATRIX}
    lookups = [read for read in reads if read["file"] == MATRIX]
    lookup_rows = {line for read in lookups for line in read["rows"]}
    flags = {
        "activation": skills == wanted,
        "fixture": trigger or any(read["file"] == fixture for read in reads),
        "routing": (not resources if not wanted else True) if trigger else resources == selected,
        "matrix": not selected or (EXPECTED_ROWS[case[0]] <= lookup_rows and any(read["header"] for read in lookups)),
        "template": not selected or matches_template(answer, fixture, docs[TEMPLATE]),
    }
    if not wanted:
        flags["activation"] &= not any("migration-safety-review" in command for command in commands.values())
    excerpt.append(json_bytes({"line": final_line, "record": final_row}))
    evidence = b"".join(excerpt)
    (HARNESS / f"{case}.jsonl").write_bytes(evidence)
    if fixture:
        (TESTS / f"output-{case}.md").write_bytes(answer.encode())
    return {"source_log": source.name, "source_sha256": digest(raw), "excerpt_sha256": digest(evidence),
            "answer_sha256": digest(answer.encode()), "model": context["model"], "tool_calls": len(commands),
            "reads": reads, "activation": sorted(skills), "resources": sorted(resources),
            "matrix_rows": sorted(lookup_rows), "checks": flags, "pass": all(flags.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sessions", nargs=len(CASES), metavar="SESSION_ID")
    parser.add_argument("--sessions-dir", type=Path, default=Path.home() / ".codex" / "sessions")
    args = parser.parse_args()
    if len(set(args.sessions)) != len(CASES):
        parser.error("every case must use a distinct session ID")
    registry = json.loads((HARNESS / "registry.json").read_bytes())
    for version in VERSIONS:
        enabled = registry[version]["enabled"]
        if version == "baseline":
            if enabled:
                raise ValueError("the baseline must have no enabled skills")
        elif (len(enabled) != 1 or enabled[0]["name"] != "migration-safety-review" or not enabled[0]["enabled"]
              or enabled[0]["sha256"] != digest(DOCS[version].read_bytes())):
            raise ValueError(f"{version}: expected exactly the matching on-disk skill in the registry")
    docs = {name: path.read_text(encoding="utf-8").strip() for name, path in DOCS.items()}
    runs = {}
    for case, session in zip(CASES, args.sessions):
        sources = list(args.sessions_dir.rglob(f"*{session}.jsonl"))
        if len(sources) != 1:
            raise ValueError(f"{case}: expected one log for {session}, found {len(sources)}")
        run = collect(case, sources[0], registry, docs)
        runs[case] = {"session_id": session, **run}
        print(f"{case}: " + ("PASS" if run["pass"] else "FAIL " + ", ".join(
            name for name, passed in run["checks"].items() if not passed)))
    if len({run["model"] for run in runs.values()}) != 1:
        raise ValueError("all cases must use the same model")
    manifest = {"document_sha256": {name: digest(path.read_bytes()) for name, path in DOCS.items()}, "runs": runs}
    (HARNESS / "manifest.json").write_bytes(json_bytes(manifest, indent=2))
    return 0 if all(run["pass"] for run in runs.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
