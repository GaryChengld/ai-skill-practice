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

## Original Frozen Evaluation Policy

The competitor stub and the 20 labeled queries were written before these candidates. All three candidates are frozen before evaluation. Compare exact skill-routing accuracy on the 12 training queries. Select the highest-scoring version; on a tie, prefer V3, then V2, then V1 because explicit boundaries are the intended learning objective. Run only the selected version on the eight validation queries after selection. Do not revise candidates or labels in response to validation results.

## Review Revision R1 - 439 characters - Evaluated Revision

This review-driven revision replaced V3 and was used in the challenge evaluation. V1, V2, and V3 above remain the historical candidates; their scores do not apply to R1. R1 names the audience and release deliverables in its first sentence and removes the routing meta-instruction.

```text
Draft user-facing release notes, changelog entries, or What's New announcements for a shipped version from commits, merged PRs, or a tag range. Use this skill when the user wants to tell users or customers what changed in a release, even if the input is a list of commits or PRs. Do not use for single commit messages, pull request descriptions for reviewers, code review, Git how-to questions, or internal engineering or activity reports.
```

### Review Challenge Policy

The original 20 queries retain their historical wording and labels for regression checks. Six new queries H01-H06 have no defensive disclaimers and use `split: challenge`. The file has 12 train, eight validation, and six challenge queries; every group contains positive and negative cases. H cases were originally mislabeled train/validation, but all six were evaluated for every candidate; relabeling them does not change the observations.

H01 (changelog update) and H04 (GitHub Release body) are release documentation. H05 and H06 belong to the commit and PR competitors. For H02 (sprint demo) and H03 (bare tag comparison), use a conservative provisional policy: ask about the audience or output format before selecting a release-documentation skill. Their `none` label means clarify first, not that release notes could never be appropriate. This is an assumption pending user preference, not an objective universal boundary.

Freeze R1, the six queries, and these labels before the review run. Compare V2, original V3, and R1 on the same six-query challenge, with both competitors present. Do not change descriptions or labels after observing results. These review-authored challenge cases are an exploratory boundary check, not a pristine holdout for model selection; do not merge their scores with the original train/validation experiment or claim statistical superiority from this run.

## Review Revision R2 - 431 characters - Current Description

Replace "for a shipped version" with "for a release" to include draft and Unreleased changelog work. Existing routing scores apply to the evaluated versions, not R2; this wording correction was not rerun through the routing benchmark.

```text
Draft user-facing release notes, changelog entries, or What's New announcements for a release from commits, merged PRs, or a tag range. Use this skill when the user wants to tell users or customers what changed in a release, even if the input is a list of commits or PRs. Do not use for single commit messages, pull request descriptions for reviewers, code review, Git how-to questions, or internal engineering or activity reports.
```
