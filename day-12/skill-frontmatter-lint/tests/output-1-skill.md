The frontmatter in [SKILL.md](C:/Users/Gary/AppData/Local/Temp/day12-lint-qboaue9d/skill-followup/fixtures/Bad-Name/SKILL.md) has three errors:

- **`name`, line 2:** The name must use lowercase letters. Change it to `name: bad-name` and rename the parent directory to `bad-name`.
- **`description`, line 3:** The description is empty. Provide a nonempty description string.
- **`allowed-tools`, line 4:** This must be a YAML string, but it is a list. Use a quoted, space-separated string such as `'Read Bash'`.

The linter reported no warnings or parse failures. No files were changed.