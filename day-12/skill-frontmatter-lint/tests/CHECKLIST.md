# Frozen behavior checklist

Use the same request for both input 1 variants. In each session ask whether the named skill's frontmatter is set up correctly. Give the fixture path and request findings only. Score each check independently. Accept equivalent wording and score script use separately using the harness.

| Input | Fixture | ID | Response check |
| --- | --- | --- | --- |
| 1 | `19-multiple-errors/Bad-Name` | 1a | Reports the uppercase name, empty description, and YAML list where an allowed-tools string is required. |
| 1 | `19-multiple-errors/Bad-Name` | 1b | Gives actionable fixes for all three findings, including keeping the directory name in sync with the lowercased name. |
| 1 | `19-multiple-errors/Bad-Name` | 1c | Reports no issues beyond those in the linter output and leaves the file untouched. |
| 2 | `11-yaml-colon/yaml-colon` | 2a | Calls out a YAML parse failure on line 3 and explains the unquoted colon-space. |
| 2 | `11-yaml-colon/yaml-colon` | 2b | Suggests quoting the entire description or rephrasing it to remove the colon-space. |
| 2 | `11-yaml-colon/yaml-colon` | 2c | Reports no unrelated lint findings and leaves the file untouched. |
| 3 | `02-full-fields/full-fields` | 3a | Says that the frontmatter is valid. |
| 3 | `02-full-fields/full-fields` | 3b | Reports no errors or warnings for the valid fixture and leaves the file untouched. |
