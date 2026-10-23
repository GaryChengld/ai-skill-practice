"""Exercise read-only Git collection against a disposable local repository."""

from pathlib import Path
import subprocess
import tempfile


def git(*args):
    result = subprocess.run(["git", *map(str, args)], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"Git failed: {args}\n{result.stderr.strip()}")
    return result.stdout.strip()


# Five setup lines. Mutations here create the fixture; they are not skill actions.
root = Path(tempfile.mkdtemp(prefix="stale-branches-collection-"))
git("init", "--quiet", root / "source")
git("-C", root / "source", "symbolic-ref", "HEAD", "refs/heads/develop")
git("-C", root / "source", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "--quiet", "--allow-empty", "-m", "Seed")
git("clone", "--quiet", root / "source", root / "repo")

repo = root / "repo"
# Add a local commit after cloning to make upstream tracking observable.
git("-C", repo, "branch", "--track", "topic/retired-notes", "origin/develop")
git("-C", repo, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "--quiet", "--allow-empty", "-m", "Local work")


def collect(*args):
    return git("-C", repo, *args)


# Snapshot refs before collection, so accidental changes are detectable.
before = collect("for-each-ref", "--format=%(refname) %(objectname) %(symref)")
assert collect("rev-parse", "--git-dir") == ".git"
base = collect("rev-parse", "--abbrev-ref", "refs/remotes/origin/HEAD")
full_base = collect("rev-parse", "--symbolic-full-name", base)
base_id = collect("rev-parse", "--verify", "--end-of-options", f"{base}^{{commit}}")
current = collect("rev-parse", "--abbrev-ref", "HEAD")
assert base == "origin/develop"
assert full_base == "refs/remotes/origin/develop"
assert base_id == collect("rev-parse", "--verify", "refs/remotes/origin/develop^{commit}")
assert current == "develop"

fmt = "%(refname)|%(committerdate:iso-strict)|%(authorname)|%(upstream)|%(upstream:track)"
rows = [line.split("|") for line in collect("for-each-ref", f"--format={fmt}", "refs/heads").splitlines()]
by_ref = {row[0]: row for row in rows}
assert len(rows) == 2
assert all(row[1] and row[2] == "Fixture" for row in rows)
assert by_ref["refs/heads/develop"][3:5] == [full_base, "[ahead 1]"]
assert by_ref["refs/heads/topic/retired-notes"][3:5] == [full_base, ""]
worktrees = collect("worktree", "list", "--porcelain")
assert "branch refs/heads/develop" in worktrees.splitlines()
assert "branch refs/heads/topic/retired-notes" not in worktrees.splitlines()
assert any(line.startswith("worktree ") for line in worktrees.splitlines())
merged = collect("for-each-ref", f"--merged={base}", "--format=%(refname)", "refs/heads").splitlines()
assert merged == ["refs/heads/topic/retired-notes"]
assert before == collect("for-each-ref", "--format=%(refname) %(objectname) %(symref)")

print(f"Fixture: {root}")
print(f"Baseline: {base}; full ref: {full_base}; commit: {base_id}")
print("PASS: cached HEAD resolved to develop without assuming main")
print("PASS: dates, tip authors, and current-worktree path collected")
print("PASS: develop is ahead 1; topic/retired-notes has no commits missing from upstream")
print("PASS: only topic/retired-notes is included in the baseline history")
print("PASS: refs unchanged during read-only collection; no cleanup commands executed")
