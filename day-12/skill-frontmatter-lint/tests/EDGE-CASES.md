# Frozen frontmatter cases

The UTF-8 BOM is accepted as an encoding marker. CRLF is accepted so normal Windows checkout settings do not change lint results. Invalid UTF-8 fails with a line number. Examples use the exercise's ASCII name grammar.

| Fixture | Input characteristic | Exit | Expected finding codes |
| --- | --- | ---: | --- |
| 01-minimal | Minimum required fields | 0 | - |
| 02-full-fields | All optional fields, including a quoted metadata version | 0 | - |
| 03-uppercase | Uppercase ASCII name matching its directory | 1 | name-uppercase |
| 04-leading-hyphen | Leading hyphen | 1 | name-leading-hyphen |
| 05-trailing-hyphen | Trailing hyphen | 1 | name-trailing-hyphen |
| 06-consecutive-hyphens | Consecutive hyphens | 1 | name-consecutive-hyphens |
| 07-name-mismatch | Valid name differing from the parent directory | 1 | name-directory-mismatch |
| 08-description-missing | Required description omitted | 1 | description-missing |
| 09-description-empty | Description contains only spaces | 1 | description-empty |
| 10-description-long | Description of 1025 characters | 1 | description-length |
| 11-yaml-colon | Unquoted colon followed by a space in description | 3 | yaml-syntax |
| 12-missing-close | No frontmatter closing delimiter | 3 | frontmatter-unclosed |
| 13-metadata-value | Metadata version written as an unquoted number | 1 | metadata-value-type |
| 14-tools-list | Allowed tools as a YAML sequence | 1 | allowed-tools-type |
| 15-crlf-bom | UTF-8 BOM and CRLF throughout | 0 | - |
| 16-invalid-utf8 | Invalid byte in the description line | 3 | invalid-utf8 |
| 17-name-boolean | Unquoted `yes` resolves to a YAML boolean | 1 | name-type |
| 18-unknown-field | Unrecognized top-level field | 0 | unknown-field |
| 19-multiple-errors | Uppercase name, blank description and allowed tools sequence | 1 | name-uppercase, description-empty, allowed-tools-type |
| 20-no-frontmatter | Markdown starts with a heading | 3 | frontmatter-missing |
| 21-nonmapping | Frontmatter is a YAML sequence | 3 | frontmatter-not-mapping |
| 22-duplicate-key | Two description keys in the same mapping | 3 | yaml-duplicate-key |
| 23-metadata-key | Unquoted boolean metadata key | 1 | metadata-key-type |
| 24-compatibility-long | Compatibility of 501 characters | 1 | compatibility-length |
| 25-license-type | Numeric license value | 1 | license-type |
| 26-name-long | Name of 65 characters | 1 | name-length |
| 27-name-characters | Name with an underscore | 1 | name-characters |

`unknown-field` is a warning. Parse codes are reported in `parse_error`. Other listed codes are errors. Invalid paths preempt linting with exit 2, and a valid path without PyYAML exits 4. In a valid batch of paths, parse failures take priority over lint errors.
