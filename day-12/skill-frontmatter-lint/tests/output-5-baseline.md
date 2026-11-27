The frontmatter has a portability issue in [SKILL.md](C:/Users/Gary/AppData/Local/Temp/day12-lint-qboaue9d/baseline/fixtures/yes/SKILL.md:2): `name: yes` is parsed as the boolean `true` by PyYAML, although the skill name should be a string.

Quote the name to make it unambiguous:

```yaml
---
name: "yes"
description: Review the supplied example.
---
```

The name then matches the `yes` directory, and the description is a valid string. The repository contains no local validation rules that I could find.