# Domain loading evaluation

Method: eight fresh independent Codex tasks, inherited model, original on-disk skill folder. Ordinary prompt: `Use the skill at SKILL_DIR. Our scanner flagged this; what should we change? The repository snapshot and finding are in INPUT_FILE.` No expected reads or testing instructions were supplied. N/P/J/M/G used baseline `e50e15e`; M2/O/H used the revised description/evidence rule.
Evidence: [extractor](collect-harness.py); [baseline reads](harness/READS.md) and [manifest](harness/manifest.json); [review reads](harness-review/READS.md) and [manifest](harness-review/manifest.json). Complete returned content establishes reads; model self-reports do not. Raw final responses are `output-<input>.md`.

| Input | Expected files beyond SKILL.md | Actual domain content reads | Pass | Loaded skill tokens | All-in-one tokens |
| --- | --- | --- | --- | --- | --- |
| N | references/npm.md | references/npm.md | Pass | 2,236 | 4,270 |
| P | references/python.md | references/python.md | Pass | 2,358 | 4,270 |
| J | references/jvm.md | references/jvm.md | Pass | 2,226 | 4,270 |
| M | references/python.md | references/python.md | Pass | 2,358 | 4,270 |
| G | None | None | Pass | 1,275 | 4,270 |
| M2 | None; ask for ownership evidence | None; path/chain requested | Pass | 1,293 | 4,288 |
| O | references/npm.md | references/npm.md | Pass | 2,254 | 4,288 |
| H | references/python.md | references/python.md | Pass | 2,376 | 4,288 |

Sizes: LF-normalized decoded characters / 4, rounded; body trims outer blanks. Baseline → review full SKILL.md is 5,100 → 5,172 characters; the monolith concatenates that revision plus all references (17,078 → 17,150 characters). Totals count repeated skill reads if present; none occurred. Inputs, external docs, wrappers, and system prompts are excluded; these are skill-text estimates.

| Layer | Characters | Lines | Approx. tokens |
| --- | --- | --- | --- |
| description, baseline → review | 355 → 413 | 1 | 89 → 103 |
| Body, baseline → review | 4,695 → 4,709 | 48 | 1,174 → 1,177 |
| references/npm.md | 3,843 | 51 | 961 |
| references/python.md | 4,332 | 53 | 1,083 |
| references/jvm.md | 3,803 | 62 | 951 |

No over-read or missed domain read occurred. Original M supplies the answer's ownership path, so M2 tests the missing-path case: no references read, ownership Unknown, path/chain requested. G uses no reference and discloses missing Go guidance. O proposes root-only parent-scoped overrides with compatibility checks and removal after an upstream upgrade passes without the override; H defers with mitigation, owner, and review date. See [review analysis](../../NOTES.md#review-follow-up).
Routing conditions were unchanged: M2 passed the existing ambiguity rule. Replaced test-specific evidence wording with user-supplied advisory provenance and expanded description keywords. The extractor initially missed M2's skill read because cmd TYPE interleaved filename banners inside its description; matching now removes those banners while preserving raw event bytes. No skill rerun or instruction change was needed for that extraction error.

Validation: official `skills-ref` 0.1.1 and skill-creator `quick_validate.py` passed; body 48 lines, references 51/53/62, inputs 8–20. These single explicit-invocation cases do not establish automatic triggering or coverage of pnpm, pip constraints execution, Gradle, or multiple findings. No remediation commands were executed.
