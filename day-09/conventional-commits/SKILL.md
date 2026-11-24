---
name: conventional-commits
description: Draft Conventional Commits messages when asked what a commit should say, using a git diff, staged changes, or summary. Excludes PR descriptions, changelogs, and release notes.
---

# Conventional Commits Writer

Use the supplied diff or change summary. Otherwise inspect the staged diff (`git diff --cached`), consulting the unstaged diff (`git diff`) only when nothing is staged. Keep those change sets separate and disclose when the proposal is based on unstaged changes. Draft the message in a copyable code block. Create a commit only when explicitly asked.

- Choose the type by purpose: `feat` for a new capability, `fix` for a defect, `docs` for documentation, `refactor` for behavior-preserving restructuring, `perf` for efficiency, `test` for tests, `build` for tooling or dependencies, `ci` for CI, `style` for formatting, or `chore` for other maintenance.
- Use `type(scope): subject`, omitting scope when no single component fits. Match the repository's language and conventions. Default to a lowercase type and scope and an English imperative subject without a final period. Aim for 50 characters when clear. Separate any body and footers with blank lines. Use the body to explain why or report material consequences.
- Mark a confirmed incompatible change with `!` before the colon, an uppercase `BREAKING CHANGE:` footer, or both. Explain the compatibility impact and known migration steps. Ground the message in the changes and include issue references only when supported. Summarize sensitive changes without exposing contents.
- For unrelated purposes, recommend separate commits and give a proposed message for each. If one commit is required, use the dominant purpose for the header and cover the other significant changes in the body.
- If the selected diff is empty, say there is no basis for a message and ask for a diff or summary. For ambiguous intent, state the uncertainty or ask one focused question if classification depends on the answer.
