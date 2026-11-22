"""Save final messages and verify asset reads from five local Codex session logs.

Usage: python tests/collect-harness.py SESSION_A SESSION_B SESSION_C SESSION_D SESSION_E
Pass --sessions-dir if the Codex session logs are outside ~/.codex/sessions.
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re

TESTS = Path(__file__).resolve().parent
SKILL = TESTS.parent
TEMPLATE = "assets/handoff-template.md"
MATRIX = "assets/severity-matrix.csv"
SCHEMA = "assets/handoff.schema.json"
EXPECTED = {"a": {TEMPLATE}, "b": {TEMPLATE, MATRIX}, "c": {SCHEMA}, "d": {TEMPLATE}, "e": {TEMPLATE}}
CALL_TYPES = {"function_call", "custom_tool_call"}
RESULT_TYPES = {"function_call_output", "custom_tool_call_output"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def output_text(value):
    """Unwrap tool result text and discard nonzero exit results."""
    if isinstance(value, str):
        value = value.replace("\r\n", "\n")
        if value.lstrip().startswith(("{", "[")):
            try:
                decoded = json.loads(value)
            except ValueError:
                pass
            else:
                if isinstance(decoded, dict) and "$schema" in decoded:
                    yield value
                    return
                yield from output_text(decoded)
                return
        status = re.search(r"(?m)^Process exited with code (\d+)", value)
        if status and int(status[1]) != 0:
            return
        for label in ("\nFinal output:\n", "\nOutput:\n"):
            if label in value:
                value = value.split(label, 1)[1]
                break
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from output_text(item)
    elif isinstance(value, dict):
        if value.get("exit_code") not in (None, 0) or value.get("isError"):
            return
        for key in ("output", "content", "text", "result", "value"):
            if key in value:
                yield from output_text(value[key])


def original_prompt(events):
    for _, event in events:
        payload = event.get("payload", {})
        if event.get("type") == "event_msg" and payload.get("type") == "user_message":
            return payload["message"]
        if event.get("type") == "response_item" and payload.get("type") in RESULT_TYPES:
            for fragment in output_text(payload.get("output")):
                match = re.search(r"<codex_delegation>.*?<input>(.*?)</input>", fragment, re.S)
                if match:
                    return match[1]
    raise ValueError("no original user prompt in session log")


def collect(case, source, destination, documents, matrix_rows):
    raw = source.read_bytes()
    events = [(line, json.loads(line)) for line in raw.splitlines(keepends=True)]
    prompt = original_prompt(events)
    final = [event["payload"]["last_agent_message"] for _, event in events
             if event.get("type") == "event_msg"
             and event["payload"].get("type") == "task_complete"
             and isinstance(event["payload"].get("last_agent_message"), str)]
    if not final:
        raise ValueError(f"{case}: no completed final message in {source.name}")

    tool_events = [(line, event) for line, event in events
                   if event.get("type") == "response_item"
                   and event["payload"].get("type") in CALL_TYPES | RESULT_TYPES]
    discovery_ids = {event["payload"]["call_id"] for _, event in tool_events
                     if event["payload"]["type"] in CALL_TYPES
                     and "ALL_TOOLS.filter" in event["payload"].get("input", "")
                     and "tools." not in event["payload"]["input"]}
    tool_events = [(line, event) for line, event in tool_events
                   if event["payload"]["type"] not in RESULT_TYPES
                   or event["payload"].get("call_id") not in discovery_ids]
    excerpt = b"".join(line for line, _ in tool_events)
    (destination / f"{case}-tools.jsonl").write_bytes(excerpt)
    suffix = "json" if case == "c" else "md"
    output = final[-1].encode("utf-8")
    (TESTS / f"output-{case}.{suffix}").write_bytes(output)

    reads = []
    for index, (_, event) in enumerate(tool_events, start=1):
        result = event["payload"]
        if result["type"] not in RESULT_TYPES:
            continue
        matched = {}
        for text in output_text(result.get("output")):
            for file, contents in documents.items():
                if contents in text:
                    matched[file] = {"coverage": "full"}
            rows = sorted(matrix_rows.intersection(line.strip() for line in text.splitlines()))
            if rows:
                coverage = "full" if documents[MATRIX] in text else "rows"
                if matched.get(MATRIX, {}).get("coverage") != "full":
                    matched[MATRIX] = {"coverage": coverage, "rows": rows}
        for file, details in matched.items():
            reads.append({"file": file, "call_id": result.get("call_id"), "excerpt_line": index, **details})

    files = {read["file"] for read in reads}
    assets = files - {"SKILL.md"}
    matrix_reads = [read for read in reads if read["file"] == MATRIX]
    expected_row = next(row for row in matrix_rows if row.startswith("some-users,worsening,"))
    correct_lookup = case != "b" or (
        len(matrix_reads) == 1
        and matrix_reads[0]["coverage"] == "rows"
        and matrix_reads[0]["rows"] == [expected_row]
    )
    implicit = not re.search(r"oncall-handoff|\bskill\b|SKILL\.md", prompt, re.I)
    return {
        "source_log": source.name,
        "source_sha256": digest(raw),
        "tool_excerpt_sha256": digest(excerpt),
        "omitted_tool_discovery_results": sorted(discovery_ids),
        "output_sha256": digest(output),
        "reads": reads,
        "original_prompt": prompt,
        "expected_assets": sorted(EXPECTED[case]),
        "actual_assets": sorted(assets),
        "pass": ("SKILL.md" in files and assets == EXPECTED[case] and correct_lookup
                 and (case != "e" or implicit)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sessions", nargs=5, metavar="SESSION_ID")
    parser.add_argument("--sessions-dir", type=Path, default=Path.home() / ".codex" / "sessions")
    args = parser.parse_args()
    if len(set(args.sessions)) != 5:
        parser.error("supply five distinct session IDs in case order A through E")

    destination = TESTS / "harness"
    destination.mkdir(exist_ok=True)
    candidates = [SKILL / "SKILL.md", *sorted((SKILL / "assets").iterdir())]
    documents = {file.relative_to(SKILL).as_posix(): file.read_text(encoding="utf-8").strip()
                 for file in candidates}
    matrix_reader = csv.reader(documents[MATRIX].splitlines())
    next(matrix_reader)  # Skip the column names.
    matrix_rows = {",".join(row) for row in matrix_reader}
    manifest = {"skill_and_asset_sha256": {file.relative_to(SKILL).as_posix(): digest(file.read_bytes())
                                          for file in candidates}, "runs": {}}
    for case, session in zip("abcde", args.sessions):
        sources = list(args.sessions_dir.rglob(f"*{session}.jsonl"))
        if len(sources) != 1:
            raise ValueError(f"{case}: expected one log for {session}, found {len(sources)}")
        result = collect(case, sources[0], destination, documents, matrix_rows)
        manifest["runs"][case] = {"session_id": session, **result}
        print(f"{case.upper()}: {', '.join(result['actual_assets']) or 'no asset reads'}; "
              f"{'PASS' if result['pass'] else 'FAIL'}")

    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    return 0 if all(run["pass"] for run in manifest["runs"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
