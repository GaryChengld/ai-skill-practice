# Real Git collection check

Run on 2026-10-23 with Git 2.21.0.windows.1: `python day-04/stale-branches/tests/git-collection.py`.
The script's five setup lines create a source repository and clone with default develop. Extra setup creates a merged local branch and one unpushed commit on develop. All writes are confined to the temporary fixture; the collection phase only reads.

Observed output, excluding the random temporary-directory path:
```text
Baseline: origin/develop; full ref: refs/remotes/origin/develop; commit: 46f44d7792d45336914672806310af4be070c90d
PASS: cached HEAD resolved to develop without assuming main
PASS: dates, tip authors, and current-worktree path collected
PASS: develop is ahead 1; topic/retired-notes has no commits missing from upstream
PASS: only topic/retired-notes is included in the baseline history
PASS: refs unchanged during read-only collection; no cleanup commands executed
```

The first attempts exposed unsupported init --initial-branch and for-each-ref worktreepath options in Git 2.21. Setup now assigns HEAD explicitly; collection uses worktree list --porcelain, matching the revised skill.
This checks actual collection, not model routing, remote protection rules, or report generation. The original fresh-session smoke remains unchanged and records the initial skill version; this test supplements it.
