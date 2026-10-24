# Editorial audit

Post-fix snapshot, 2026-10-24. These are repository quality checks, separate from reference validation.
Single = one physical, plain-scalar description line; Intent = explicit Use when / Use this skill when; Boundary = meaningful excluded requests.
Length = original body cap (release 40, incident 80, branches 60; other tasks set no cap). Count body lines excluding outer blank lines.
Portable = no vendor-specific tool names or paths anywhere in SKILL.md; Rationale = explicit integrity/safety prohibitions explain the consequence.
Isolation = worked examples do not supply answers to behavioral test fixtures (N/A for routing-only tests or the PR stub); Legacy = outstanding required review items addressed.

| Skill | Single | Intent | Boundary | Length | Portable | Rationale | Isolation | Legacy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| conventional-commits | Pass | Pass | Pass | N/A | Pass | Fail | N/A | Pass |
| release-notes | Pass | Pass | Pass | Pass | Pass | Fail | N/A | Pass |
| pr-description | Pass | Pass | Pass | N/A | Pass | Fail | N/A | N/A |
| incident-postmortem | Pass | Pass | Pass | Pass | Pass | Pass | Pass | Pass |
| stale-branches | Pass | Pass | Pass | Pass | Fail | Pass | Pass | Pass |

Rationale failures: day-01 bans invented issue details, release-notes bans invented changes, and the PR stub bans publication without stating a consequence beside each rule. These are follow-up editorial gaps, not validation errors; avoid broad rewrites in this timebox.
Portability failure is deliberate: day-04 requires Claude-style Bash patterns. Ignoring them preserves the body safety rule but removes pre-approval; no claim of universal client support.
Body counts from `python day-05/lint.py`: 93, 33, 5, 68, 45 in table order. The script checks Single, Intent, and capped Length; all passed.

## Fixes

Repairs were initially prepared without commits; after explicit authorization, all fixes below were committed in `bc5cf45`.
- `bc5cf45` (base `23215a3`), day-01: replace folded description with a single plain string; omit the redundant colon-containing format parenthesis so YAML stays valid.
- `bc5cf45` (base `ab236a3`), day-03: replace the payment retry remedy with a conditional search-index alias example, outside the INC-482 domain.
- `bc5cf45` (base `ab236a3`), day-03: split the timezone Gotcha and remove its duplicated canary-action instruction.
- `bc5cf45` (base `f7432ae`), day-04: explicitly handle a branch equal to the baseline, with no unique commits; distinguish commit age from unknown branch creation age and require owner review.
- `bc5cf45` (base `f7432ae`), day-04 test: use TemporaryDirectory and verify cleanup; the real Git collection run passed its original five checks plus fixture removal.

The baseline-equality fix satisfies the allowed day-04 alternative. Original smoke output remains historical, not claimed as a rerun; old incident outputs likewise remain unchanged and are not new evidence for the revised example.
