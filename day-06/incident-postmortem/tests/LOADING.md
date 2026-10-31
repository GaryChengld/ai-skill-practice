# Loading evaluation

Method: six independent `fork_turns:none` sessions, three initial and three final, with inherited model settings (not pinned). Each received only the original skill-folder path, its input path, and an instruction to use the skill; file contents were not pasted or transcribed. Reads used `exec_command` with `cmd.exe type`.
Expected loads were recorded before testing. Input reads are excluded below; detailed final traces include all content reads. Final outputs are `output-a.md`, `output-b.md`, and `output-c.md`; initial read traces remain in `trace-*-initial.md`.

| Input | Expected skill files | Actually opened in final run | Pass |
| --- | --- | --- | --- |
| A | SKILL.md | SKILL.md ([trace](trace-a.md)) | Pass |
| B | SKILL.md; references/timezones.md | SKILL.md; references/timezones.md ([trace](trace-b.md)) | Pass |
| C | SKILL.md; references/sensitive-incidents.md | SKILL.md; references/sensitive-incidents.md ([trace](trace-c.md)) | Pass |

Sizes use UTF-8 decoded character counts with LF newlines, divided by 4 and rounded; these are estimates, not tokenizer measurements. Body counts trim outer blank lines.

| Layer | Characters | Lines | Approx. tokens |
| --- | --- | --- | --- |
| description | 381 | 1 | 95 |
| SKILL.md body | 3,628 | 53 (55 including separator padding) | 907 |
| references/timezones.md | 2,580 | 41 | 645 |
| references/rca-methods.md | 2,604 | 46 | 651 |
| references/sensitive-incidents.md | 2,968 | 40 | 742 |

Neither round showed over-reading or under-reading. B preserved a repeated-hour timestamp as Unknown without loading RCA guidance: timestamp uncertainty alone is not a competing cause. Clarified the RCA condition from "competing explanations" to "competing causal explanations" to prevent that possible over-read; this is a preventive clarification, not a demonstrated failure fix.

Initial inputs included routing hints (negative sensitive-data statements and single-chain assertions) and explicit redaction/order instructions. Removed those hints, then reran A/B/C in new sessions against the final files; loading results stayed the same. Initial failed sandbox starts read no content; final traces have no failed reads.

Validation: `skills-ref` 0.1.1, `agentskills validate day-06/incident-postmortem` → Valid; skill-creator's `quick_validate.py` also passed. Day-03 remains unchanged.
Scope: these explicit-invocation tests exercise conditional reads, not automatic client startup loading. The RCA reference's positive trigger and the spring DST gap remain untested. C's Detect-action row omits a Due cell in the raw output; a loading Pass is not an output-quality Pass. Three fixtures do not establish general loading accuracy.
