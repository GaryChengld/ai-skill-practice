# Invalid frontmatter examples

Each fragment replaces the valid skill's frontmatter; errors refer to the Agent Skills specification, not every client's permissive parser.

## Non-string metadata
```yaml
---
name: stale-branches
description: Report stale Git branches when asked for cleanup advice.
metadata:
  practice-stale-branches-version: 1.0
  practice-stale-branches-enabled: true
---
```
Both values are non-strings; quote them, because metadata requires string keys and string values.

## Oversized compatibility
```yaml
---
name: stale-branches
description: Report stale Git branches when asked for cleanup advice.
compatibility: <imagine a literal 501-character ASCII string here>
---
```
The displayed placeholder is not itself oversized; replacing it with the described 501-character literal violates the 500-character maximum.

## List instead of string
```yaml
---
name: stale-branches
description: Report stale Git branches when asked for cleanup advice.
allowed-tools:
  - Bash(git log:*)
  - Bash(git rev-parse:*)
---
```
A YAML list violates the standard's space-separated string type, even though Claude Code currently accepts lists as an extension.

## Illegal name
```yaml
---
name: Stale_Branches
description: Report stale Git branches when asked for cleanup advice.
---
```
Uppercase letters and the underscore violate the name grammar; the name also fails to match the stale-branches directory.

## Valid spelling, wrong directory
```yaml
---
name: branch-audit
description: Report stale Git branches when asked for cleanup advice.
---
```
The name is syntactically valid but invalid in a directory named stale-branches because the two must match.

## Legal syntax, unsafe scope
```yaml
---
name: stale-branches
description: Report stale Git branches when asked for cleanup advice.
allowed-tools: Bash(git:*)
---
```
This is not a schema error, but fails this skill's safety requirements by pre-approving all Git commands, including deletion.
