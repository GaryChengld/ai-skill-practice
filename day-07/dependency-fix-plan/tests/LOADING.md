# Domain loading evaluation

Method: five fresh independent Codex tasks, inherited model, original on-disk skill folder. Ordinary prompt: `Use the skill at SKILL_DIR. Our scanner flagged this; what should we change? The repository snapshot and finding are in INPUT_FILE.` No expected reads or testing instructions were supplied.
Evidence: [extractor](collect-harness.py), [raw tool excerpts and read call IDs](harness/READS.md), [session IDs, exact prompts, source hashes and counts](harness/manifest.json). Successful returned content establishes reads; model self-reports are not evidence. Raw final responses are `output-{n,p,j,m,g}.md`.

| Input | Expected files beyond SKILL.md | Actual domain content reads | Pass | Loaded skill tokens | All-in-one tokens |
| --- | --- | --- | --- | --- | --- |
| N | references/npm.md | references/npm.md | Pass | 2,236 | 4,270 |
| P | references/python.md | references/python.md | Pass | 2,358 | 4,270 |
| J | references/jvm.md | references/jvm.md | Pass | 2,226 | 4,270 |
| M | references/python.md | references/python.md | Pass | 2,358 | 4,270 |
| G | None | None | Pass | 1,275 | 4,270 |

Sizes: LF-normalized decoded characters / 4, rounded; body trims outer blank lines. Loaded totals include the full SKILL.md (5,100 characters) plus returned references, including repeat reads if any. The monolith baseline concatenates that same skill and all three references (17,078 characters). Inputs, external documentation, tool wrappers, and system prompts are excluded; these are skill-text estimates, not measured context tokens.

| Layer | Characters | Lines | Approx. tokens |
| --- | --- | --- | --- |
| description | 355 | 1 | 89 |
| Body | 4,695 | 48 | 1,174 |
| references/npm.md | 3,843 | 51 | 961 |
| references/python.md | 4,332 | 53 | 1,083 |
| references/jvm.md | 3,803 | 62 | 951 |

No over-read or missed domain read occurred. M used the finding's services/indexer/uv.lock path and ignored the unrelated web manifests; G loaded only the body, explicitly disclosed missing Go guidance, and consulted official Go documentation. No skill file was read twice. The measured skill-text saving is approximately 45–70% per run.
Routing wording added before these runs requires ownership before consulting the table, prohibits globbing the reference directory, and explicitly selects no reference for unsupported ecosystems. Results did not justify a post-run wording change or rerun. These five explicit-invocation cases do not establish automatic triggering or reliability for ambiguous ownership, pnpm, pip, Gradle, or multiple findings.

Validation: official `skills-ref` 0.1.1 `agentskills validate day-07/dependency-fix-plan` and skill-creator `quick_validate.py` passed. Input lengths are 11/12/12/12/11 lines; reference examples use different packages and scenarios. No dependency installation or real project remediation was tested.
