# Loading evaluation

Method: five new independent Codex tasks, with inherited model settings and no conversation history. Each received one ordinary task prompt; none was told about loading tests or asked to write a trace. The original skill folder was read from disk.
Prompt: `Use the skill at SKILL_DIR to draft a postmortem from INPUT_FILE.` Literal paths, session IDs, model, and source/excerpt hashes are in [manifest.json](harness-review/manifest.json).
Evidence comes from local `~/.codex/sessions/**/*.jsonl`, extracted by [collect-harness.py](collect-harness.py). [READS.md](harness-review/READS.md) correlates calls and returned content; historical model-authored traces are not used as proof. Input reads, failed attempts, and directory listings are excluded below.

| Input/run | Expected skill files | Confirmed content loads | Loading pass |
| --- | --- | --- | --- |
| A | SKILL.md | SKILL.md | Pass |
| B | SKILL.md; references/timezones.md | SKILL.md; references/timezones.md | Pass |
| C | SKILL.md; references/sensitive-incidents.md | SKILL.md; references/sensitive-incidents.md | Pass |
| D | SKILL.md; references/rca-methods.md | SKILL.md; references/rca-methods.md | Pass |
| C follow-up | SKILL.md; references/sensitive-incidents.md | SKILL.md; references/sensitive-incidents.md | Pass |

Sizes use decoded characters with LF newlines divided by 4 and rounded; body counts trim outer blank lines. These are estimates, not tokenizer measurements.

| Layer | Characters | Lines | Approx. tokens |
| --- | --- | --- | --- |
| description | 381 | 1 | 95 |
| Final SKILL.md body | 3,774 | 53 (55 including separator padding) | 944 |
| references/timezones.md | 2,580 | 41 | 645 |
| references/rca-methods.md | 2,604 | 46 | 651 |
| references/sensitive-incidents.md | 2,968 | 40 | 742 |

No unrelated reference content or missed required reference was observed. D triggered RCA from two independent paths without explicitly requesting a tree, and its output includes one. B preserved both UTC candidates for its repeated-hour timestamp. The earlier clarification to "competing causal explanations" remains; this review removed the redundant timeline-order phrase without changing reference conditions.

Output checks: original C had 3/4 short action rows, correcting the old report's count of one. An enumerated five-field checklist still left 4/5 C and 3/4 D rows short in the first review run. Replaced it with pipe-cell counting, repair, and separate owner/due TBD cells; a fresh C follow-up has 4/4 complete rows. All raw outputs are retained without repair. A–D used the enumerated revision; only C follow-up used the final checklist.

Validation: `skills-ref` 0.1.1 `agentskills validate day-06/incident-postmortem` and skill-creator `quick_validate.py` passed. Day-03 remains unchanged. The spring DST gap and general loading/output reliability remain unproven by these few explicit-invocation cases.
