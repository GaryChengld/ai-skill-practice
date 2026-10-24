# Editorial audit

Post-fix snapshot, 2026-10-24. These are repository quality checks, separate from reference validation.
Single = one physical, plain-scalar description line; Intent = explicit Use when / Use this skill when; Boundary = meaningful excluded requests.
Length = original body cap (commit 150, release 40, incident 80, branches 60; the PR stub has no cap). Count body lines excluding outer blank lines.
Portable = no vendor-specific tool names or paths anywhere in SKILL.md; Rationale = explicit integrity/safety prohibitions explain the consequence.
Isolation = worked examples do not supply answers to behavioral test fixtures (N/A for routing-only tests or the PR stub); Legacy = outstanding required review items addressed.

| Skill | Single | Intent | Boundary | Length | Portable | Rationale | Isolation | Legacy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| conventional-commits | Pass | Pass | Pass | Pass | Pass | Pass | N/A | Pass |
| release-notes | Pass | Pass | Pass | Pass | Pass | Pass | N/A | Pass |
| pr-description | Pass | Pass | Pass | N/A | Pass | Pass | N/A | N/A |
| incident-postmortem | Pass | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| stale-branches | Pass | Pass | Pass | Pass | Fail | Pass | Pass | Pass |

The three previously failed Rationale checks now pass: invented commit references mislead reviewers, inaccurate release facts mislead upgrade decisions, and a PR draft does not authorize publication. Each checked rule now states its reason.
Portability failure is deliberate: day-04 requires Claude-style Bash patterns. Ignoring them preserves the body safety rule but removes pre-approval; no claim of universal client support.
Body counts from `python day-05/lint.py`: 93/150, 33/40, 5/N/A, 68/80, 45/60 in table order. The script checks Single, Intent, and capped Length; all passed.

## Fixes

Initial repairs were committed in `bc5cf45`; review follow-up fixes were committed in `998c513`, both after explicit authorization.
- `bc5cf45` (base `23215a3`), day-01: replace folded description with a single plain string; omit the redundant colon-containing format parenthesis so YAML stays valid.
- `bc5cf45` (base `ab236a3`), day-03: replace the payment retry remedy with a conditional search-index alias example, outside the INC-482 domain.
- `bc5cf45` (base `ab236a3`), day-03: split the timezone Gotcha and remove its duplicated canary-action instruction.
- `bc5cf45` (base `f7432ae`), day-04: explicitly handle a branch equal to the baseline, with no unique commits; distinguish commit age from unknown branch creation age and require owner review.
- `bc5cf45` (base `f7432ae`), day-04 test: use TemporaryDirectory and verify cleanup; the real Git collection run passed its original five checks plus fixture removal.
- `998c513` (review baseline `aaf5482`): restore the day-01 150-line cap in lint and add reasons to the three previously failed rules; this audit reflects those corrections.
- `998c513` (review baseline `aaf5482`), day-04: enforce baseline-equal holds in the main recommendation flow, deletion conditions, and final checklist.
- `998c513` (review baseline `aaf5482`): add four independent-session routing challenges without deliverable nouns; the companion notes record the local catalog's publication limitation.

The baseline-equality rule now connects the edge case to the main flow and checklist. Original smoke output remains historical, not claimed as a rerun; old incident outputs likewise remain unchanged and are not new evidence for the revised example.
