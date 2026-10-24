---
name: conventional-commits
description: Write Conventional Commits messages from git diffs, staged changes, or a description of the change. Use when the user asks for a commit message, how to word or describe a commit, or wants a diff summarized as a commit. Do not use for pull request descriptions, changelogs, or release notes.
---

# Conventional Commits Writer

Generate an accurate, concise Conventional Commits message from the changes the user intends to commit. Do not create a commit unless explicitly asked to do so.

## Workflow

1. Identify the intended change set. Prefer staged changes (`git diff --cached`) when staged files exist; otherwise inspect unstaged changes (`git diff`). If the user provides a diff or a change summary, use that input instead. Never silently combine staged and unstaged changes.
2. Review changed file paths and relevant hunks. Infer the observable purpose and user-facing impact; do not guess behavior that the diff does not establish.
3. Select the most appropriate type from the list below. Classify by the purpose of the change, not merely the filenames.
4. Add an optional scope naming the affected component or module (for example, `auth`, `api`, or `docs`). Omit scope when no single meaningful component applies.
5. Write a concise subject that describes the outcome. Add a body when context or reasoning is necessary, and add footers for breaking changes or issue references when supported by evidence.
6. Validate the message against the format and rules below. Return the proposed message in a copyable code block, with a short explanation only when useful.

## Allowed types

- `feat`: Add a new feature or externally observable capability.
- `fix`: Correct a defect or unintended behavior.
- `docs`: Change documentation only.
- `refactor`: Restructure code without changing intended behavior.
- `perf`: Improve runtime or resource efficiency.
- `test`: Add or modify tests without changing production behavior.
- `build`: Change build tooling, packaging, or dependencies.
- `ci`: Change continuous integration workflows or configuration.
- `style`: Change formatting or whitespace without behavioral changes.
- `chore`: Perform routine maintenance not better described by another type.

## Message format

Use this structure:

```text
<type>(<optional-scope>)<optional-!>: <subject>

<optional body>

<optional footer(s)>
```

- Prefer lowercase for type and scope unless repository conventions differ; the specification treats them as case-insensitive.
- Write `BREAKING CHANGE:` in uppercase (`BREAKING-CHANGE:` is an accepted synonym).
- Match the language of the repository's existing commit history; default to English. Use an imperative verb such as `add`, `fix`, or `remove` when writing in English.
- Keep the subject at or below 50 characters when practical (a common git convention, not part of the Conventional Commits spec); never sacrifice clarity to meet the target.
- For English subjects, prefer a lowercase first word unless it is a proper noun or identifier, or repository conventions differ.
- Do not end the subject with a period.
- Describe what changed, not vague activity such as `update code` or `fix stuff`.
- Separate the header, body, and footer sections with blank lines when present.
- Explain motivation and notable consequences in the body instead of repeating the subject.
- Do not invent issue numbers, breaking impacts, or implementation details.

## Examples

### Example 1: Bug fix

Diff summary: Fix token refresh logic so expired access tokens no longer cause repeated unauthorized requests.

```text
fix(auth): refresh expired access tokens
```

### Example 2: New feature

Diff summary: Add CSV export to the reports module and cover the export flow with tests.

```text
feat(reports): add CSV export

Allow users to download report data for offline analysis.
Include tests for the export flow.
```

### Example 3: Breaking change

Diff summary: Remove the deprecated `legacyMode` option from public configuration.

```text
feat(config)!: remove legacyMode option

BREAKING CHANGE: Configurations using legacyMode must remove
that option before upgrading.
```

## Edge cases

- **Breaking changes:** Use `!` before the colon, a `BREAKING CHANGE:` footer, or both. Explain the compatibility impact and migration steps when known. Do not mark an internal-only change as breaking without evidence.
- **Mixed purposes:** If unrelated features, fixes, or maintenance changes are mixed together, recommend splitting them into separate commits and propose a message for each logical change. If a single commit is required, summarize the dominant purpose and mention other significant changes in the body.
- **Empty diff:** If there are no relevant changes, say that no commit message can be grounded in the available diff. Ask for a diff or a description; do not invent a commit.
- **Only unstaged changes:** State that the proposed message is based on unstaged changes and that those changes have not been staged.
- **Ambiguous intent:** Ask one concise question when the change purpose cannot be inferred reliably; otherwise explicitly state uncertainty.
- **Unrelated or sensitive files:** Avoid exposing secrets or reproducing sensitive diff contents. Describe their purpose at a high level when possible.

## Final check

Before responding, verify that the chosen type reflects the actual change, the scope is optional and meaningful, the subject follows the style rules, and any breaking-change marker accurately reflects compatibility impact.
