# Fresh-session smoke test

Method: 2026-10-23; fresh subagent with no inherited conversation; only SKILL.md and this fictional snapshot; no Git commands or file edits. Output below is verbatim; model/settings were inherited, not pinned.
Request: Audit these local branches for cleanup and show recommended commands; return at most 16 Markdown lines with all six rows, baseline/cutoff/freshness, and suggestions.
Snapshot: as-of 2026-10-23T12:00:00Z; full history; sole remote origin; cached origin/HEAD resolves to refs/remotes/origin/trunk at aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa; refs freshly verified then; local scope only.
Policy: only trunk and release/2026-q4 protected; all others confirmed unprotected. Only topic/quick-filter checked out, in current worktree; no other worktrees. Every upstream is origin/<same name>. Rows: branch | committer date at 12:00:00Z | tip author | baseline reachability | ahead count | evidence.
trunk | 2026-10-22 | Ari | reachable | 0 | default
topic/catalog-cache | 2026-05-10 | Bea | reachable | 0 | none
fix/receipt-tax | 2026-06-01 | Chen | not reachable | 0 | PR #42 confirms squash integration into trunk
work/refund-batch | 2026-05-20 | Dev | not reachable | 2 | none
topic/quick-filter | 2026-10-20 | Eli | not reachable | 0 | current
release/2026-q4 | 2026-06-15 | Fran | reachable | 0 | protected

## Output

Baseline: `refs/remotes/origin/trunk` at `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`; as of **2026-10-23T12:00:00Z**.
Scope: local branches only; full history; refs freshly verified at as-of. Inactivity threshold: **90 elapsed days**; stale means strictly before **2026-07-25T12:00:00Z**.
| Branch (full ref) | Last commit (UTC) | Tip author | Merged by ancestry | Stale | Recommendation |
| --- | --- | --- | --- | --- | --- |
| `refs/heads/trunk` | 2026-10-22T12:00:00Z | Ari | Yes | No | Keep: default and protected. |
| `refs/heads/topic/catalog-cache` | 2026-05-10T12:00:00Z | Bea | Yes | Yes | Eligible for local deletion: 0 ahead, unprotected, no worktree checkout. |
| `refs/heads/fix/receipt-tax` | 2026-06-01T12:00:00Z | Chen | No | Yes | Review: PR #42 confirms squash integration into trunk; 0 ahead. |
| `refs/heads/work/refund-batch` | 2026-05-20T12:00:00Z | Dev | No | Yes | Hold for review: 2 commits ahead of upstream. |
| `refs/heads/topic/quick-filter` | 2026-10-20T12:00:00Z | Eli | No | No | Keep: checked out in current worktree; 0 ahead. |
| `refs/heads/release/2026-q4` | 2026-06-15T12:00:00Z | Fran | Yes | Yes | Keep: protected; 0 ahead. |
Suggested command — **Not executed; explicit confirmation required:** `git branch -d -- 'topic/catalog-cache'`
`-d` may refuse deletion relative to upstream/HEAD; do not substitute `-D`.
Commit age is an inactivity proxy, not last-push evidence or proof of abandonment. “No” by ancestry does not prove unshipped work.
