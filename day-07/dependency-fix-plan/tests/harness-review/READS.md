# Harness read evidence

Each row matches complete returned file content after LF normalization and removal of interleaved cmd TYPE filename banners, not a command path or model claim.
Raw tool calls and file-read results are retained byte-for-byte in `*-tools.jsonl`; manifest hashes link them to local source logs.
Tool discovery and web-only result bodies are omitted; their requests and omitted call IDs remain recorded. No filesystem result is omitted.
Failed sandbox attempts, empty PowerShell results, and listings count as no content load. Inputs are excluded from skill-size totals.

| Run | Confirmed file | Result call ID | Harness ordinal |
| --- | --- | --- | --- |
| m2 | SKILL.md | `call_dde91fef52164e0cb6564190de04424b` | 87 |
| o | SKILL.md | `call_4149cbf894cd46369db5efbae9df1224` | 88 |
| o | references/npm.md | `call_eaf4a82b3fb94ee78d2a03dd095888b6` | 97 |
| h | SKILL.md | `call_ca6cff1cba48473cbc49347ad4e730d0` | 66 |
| h | references/python.md | `call_b9204ac7053a459a89878e707327dea5` | 73 |
