Assuming the removal is intentional API maintenance:

```text
chore(config)!: remove parse options from parseConfig

BREAKING CHANGE: parseConfig no longer accepts or forwards parse
options. Callers must remove the second argument.
```