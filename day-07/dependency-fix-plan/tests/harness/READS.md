# Harness read evidence

Each row matches the complete LF-normalized file content in a returned tool result, not a command path or model claim.
Raw tool calls and file-read results are retained byte-for-byte in `*-tools.jsonl`; manifest hashes link them to local source logs.
Tool discovery and web-only result bodies are omitted; their requests and omitted call IDs remain recorded. No filesystem result is omitted.
Failed sandbox attempts, empty PowerShell results, and listings count as no content load. Inputs are excluded from skill-size totals.

| Run | Confirmed file | Result call ID | Harness ordinal |
| --- | --- | --- | --- |
| n | SKILL.md | `call_37e31b41a59942fa807c9bbd81760c42` | 63 |
| n | references/npm.md | `call_c698be0429f646c09ed72e6c74557079` | 73 |
| p | SKILL.md | `call_5194f046e4b24fb8beae831f346216c6` | 66 |
| p | references/python.md | `call_7c7349820bfd4cc49a77e7e290c958f9` | 71 |
| j | SKILL.md | `call_995302e1504f430dbab09b846e51ba96` | 68 |
| j | references/jvm.md | `call_992af8a6bc1c4252ae68fcdc5622e3fb` | 79 |
| m | SKILL.md | `call_2a1ffd41f8d64500b1b356d63b164917` | 66 |
| m | references/python.md | `call_9d9829fa60334d6c93ebcb74857a9fdc` | 71 |
| g | SKILL.md | `call_ec4641c412204f36848e1f5cf8f59728` | 67 |
| day06-d | SKILL.md | `call_3c4cf8ff102f4779afedfb223d557d47` | 80 |
| day06-d | references/rca-methods.md | `call_41a33d63b3cd40f0b8284099ed9cf73e` | 88 |

Day-06 D action-row cell counts from the untouched final response: `[5, 5, 5, 5]`.
All rows have five cells: True.
