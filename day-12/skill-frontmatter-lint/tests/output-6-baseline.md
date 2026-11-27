The frontmatter in [SKILL.md](C:/Users/Gary/AppData/Local/Temp/day12-lint-qboaue9d/baseline/fixtures/metadata-key/SKILL.md:1) has a portability issue: the metadata key `yes` is unquoted.

A YAML 1.1 parser can interpret `yes` as the boolean `true`, while a YAML 1.2 parser interprets it as a string. Quoting the key makes its meaning consistent across parsers. [YAML 1.2 changes](https://yaml.org/spec/1.2.2/ext/changes/)

```yaml
metadata:
  "yes": confirmed
```

The required `name` and `description` fields are present, and the name matches the directory. I didn’t find a repository-specific validator in this fixture. No files were changed.