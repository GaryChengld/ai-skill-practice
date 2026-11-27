The frontmatter has **three errors** in [SKILL.md](C:/Users/Gary/AppData/Local/Temp/day12-lint-qboaue9d/skill-final/fixtures/Bad-Name/SKILL.md):

- **`name`, line 2:** The name contains uppercase letters. Lowercase it and rename the parent directory to match.
- **`description`, line 3:** The description is empty. Provide a nonempty description string.
- **`allowed-tools`, line 4:** This is a YAML list, but it must be a string. Use a quoted, space-separated string such as `'Read Bash'`.

The linter reported no warnings or parsing failures. I did not modify the file.