The frontmatter in [SKILL.md](C:/Users/Gary/AppData/Local/Temp/day12-lint-qboaue9d/baseline/fixtures/Bad-Name/SKILL.md:1) is valid YAML, but it has three issues under the [Agent Skills specification](https://agentskills.io/specification):

- `name: Bad-Name` contains uppercase letters. Use a lowercase name such as `bad-name` and rename the parent directory to match it.
- `description: ""` is empty. It must describe what the skill does and when to use it.
- `allowed-tools: [Read, Bash]` is a YAML list. The specification calls for a space-separated string: `allowed-tools: Read Bash`. Support for this optional field is experimental.

I did not modify the fixture.