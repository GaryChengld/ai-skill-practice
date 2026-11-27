# Day 12 results

The [fixture matrix](EDGE-CASES.md) (`5b47a11`), [behavior checklist](CHECKLIST.md) (`f72ce10`), and [follow-up checks](FOLLOWUP.md) (`adb1f64`, `ec0b3db`) preceded their runs. `uv run --no-project --with PyYAML==6.0.3 python -B -m unittest day-12/skill-frontmatter-lint/scripts/test_lint_frontmatter.py` passed 11 tests and 27 fixture subtests. uv resolved Python 3.12.12 and PyYAML 6.0.3. `skills-ref validate day-12\skill-frontmatter-lint` printed `Valid skill: day-12\skill-frontmatter-lint`.

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

**Day 01–11 audit.** All 12 skills had 0 errors, 0 warnings, and 0 parse failures, including the Day 02 competitor and the Day 10 BEFORE copy.

## Fresh-session checks

| Case | Skill checks | Baseline checks | Evidence |
| --- | --- | --- | --- |
| 1 · multiple errors | 1a P, 1b P, 1c P | 1a P, 1b P, 1c P | [Exit 1](harness/1-skill.jsonl) · [Baseline](harness/1-baseline.jsonl) |
| 2 · invalid YAML | 2a P, 2b P, 2c P | — | [Exit 3](harness/2-skill.jsonl) |
| 3 · valid skill | 3a P, 3b P | — | [Exit 0](harness/3-skill.jsonl) |
| 4 · numeric metadata value | 4a P, 4b P | 4a P, 4b P | [Exit 1](harness/4-skill.jsonl) · [Baseline](harness/4-baseline.jsonl) |
| 5 · boolean name | 5a P, 5b P | 5a P, 5b P | [Exit 1](harness/5-skill.jsonl) · [Baseline](harness/5-baseline.jsonl) |
| 6 · boolean metadata key | 6a P, 6b P | 6a F, 6b P | [Exit 1](harness/6-skill.jsonl) · [Baseline](harness/6-baseline.jsonl) |
| 7 · invalid encoding | 7a P, 7b P | 7a P, 7b P | [Exit 3](harness/7-skill.jsonl) · [Baseline](harness/7-baseline.jsonl) |

The [manifest](harness/manifest.json) verifies seven linter executions, no source reads, and unchanged fixtures. The skill passed 16/16 checks and scored 11/11 on paired cases, versus 10/11 for the baseline. The baseline caught all three coercions and identified the invalid byte, but omitted the string-key requirement in case 6. The frozen `yes` and `1.0` cases exposed genuine parser differences in the reference comparison. [Early sessions](harness/initial/) showed why diagnostics should name the actual type and field.
