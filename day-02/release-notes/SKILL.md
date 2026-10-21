---
name: release-notes
description: Write summaries of software changes from commits, diffs, or pull requests. Use this skill when the user asks for release notes, a customer changelog, a What's New announcement, a release digest, or an upgrade bulletin for a shipped version. Do not use for individual commit messages, PR titles or descriptions for reviewers, code review, Git instructions, or internal engineering and activity reports. Commits and PRs may be source material; route by the requested deliverable.
---

# Release Notes

## Inputs

Accept a commit list, a list of merged PRs, or a range between two tags.
Confirm the target version and audience when they are not clear.
Use supplied material or inspect the requested range if repository access is available.
If sources cannot be read, request them; do not invent changes, dates, or links.

## Drafting

1. Identify user-visible outcomes and combine commits or PRs describing the same change.
2. Group by useful categories such as Added, Improved, Fixed, and Breaking Changes; omit empty groups.
3. Skip chore, ci, test-only, and other internal work when it has no user-visible effect. Judge the actual impact rather than the commit type alone.
4. Explain compatibility changes and required upgrade actions when supported by the input.
5. Write concise Markdown for the intended users. Include version, date, and source links only when known.
6. If all changes are internal, state that no user-visible changes were identified in the supplied scope.
7. Return a draft; do not publish a release or modify files unless requested.

## Example

Input for v2.4 - add CSV export, fix login timeout, update CI cache.

```markdown
## v2.4
### Added
- Export reports as CSV.
### Fixed
- Signing in no longer fails with a timeout.
```
