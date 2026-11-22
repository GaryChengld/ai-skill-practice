# Asset loading results

Each case ran in a fresh Codex app session. A–D named the original skill directory to isolate asset loading. E requested a shift summary for the next responder and supplied the notes inline. Outputs are the unchanged final messages.

| Case | Expected asset reads | Observed in session logs | Result |
| --- | --- | --- | --- |
| A | `handoff-template.md` | `handoff-template.md` | Pass. Both declared severities were preserved. |
| B | `handoff-template.md`, `severity-matrix.csv` (one data row) | `handoff-template.md`, `severity-matrix.csv` (header and one data row) | Pass. `some-users,worsening,SEV2` produced `SEV2` for DEL-518. |
| C | `handoff.schema.json` | `handoff.schema.json` | Pass. The raw JSON validated against draft 2020-12. |
| D | `handoff-template.md` | `handoff-template.md` | Pass. SRC-774 got `Unknown` and an open question about urgency. |
| E | Automatic skill discovery, then `handoff-template.md` | `SKILL.md` and `handoff-template.md` via the repository skill registry | Pass. The logged request did not name or link to the skill. |

From the repository root, `python day-08/oncall-handoff/tests/verify.py` passed using `jsonschema.Draft202012Validator` for C. The same command checks the exact heading sequence and every entry line in A/B/D/E, including the standalone `None reported.` marker for an empty list section.

`skills-ref validate day-08/oncall-handoff` passed with the upstream reference validator (0.1.0, installed in a temporary virtual environment).

The [initial A response](harness/initial-a.md) changed the open-item labels. A later review found that resolved entries also differed across A/B/D and B omitted the period in the empty marker. The revised template fixes every entry layout, the instructions require its punctuation in every section, and the verifier now checks each list section. The five reruns confirmed the intended asset reads.

For E, a temporary `.agents/skills/oncall-handoff` junction pointed to the original skill directory. A fresh session selected it from the ordinary request. The [harness manifest](harness/manifest.json) records prompts, session and tool call IDs, excerpt line numbers, and hashes. To reproduce extraction, pass its session IDs in A–E order to `python day-08/oncall-handoff/tests/collect-harness.py` where the original session logs are available.
