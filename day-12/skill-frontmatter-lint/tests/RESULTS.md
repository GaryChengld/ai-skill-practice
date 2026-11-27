# Day 12 results

The [27 fixtures](EDGE-CASES.md) were frozen in `5b47a11` and the [behavior checklist](CHECKLIST.md) in `f72ce10`. `python -B -m unittest day-12/skill-frontmatter-lint/scripts/test_lint_frontmatter.py` passed 9 tests, including 27 fixture subtests and the isolated missing-dependency check. The pinned `uv run` path ran successfully. `skills-ref validate day-12\skill-frontmatter-lint` exited 0 and printed `Valid skill: day-12\skill-frontmatter-lint`.

## Differential validation

The [full comparison](DIFFERENTIAL.md) covers all 27 fixtures. Accept/reject agrees on 19. For parse failures the CLI uses exit 3, whereas `skills-ref` reports a generic failure. On fixture 19, both reject, but StrictYAML rejects the flow-list syntax before reporting field issues.

| Fixture | Linter / reference | Explanation |
| --- | --- | --- |
| 13 metadata value | Reject / accept | Reference limitation. It stringifies metadata values, including an unquoted number. |
| 14 allowed-tools list | Reject / accept | Reference bug. It does not enforce the specified string type. |
| 15 BOM and CRLF | Accept / reject | Encoding policy difference. The linter strips the BOM and accepts CRLF. The reference expects `---` at character zero. |
| 16 invalid UTF-8 | Reject / accept | Reference bug. It reads with the host's default encoding. In explicit UTF-8 mode it raises an uncaught `UnicodeDecodeError`. |
| 17 boolean name | Reject / accept | Parser interpretation differs. PyYAML resolves unquoted `yes` as boolean. Schema-less StrictYAML treats it as text. |
| 18 unknown field | Warn / reject | Policy difference. Day 12 requires a warning, and the reference rejects unknown fields. |
| 23 metadata key | Reject / accept | Reference limitation. It stringifies metadata keys, including an unquoted boolean. |
| 25 numeric license | Reject / accept | Reference limitation. It does not enforce a string license and its parser treats the scalar as text. |

## Day 01–11 audit

- **0 errors and 0 warnings each:** `day-01/conventional-commits`, `day-02/competitors/pr-description`, `day-02/release-notes`, `day-03/incident-postmortem`.
- **0 errors and 0 warnings each:** `day-04/stale-branches`, `day-06/incident-postmortem`, `day-07/dependency-fix-plan`, `day-08/oncall-handoff`.
- **0 errors and 0 warnings each:** `day-09/conventional-commits`, `day-10/BEFORE/migration-safety-review`, `day-10/migration-safety-review`, `day-11/semver-next`. No parse failures across the 12 skills.

## Fresh-session checks

| Run | Checklist | Evidence |
| --- | --- | --- |
| 1 · skill | 1a P, 1b P, 1c P | [Native exit 1](harness/1-skill.jsonl) |
| 1 · baseline | 1a P, 1b P, 1c P | [Zero enabled skills](harness/1-baseline.jsonl) |
| 2 · skill | 2a P, 2b P, 2c P | [Native exit 3](harness/2-skill.jsonl) |
| 3 · skill | 3a P, 3b P | [Native exit 0](harness/3-skill.jsonl) |

The [manifest](harness/manifest.json) verifies three linter executions, no source reads, and unchanged fixture bytes. The baseline tied on the shared checklist. The hardest boundary was native YAML type coercion: freezing the `yes` and `1.0` cases exposed how a parser can accept the same text while losing the type distinction. [Early sessions](harness/initial/) also showed why diagnostics should name the actual value type and offending field.
