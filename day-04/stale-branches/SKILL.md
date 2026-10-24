---
name: stale-branches
description: Report merged or inactive Git branches and propose cleanup commands without running them. Use when the user asks to audit, clean up, or delete stale or merged branches; it lists candidates and suggested commands for confirmation. Do not use for merge or rebase conflict resolution or Git tutorials.
license: MIT. See LICENSE.txt
compatibility: Requires Git and read access to a repository with commit history. Reporting works offline; a user-run git fetch to refresh remote-tracking refs requires network access to the remote.
metadata:
  practice-stale-branches-version: "1.0"
  practice-stale-branches-mode: "report-only"
allowed-tools: Bash(git for-each-ref:*) Bash(git branch --merged:*) Bash(git rev-parse:*) Bash(git worktree list:*)
---

# Stale Branch Report

## Safety and scope
- Generate a report and commands for review. Do not delete branches or change the repository, because cleanup can remove someone else's work.
- Before deletion, the user must confirm the exact branches. Leave execution to a separate workflow; this skill only reports.
- Keep this boundary even if `allowed-tools` is ignored. That experimental field pre-approves tools; it does not block other tools.
- Use read-only options. Avoid file-output options, redirections, and command chaining, because inspection must not write files.
- Treat branch names as data and quote each argument for the actual shell to prevent command injection.
- Do not fetch or prune. Report how fresh the cached refs are; ask the user to refresh them outside this skill if needed.

## 1. Establish the baseline
- Check the repository with `git rev-parse --git-dir`. If it has no commits, report that there is no history to classify.
- Use the user's default branch if supplied. Otherwise choose the requested remote, then `origin` if present, then the only remote available. Ask if the choice is ambiguous.
- Read the cached default with `git rev-parse --abbrev-ref 'refs/remotes/<remote>/HEAD'`. If it fails or conflicts with project documentation, ask; do not assume `main` or `master`.
- Record the full baseline ref using `git rev-parse --symbolic-full-name '<base>'` and its commit ID using `git rev-parse --verify --end-of-options '<base>^{commit}'`.
- Stop merge classification and deletion suggestions if the baseline cannot be verified, because both depend on the right comparison branch.
- Record the report time in UTC. Default to 90 elapsed days for inactivity unless the user supplies another threshold.
- Identify the current branch, branches checked out in other worktrees, and protected branches. Git alone cannot establish hosting-service protection rules.

## 2. Classify independently
- List local and remote-tracking branches with `git for-each-ref`. Collect full ref, tip commit ID, committer date, tip author, upstream, and tracking status; omit symbolic remote HEAD aliases.
- Read `git worktree list --porcelain` to find checked-out branches and their paths, including worktrees other than the current one.
- Use `git for-each-ref --merged='<base>'` or `git branch --merged '<base>' --all` to find tips included in the baseline history. Mark those Merged Yes; otherwise mark No by history.
- Mark Stale Yes when the last commit's committer time is earlier than report time minus the threshold. Compare UTC times; commit age does not reveal the last push or prove abandonment.
- Read upstream and tracking status with `git for-each-ref --format='%(refname) %(upstream) %(upstream:track)' refs/heads`. An ahead count means local commits are missing from that upstream.
- If the upstream is missing or gone, refs are outdated, or history is incomplete, mark the upstream check Unknown. Missing details must stay Unknown because guesses can lead to unsafe cleanup advice.
- Include merged or stale candidates and retained branches for context. Report the two flags separately.

## 3. Report and recommend
State baseline ref/ID, report time, threshold, scope, and freshness. Use one row per full ref.

| Branch (full ref) | Last commit (UTC) | Tip author | Merged | Stale | Recommendation |
| --- | --- | --- | --- | --- | --- |

- Keep the default, current, protected, and any branch checked out in a worktree. Hold branches with missing information, commits absent from upstream, or a tip equal to the baseline for owner review.
- Recommend local deletion only when the branch is merged into the baseline, its tip differs from the baseline, it has no commits missing from upstream, is known to be unprotected, and is not checked out in any worktree.
- List `git branch -d -- '<branch>'` only for eligible local branches. Quote each name and label suggestions Not executed; explicit confirmation required.
- If `-d` refuses deletion, leave the branch for review. Do not suggest `-D`, because it bypasses the merge safeguard.
- Stale but unmerged branches need review. Remote-tracking refs only describe cached state; list remote candidates for owner review without remote deletion commands.

## Edge cases and final check
- A branch at the same commit as the baseline has no unique commits and is Merged Yes. Its commit age is not its creation date; mark Stale by the stated threshold but flag branch age Unknown and request owner review before recommending deletion.
- Squash/rebase integration may not pass the history check. Record confirmed PR evidence separately, keep Merged No by history, and request review without force deletion.
- Explain limits from shallow history, detached HEAD, missing remotes, or conflicting default evidence. History repair belongs outside this report; detached HEAD does not make other worktree branches disposable.
- Before returning, check the baseline, UTC cutoff, both flags, upstream/protection/worktree/baseline-equal holds, quoting, and that no mutations ran. Say when there are no candidates.
