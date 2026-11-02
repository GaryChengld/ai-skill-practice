"""Export real tool events and outputs from independent local harness sessions.

Run from any directory with Python 3.12+. No model-authored trace is consumed.
Full returned file content, rather than a path in a command, confirms a load.
"""
from pathlib import Path
import hashlib
import json
import re

RUNS = {
    "n": "01a19a2d-07cd-7883-9387-72a8d322a944",
    "p": "01a19a2d-323f-70f2-be26-34219147171c",
    "j": "01a19a2d-4477-76c3-a400-fb8e69be7da1",
    "m": "01a19a2d-5669-7581-b168-fcc11777a561",
    "g": "01a19a2d-7398-7ab0-8189-3a6828a15f03",
    "day06-d": "01a19a2d-91e3-7d61-882c-a6c7d5c286a5",
}
TESTS = Path(__file__).resolve().parent
SKILL = TESTS.parent
REPO = SKILL.parents[1]
DEST = TESTS / "harness"
DEST.mkdir(exist_ok=True)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def strings(value):
    """Unwrap JSON text blocks and exec-result objects without executing them."""
    if isinstance(value, str):
        yield value.replace("\r\n", "\n")
        if value.lstrip().startswith(("{", "[")):
            try:
                yield from strings(json.loads(value))
            except (ValueError, RecursionError):
                pass
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def action_cells(output):
    section = re.search(r"^## Action Items\s*\n(.*?)(?=^## |\Z)", output, re.M | re.S)
    if not section:
        return []
    rows = [line for line in section[1].splitlines() if line.strip().startswith("|")]
    return [len(re.split(r"(?<!\\)\|", line.strip().strip("|")))
            for line in rows[2:]]


manifest = {}
for case, session_id in RUNS.items():
    sources = list((Path.home() / ".codex/sessions").rglob(f"*{session_id}.jsonl"))
    if len(sources) != 1:
        raise ValueError(f"{case}: expected one harness source, got {sources}")
    source = sources[0]
    raw = source.read_bytes()
    events = [(line, json.loads(line)) for line in raw.splitlines(keepends=True)]
    complete = [e["payload"] for _, e in events if e.get("type") == "event_msg"
                and e.get("payload", {}).get("type") == "task_complete"]
    if not complete:
        print(f"{case}: pending")
        continue
    output = complete[-1].get("last_agent_message")
    if not isinstance(output, str):
        raise ValueError(f"{case}: missing final message")
    (TESTS / f"output-{case}.md").write_text(output + "\n", encoding="utf-8", newline="\n")
    calls = [e["payload"] for _, e in events if e.get("type") == "response_item"
             and e.get("payload", {}).get("type") in ("function_call", "custom_tool_call")]
    discovery = {c.get("call_id") for c in calls if "ALL_TOOLS." in c.get("input", "")
                 and "await tools." not in c.get("input", "")}
    web_only = {c.get("call_id") for c in calls
                if ("tools.web__run" in c.get("input", "")
                    and not re.search(r"tools\.(exec_command|write_stdin|mcp__node_repl)", c.get("input", "")))
                or c.get("name") in ("web.run", "web__run")}
    types = {"function_call", "custom_tool_call", "function_call_output", "custom_tool_call_output"}
    excerpt = b"".join(line for line, e in events if e.get("type") == "response_item"
                       and e.get("payload", {}).get("type") in types
                       and not (e["payload"]["type"].endswith("_output")
                                and e["payload"].get("call_id") in discovery | web_only))
    (DEST / f"{case}-tools.jsonl").write_bytes(excerpt)
    root = REPO / "day-06/incident-postmortem" if case == "day06-d" else SKILL
    candidates = [root / "SKILL.md", *sorted((root / "references").glob("*.md"))]
    documents = {p.relative_to(root).as_posix(): p.read_text(encoding="utf-8") for p in candidates}
    reads = []
    for _, e in events:
        p = e.get("payload", {})
        if e.get("type") != "response_item" or p.get("type") not in ("function_call_output", "custom_tool_call_output"):
            continue
        fragments = list(strings(p.get("output")))
        for name, content in documents.items():
            if any(content.rstrip() in fragment for fragment in fragments):
                reads.append({"file": name, "call_id": p.get("call_id"), "ordinal": e.get("ordinal"),
                              "characters": len(content), "file_sha256": sha((root / name).read_bytes())})
    contexts = [e["payload"] for _, e in events if e.get("type") == "turn_context"]
    prompts = [e["payload"].get("message") for _, e in events if e.get("type") == "event_msg"
               and e.get("payload", {}).get("type") == "user_message"]
    if not prompts:
        # New independent GUI tasks arrive as a harness-authored delegation event.
        prompts = [match.group(1) for _, e in events
                   if e.get("type") == "response_item"
                   and e.get("payload", {}).get("type") == "function_call_output"
                   for text in strings(e["payload"].get("output"))
                   if (match := re.search(r"<codex_delegation>.*?<input>(.*?)</input>", text, re.S))]
    if not prompts:
        raise ValueError(f"{case}: ordinary prompt not found in harness events")
    loaded = sorted({r["file"] for r in reads})
    expected = {"n": ["references/npm.md"], "p": ["references/python.md"], "j": ["references/jvm.md"],
                "m": ["references/python.md"], "g": [], "day06-d": ["references/rca-methods.md"]}[case]
    record = {
        "session_id": session_id, "source_file": source.name, "source_sha256": sha(raw),
        "tool_excerpt_sha256": sha(excerpt), "prompt": prompts[0],
        "model": contexts[-1].get("model") if contexts else None,
        "omitted_metadata_only_result_call_ids": sorted(discovery),
        "omitted_web_only_result_call_ids": sorted(web_only),
        "confirmed_content_reads": reads, "loaded_files": loaded,
        "expected_files": ["SKILL.md", *expected], "loading_pass": loaded == sorted(["SKILL.md", *expected]),
        "loaded_characters_including_repeat_reads": sum(r["characters"] for r in reads),
        "all_in_one_characters": sum(len(c) for c in documents.values()),
    }
    if case == "day06-d":
        record["action_row_cell_counts"] = action_cells(output)
    manifest[case] = record
    print(f"{case}: files={loaded}; pass={record['loading_pass']}; chars={record['loaded_characters_including_repeat_reads']}")
(DEST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")

skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
_, frontmatter, body = skill_text.split("---", 2)
description = next(line.removeprefix("description: ") for line in frontmatter.splitlines() if line.startswith("description: "))
sizes = {"description_characters": len(description), "body_lines": len(body.strip().splitlines()),
         "body_characters": len(body.strip()), "skill_file_characters": len(skill_text),
         "references": {p.name: {"lines": len(p.read_text(encoding='utf-8').splitlines()),
                                 "characters": len(p.read_text(encoding='utf-8'))}
                        for p in sorted((SKILL / "references").glob("*.md"))}}
(DEST / "sizes.json").write_text(json.dumps(sizes, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(sizes, indent=2))

report = ["# Harness read evidence", "",
          "Each row matches the complete LF-normalized file content in a returned tool result, not a command path or model claim.",
          "Raw tool calls and file-read results are retained byte-for-byte in `*-tools.jsonl`; manifest hashes link them to local source logs.",
          "Tool discovery and web-only result bodies are omitted; their requests and omitted call IDs remain recorded. No filesystem result is omitted.",
          "Failed sandbox attempts, empty PowerShell results, and listings count as no content load. Inputs are excluded from skill-size totals.", "",
          "| Run | Confirmed file | Result call ID | Harness ordinal |",
          "| --- | --- | --- | --- |"]
for case, record in manifest.items():
    for read in record["confirmed_content_reads"]:
        report.append(f"| {case} | {read['file']} | `{read['call_id']}` | {read['ordinal']} |")
if "day06-d" in manifest:
    counts = manifest["day06-d"]["action_row_cell_counts"]
    report.extend(["", f"Day-06 D action-row cell counts from the untouched final response: `{counts}`.",
                   f"All rows have five cells: {bool(counts) and all(n == 5 for n in counts)}."])
(DEST / "READS.md").write_text("\n".join(report) + "\n", encoding="utf-8", newline="\n")
