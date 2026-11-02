# Python dependency managers

## Detect
- `uv.lock` with `pyproject.toml` selects uv; requirements files plus the install command identify a pip workflow.
- A `pyproject.toml` alone can contain build metadata without runtime dependencies. Inspect `[project]`, tool configuration, and CI.
- A Poetry or Pipenv lock establishes Python ownership but not a uv/pip workflow; use that manager's documented locking process.
- Record the Python version, enabled extras/groups, and deployment platform used by resolution.

## Inspect the tree
- uv: `uv tree --locked --invert --package <package>` shows reverse paths without silently refreshing an out-of-date lock.
- pip: `python -m pip show <package>` gives installed version and reverse dependents; `python -m pip inspect` provides structured environment metadata.
- Reconstruct paths from declared requirements and installed metadata; `pip freeze` alone does not establish which dependencies are direct.
- A universal uv lock may contain multiple versions under disjoint Python or platform markers; match the scanner's environment.

## Fix a direct dependency
- uv: edit the owning `[project].dependencies` or dependency group, then use `uv lock --upgrade-package <package>`.
- `uv add '<package><specifier>'` is an alternative when its defaults match the repository's declaration style.
- pip: update the maintained requirements input, then regenerate its compiled/pinned output using the repository's existing compiler.
- If the repository maintains only a pinned requirements file, change that pin through its documented workflow.
- Regenerate hashes when a requirements workflow uses hash checking; old hashes cannot authenticate new distributions.

## Override a transitive dependency
- pip constraints restrict acceptable versions but neither install a package nor replace a conflicting parent requirement.
- Put the limit in a constraints file and apply it to the actual install, for example `python -m pip install -r requirements.txt -c constraints.txt`.
- An already incompatible exact pin in `requirements.txt` still causes resolution failure; regenerate that pin rather than claiming the constraint fixes it.
- uv reads these settings from the workspace-root `pyproject.toml` for project resolution:
```toml
[tool.uv]
constraint-dependencies = ["sample-font-metrics>=1.7.3,<2"]
```
- This illustrative font-metrics bound only intersects existing requirements; it cannot widen their allowed versions.
- `override-dependencies = ["sample-font-metrics==2.0.1"]` replaces requirements instead. It can bypass an incompatible parent cap and therefore needs explicit API compatibility evidence.
- The two snippets describe alternatives, not settings to combine. Neither global setting requests installation on its own.
- A pip constraints file is not an uv override file; `uv pip` has separate constraints and override options.

## Verify
- uv: `uv lock --check`, then `uv sync --locked` for the selected deployment groups and extras.
- Export the deployment selection to requirements for `pip-audit`, or audit the resulting environment using its existing scanner.
- pip: create a clean environment, install the maintained requirements with the constraints, then run `python -m pip check`.
- `pip-audit -r <resolved-requirements.txt>` checks requirements; `pip-audit` checks the installed environment.
- Audit the exported/resolved selection, not just a constraints file. Record exceptions for packages the scanner cannot resolve.

## Pitfalls
- A constraints file unused by CI or deployment changes nothing there; trace every consuming install command.
- Successful resolution is not API compatibility, especially after uv overrides replace upstream requirements.
- Build-system requirements and runtime requirements may need separate handling; identify which graph the scanner found.
- Preserve environment markers and hashes so a local fix does not break another supported interpreter or platform.

## Sources
- [pip constraints](https://pip.pypa.io/en/stable/user_guide/#constraints-files)
- [uv settings](https://docs.astral.sh/uv/reference/settings/#constraint-dependencies) and [overrides](https://docs.astral.sh/uv/concepts/resolution/#dependency-overrides)
- [uv commands](https://docs.astral.sh/uv/reference/cli/#uv-tree)
- [pip-audit](https://pypi.org/project/pip-audit/)
