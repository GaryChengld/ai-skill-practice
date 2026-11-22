# Asset loading results

Each case ran in its own fresh Codex app session with a normal handoff request and the original skill directory. Outputs are the unchanged final messages.

| Case | Expected asset reads | Observed in session logs | Result |
| --- | --- | --- | --- |
| A | `handoff-template.md` | `handoff-template.md` | Pass. Both declared severities were preserved. |
| B | `handoff-template.md`, `severity-matrix.csv` (one row) | `handoff-template.md`, `severity-matrix.csv` (one row) | Pass. `some-users,worsening,SEV2` produced `SEV2` for DEL-518. |
| C | `handoff.schema.json` | `handoff.schema.json` | Pass. The raw JSON validated against draft 2020-12. |
| D | `handoff-template.md` | `handoff-template.md` | Pass. SRC-774 got `Unknown` and an open question about urgency. |

From the repository root, `python day-08/oncall-handoff/tests/verify.py` passed using `jsonschema.Draft202012Validator` for C. The same command matches every A/B/D heading to the template in order and checks the literal open-item layout.

`skills-ref validate day-08/oncall-handoff` passed with the upstream reference validator (0.1.0, installed in a temporary virtual environment).

The [initial A response](harness/initial-a.md) kept the headings but changed the open-item labels and punctuation. The Markdown instruction now requires copying the template verbatim and keeping those details. The four fresh reruns preserved the layout and showed no extra or missing asset reads.

The [harness manifest](harness/manifest.json) records session IDs, call IDs, excerpt line numbers, and hashes. To reproduce extraction, pass the manifest's four session IDs in A–D order to `python day-08/oncall-handoff/tests/collect-harness.py` on a machine with the original session logs. The collector confirms reads from returned content and skips tool discovery results.
