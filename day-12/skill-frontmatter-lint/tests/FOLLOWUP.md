# Frozen follow-up behavior checks

Review each existing fixture using the same frontmatter prompt, model, and workspace layout for the skill and no-skill baseline. Use the original checklist for cases 1–3. For case 1b, also require the concrete replacement `name: bad-name` and a matching directory rename.

| Case | Fixture | ID | Response check |
| --- | --- | --- | --- |
| 4 | `13-metadata-value` | 4a | Explains that unquoted `1.0` is numeric when parsed and that metadata values must be strings. |
| 4 | `13-metadata-value` | 4b | Gives a specific replacement equivalent to `version: "1.0"`, with no unrelated finding. |
| 5 | `17-name-boolean` | 5a | Explains that PyYAML resolves unquoted `yes` as a boolean, while `name` must be a string. |
| 5 | `17-name-boolean` | 5b | Gives a specific replacement equivalent to `name: "yes"` and explains that the directory can stay `yes`. |
| 6 | `23-metadata-key` | 6a | Explains that the unquoted `yes` key is boolean and that metadata keys must be strings. |
| 6 | `23-metadata-key` | 6b | Gives a specific replacement equivalent to `"yes": confirmed`, keeping the existing value. |
