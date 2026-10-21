# Description Candidates

All counts are Unicode characters in the description value, excluding the Markdown code fence and final newline. Each value is a single line.

## V1 - 74 characters

Capability only.

```text
Write summaries of software changes from commits, diffs, or pull requests.
```

## V2 - 240 characters

Adds explicit activation language and user-intent keywords.

```text
Write summaries of software changes from commits, diffs, or pull requests. Use this skill when the user asks for release notes, a customer changelog, a What's New announcement, a release digest, or an upgrade bulletin for a shipped version.
```

## V3 - 477 characters

Adds exclusions and distinguishes source material from the requested deliverable.

```text
Write summaries of software changes from commits, diffs, or pull requests. Use this skill when the user asks for release notes, a customer changelog, a What's New announcement, a release digest, or an upgrade bulletin for a shipped version. Do not use for individual commit messages, PR titles or descriptions for reviewers, code review, Git instructions, or internal engineering and activity reports. Commits and PRs may be source material; route by the requested deliverable.
```

## Frozen Evaluation Policy

The competitor stub and the 20 labeled queries were written before these candidates. All three candidates are frozen before evaluation. Compare exact skill-routing accuracy on the 12 training queries. Select the highest-scoring version; on a tie, prefer V3, then V2, then V1 because explicit boundaries are the intended learning objective. Run only the selected version on the eight validation queries after selection. Do not revise candidates or labels in response to validation results.
