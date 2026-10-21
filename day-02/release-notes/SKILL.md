---
name: release-notes
description: Draft user-facing release notes, changelog entries, or What's New announcements for a release from commits, merged PRs, or a tag range. Use this skill when the user wants to tell users or customers what changed in a release, even if the input is a list of commits or PRs. Do not use for single commit messages, pull request descriptions for reviewers, code review, Git how-to questions, or internal engineering or activity reports.
---

# Release Notes

## Inputs

Accept a commit list, a list of merged PRs, or a range between two tags.
Confirm the target version or Unreleased section and audience when they are not clear.
Use supplied material or inspect the requested range if repository access is available.
If sources cannot be read, request them; do not invent changes, dates, or links.

## Drafting

1. Identify user-visible outcomes and combine commits or PRs describing the same change.
2. Put Breaking Changes first, followed by useful categories such as Added, Improved, and Fixed; omit empty groups.
3. Skip chore, ci, test-only, and other internal work when it has no user-visible effect. Judge the actual impact rather than the commit type alone.
4. Explain compatibility changes and required upgrade actions when supported by the input.
5. Write concise Markdown for the intended users. Include version, date, and source links only when known.
6. When updating a changelog, follow its existing format. Update Unreleased when requested; otherwise insert the new version above older versions, preserving introductory text and any Unreleased section.
7. If all changes are internal, state that no user-visible changes were identified in the supplied scope.
8. Return a draft; do not publish a release or modify files unless requested.

## Example

Input for v2.4 - add CSV export, fix login timeout, replace the configuration key timeout with requestTimeout and ignore the old key, update CI cache.

```markdown
## v2.4
### Breaking Changes
- The `timeout` configuration key is now `requestTimeout`; the old key is ignored. Rename it when you upgrade.
### Added
- Export reports as CSV.
### Fixed
- Signing in no longer fails with a timeout.
```
