# Differential validation

Reference: skills-ref, version 0.1.0. Exit 0 means accepted. Nonzero means rejected or unable to complete.

| Fixture | Linter exit and codes | Reference exit | Reference diagnostic on failure |
| --- | --- | ---: | --- |
| `01-minimal` | 0 | 0 | — |
| `02-full-fields` | 0 | 0 | — |
| `03-uppercase` | 1 · `name-uppercase` | 1 | Validation failed for 03-uppercase/Mixed-Case:<br>- Skill name 'Mixed-Case' must be lowercase |
| `04-leading-hyphen` | 1 · `name-leading-hyphen` | 1 | Validation failed for 04-leading-hyphen/-leading:<br>- Skill name cannot start or end with a hyphen |
| `05-trailing-hyphen` | 1 · `name-trailing-hyphen` | 1 | Validation failed for 05-trailing-hyphen/trailing-:<br>- Skill name cannot start or end with a hyphen |
| `06-consecutive-hyphens` | 1 · `name-consecutive-hyphens` | 1 | Validation failed for 06-consecutive-hyphens/double--dash:<br>- Skill name cannot contain consecutive hyphens |
| `07-name-mismatch` | 1 · `name-directory-mismatch` | 1 | Validation failed for 07-name-mismatch/pdf-tools:<br>- Directory name 'pdf-tools' must match skill name 'image-tools' |
| `08-description-missing` | 1 · `description-missing` | 1 | Validation failed for 08-description-missing/no-description:<br>- Missing required field in frontmatter: description |
| `09-description-empty` | 1 · `description-empty` | 1 | Validation failed for 09-description-empty/empty-description:<br>- Field 'description' must be a non-empty string |
| `10-description-long` | 1 · `description-length` | 1 | Validation failed for 10-description-long/long-description:<br>- Description exceeds 1024 character limit (1025 chars) |
| `11-yaml-colon` | 3 · `yaml-syntax` | 1 | Validation failed for 11-yaml-colon/yaml-colon:<br>- Invalid YAML in frontmatter: mapping values are not allowed here<br>in "<unicode string>", line 3, column 20:<br>description: Review: check markup<br>^ (line: 3) |
| `12-missing-close` | 3 · `frontmatter-unclosed` | 1 | Validation failed for 12-missing-close/unclosed:<br>- SKILL.md frontmatter not properly closed with --- |
| `13-metadata-value` | 1 · `metadata-value-type` | 0 | — |
| `14-tools-list` | 1 · `allowed-tools-type` | 0 | — |
| `15-crlf-bom` | 0 | 1 | Validation failed for 15-crlf-bom/crlf-bom:<br>- SKILL.md must start with YAML frontmatter (---) |
| `16-invalid-utf8` | 3 · `invalid-utf8` | 0 | — |
| `17-name-boolean` | 1 · `name-type` | 0 | — |
| `18-unknown-field` | 0 · `unknown-field` | 1 | Validation failed for 18-unknown-field/unknown-field:<br>- Unexpected fields in frontmatter: category. Only ['allowed-tools', 'compatibility', 'description', 'license', 'metadata', 'name'] are allowed. |
| `19-multiple-errors` | 1 · `name-uppercase`, `description-empty`, `allowed-tools-type` | 1 | Validation failed for 19-multiple-errors/Bad-Name:<br>- Invalid YAML in frontmatter: While scanning<br>in "<unicode string>", line 4, column 16:<br>allowed-tools: [Read, Bash]<br>^ (line: 4)<br>Found ugly disallowed JSONesque flow mapping (surround with ' and ' to make text appear literally)<br>in "<unicode string>", line 4, column 17:<br>allowed-tools: [Read, Bash]<br>^ (line: 4) |
| `20-no-frontmatter` | 3 · `frontmatter-missing` | 1 | Validation failed for 20-no-frontmatter/no-frontmatter:<br>- SKILL.md must start with YAML frontmatter (---) |
| `21-nonmapping` | 3 · `frontmatter-not-mapping` | 1 | Validation failed for 21-nonmapping/sequence:<br>- SKILL.md frontmatter must be a YAML mapping |
| `22-duplicate-key` | 3 · `yaml-duplicate-key` | 1 | Validation failed for 22-duplicate-key/duplicate-key:<br>- Invalid YAML in frontmatter: While parsing<br>in "<unicode string>", line 4, column 1:<br>description: Review the second e ...<br>^ (line: 4)<br>Duplicate key 'description' found<br>in "<unicode string>", line 4, column 12:<br>description: Review the second example.<br>^ (line: 4) |
| `23-metadata-key` | 1 · `metadata-key-type` | 0 | — |
| `24-compatibility-long` | 1 · `compatibility-length` | 1 | Validation failed for 24-compatibility-long/long-compatibility:<br>- Compatibility exceeds 500 character limit (501 chars) |
| `25-license-type` | 1 · `license-type` | 0 | — |
| `26-name-long` | 1 · `name-length` | 1 | Validation failed for 26-name-long/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx:<br>- Skill name 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' exceeds 64 character limit (65 chars) |
| `27-name-characters` | 1 · `name-characters` | 1 | Validation failed for 27-name-characters/under_score:<br>- Skill name 'under_score' contains invalid characters. Only letters, digits, and hyphens are allowed. |
