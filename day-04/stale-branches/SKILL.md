---
name: stale-branches
description: Report merged or inactive Git branches and propose cleanup commands without deleting branches. Use when the user asks to audit stale branches, identify merged branches, or plan branch cleanup. Do not use for merge or rebase conflict resolution, Git tutorials, or executing branch deletion.
license: MIT. See LICENSE.txt
compatibility: Requires Git and read access to a repository with commit history. Reporting works offline; a user-run git fetch to refresh remote-tracking refs requires network access to the remote.
metadata:
  practice-stale-branches-version: "1.0"
  practice-stale-branches-mode: "report-only"
allowed-tools: Bash(git for-each-ref:*) Bash(git log:*) Bash(git branch --merged:*) Bash(git rev-parse:*)
---

# Stale Branch Report

## Safety and scope
- Produce a report and suggested commands only. Do not execute deletion, force operations, pushes, resets, or other repository mutations, because this skill cannot establish that removing someone's work is intended.
- Explicit user confirmation of the exact refs is required before deletion in a separate execution workflow; even confirmation does not turn this reporting skill into a deletion tool.
- Enforce these rules independently of `allowed-tools`: it is experimental pre-approval, not a restriction, and clients may ignore it. Unlisted read-only tools can follow normal client permissions.
- Use read-only options only, without output-file options, redirections, or command chaining. Treat ref names as data and quote arguments for the actual shell to prevent command injection.
- Use existing refs without fetching or pruning. Record snapshot freshness; if freshness is unknown, qualify conclusions and ask the user to refresh refs outside this skill before relying on remote state.

## 1. Establish the baseline
- Verify the repository with `git rev-parse --git-dir`; an unborn repository has no commit history to classify.
- Use the user's explicit default branch when supplied. Otherwise choose the requested remote, then `origin` if present, then the sole remote; ask if multiple other remotes remain.
- Read that remote's cached HEAD using `git symbolic-ref --quiet --short refs/remotes/<remote>/HEAD`. If missing or inconsistent with project documentation, ask for the default rather than assuming `main` or `master`.
- Resolve the baseline to a commit with `git rev-parse --verify --end-of-options '<base>^{commit}'`; record its full ref and commit ID. Without a verified baseline, stop merge classification and deletion suggestions.
- Record the as-of timestamp in UTC and the inactivity threshold, defaulting to 90 elapsed days. Determine current HEAD, linked worktrees, and known protected branches; protection cannot be inferred from Git alone.

## 2. Classify independently
- Inventory local heads and remote-tracking branches with `git for-each-ref`, including full ref, tip commit ID, committer date, tip author, upstream, tracking status, and worktree path. Exclude symbolic remote HEAD aliases.
- Set merged to Yes only when the tip is reachable from the baseline, using `git for-each-ref --merged='<base>'` or `git branch --merged '<base>' --all`. Otherwise label No by ancestry, not proof of unshipped work.
- Set stale to Yes when the tip committer timestamp is strictly earlier than as-of minus the threshold; compare UTC instants. Commit age is a proxy for inactivity, not a branch's last push date or proof of abandonment.
- Check local commits absent from the configured upstream with `git log --oneline '<upstream>..<branch>' --`; any results mean ahead of that upstream. A missing upstream, stale refs, or incomplete history makes this safety check Unknown.
- Include merged OR stale branches as candidates, plus retained branches for context. Do not fabricate missing dates, authors, protection, or upstream status; use Unknown and explain the consequence.

## 3. Report and recommend
State baseline ref/ID, as-of time, threshold, scope, and freshness. Use one row per ref; distinguish local heads from remote-tracking refs.

| Branch (full ref) | Last commit (UTC) | Tip author | Merged | Stale | Recommendation |
| --- | --- | --- | --- | --- | --- |

- Keep the default, current, protected, and any worktree-checked-out branch. Hold branches ahead of upstream, with unknown upstream safety, or unknown protection for review, even when old or merged.
- Recommend local deletion only for ancestry-merged branches with verified upstream safety, known unprotected status, and no checkout in any worktree. Stale unmerged branches need review, not automatic deletion.
- After the table, list individually quoted `git branch -d -- '<branch>'` suggestions only for eligible local branches, marked Not executed; explicit confirmation required. Explain that `-d` can refuse deletion relative to its upstream/HEAD; do not substitute `-D`.
- Remote-tracking refs are cached observations, not server branches. List remote cleanup candidates for owner/protection review without executable remote deletion commands, because local evidence cannot verify server permissions or current state.

## Edge cases and final check
- Squash/rebase merges can fail ancestry checks. Report confirmed PR evidence separately as integrated by squash/rebase; retain No by ancestry and request review without a force-delete suggestion.
- Shallow history, detached HEAD, missing remotes, gone upstreams, or conflicting default-branch evidence require explicit limitations; fetch/history repair belongs outside this report. Keep other worktree checkouts protected even when HEAD is detached.
- Before returning, check baseline evidence, UTC cutoff, both independent flags, upstream/protection/worktree holds, shell quoting, and the absence of executed mutations. A no-candidate report should say so rather than invent cleanup work.
