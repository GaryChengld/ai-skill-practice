# Harness read evidence

The evaluator extracted tool events from local Codex session JSONL files after each session finished. The evaluated model was never asked to record a trace or told this was a loading test. `manifest.json` records session IDs, literal prompts, model, source hashes, and excerpt hashes.

Each `*-tools.jsonl` retains original call/result records byte-for-byte. Tool-discovery requests remain, but their bulky metadata-only results are omitted with call IDs recorded in the manifest. No reasoning or unrelated session messages are exported. Run `python day-06/incident-postmortem/tests/collect-harness.py` on the original machine to repeat extraction.

Paths below are relative to the skill root. A path in a command is insufficient: the paired result must return the requested content. Missing instruction-file probes and directory listings are separate from content loads.

| Case | Confirmed content returned, in order | Supporting call IDs in excerpt |
| --- | --- | --- |
| A | `SKILL.md`; `tests/input-a.md` | `call_1c3f770066744130bd2f041a4c264907`; `call_4d9fb76e53b643afaad696a8c01342f5` |
| B | `SKILL.md`; `tests/input-b.md`; `references/timezones.md` | `call_a6d5f5c9f7a945bf98a500f3c69906ca`; `call_40da8d19168d4e7db36fff8706e16575` |
| C | `SKILL.md`; `tests/input-c.md`; `references/sensitive-incidents.md` | `call_fb87518e771945809352709c357ee3a4`; `call_0062276cebab431f83eb0a98317f662e`; `call_5b1b40461a7243ceb42ddf2fa1e43922` |
| D | `SKILL.md`; `tests/input-d.md`; `references/rca-methods.md` | `call_6a23ca15279e4abb96af35a2dfd1e044`; `call_8ee1651bae914cd58b69864d62e8dbf9`; `call_2bd23914377842ac916372f43a7952b9` |
| C follow-up | `SKILL.md`; `tests/input-c.md`; `references/sensitive-incidents.md` | `call_26210e16344043c8890f1ce3106dbf51`; `call_e003c0f57e3d4699a9fe9f522de251f4`; `call_a90ea1d0f945435abfa7451dd2b0c1b9` |

All four first-round sessions encountered sandbox/reader startup failures and unresponsive PowerShell before falling back to successful elevated `cmd.exe type` reads. Those failed or empty returns are retained, not counted as content loads. B's `call_9440c04350554b81a1124967fe308058` returned no content despite listing several paths; only the later returned timezone content establishes that read. C listed `tests/` filenames in its final read call; it did not read their contents. Conditional AGENTS.md probes returned no content.

The original `trace-*.md` and `trace-*-initial.md` files are historical model-authored reports; they are not independent evidence for this rerun. Original outputs also remain unchanged. `output-*-review.md` files are extracted final session messages, without corrections to their action tables.

A–D read the first review revision with an enumerated five-field checklist. That still produced short action rows in C and D. C follow-up is a new ordinary-prompt session against the final count-and-repair checklist; no testing instruction or corrective follow-up was sent to any evaluated session. Its four action rows each have five cells. The other four sessions were not rerun against that last checklist change; their actual read versions remain visible in the excerpts.
