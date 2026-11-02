## Dependency fix plan

**Change the runtime pin from `fixture-archive-stream==1.4.0` to `fixture-archive-stream==1.4.2`, then regenerate `uv.lock`.** This is the smallest supported fix; no override or parent upgrade is needed.

Ownership: Python project represented by the snapshot’s `pyproject.toml` and scanner location `uv.lock`; CI uses uv **0.9.5** and Python **3.12**. Repository root path is unspecified.

Guidance: Applied the requested `dependency-fix-plan` skill and its `references/python.md`.

| Package / advisory | Current → Target | Direct or transitive | Fix | Verification | Risk |
| --- | --- | --- | --- | --- | --- |
| `fixture-archive-stream` / synthetic `FIXTURE-P-21`. Affected: `>=1.4.0,<1.4.2`; supplied upstream note identifies `1.4.2` as fixed. | Declared and locked: `1.4.0` → `1.4.2`. Installed version: Unknown. | Direct runtime dependency. Only supplied path: project → package; all supported platforms resolve `1.4.0`. | Edit `[project].dependencies` in `pyproject.toml`; regenerate `uv.lock`, including artifact metadata and hashes. Avoid unrelated upgrades. | **Proposed:** commands below, inspect every platform resolution, rerun CI’s runtime export and advisory scan, and execute archive tests. | Python 3.12 compatibility is supplied evidence; archive behavior still requires testing. |

After editing the pin, run these **proposed commands** with uv 0.9.5:

```powershell
uv --version
uv lock --upgrade-package fixture-archive-stream
uv lock --check
uv tree --locked --invert --package fixture-archive-stream
```

Review the diff: the package must resolve to `1.4.2` across every supported platform, with no remaining affected resolution. Targeted upgrades are documented in the [uv CLI reference](https://docs.astral.sh/uv/reference/cli/#uv-lock).

Then, in a fresh Python 3.12 CI environment:

```powershell
uv sync --locked
uv run --locked pytest
```

Confirm the archive corruption and streaming-boundary tests run and pass. Rerun CI’s existing runtime requirements export and audit using the same deployment selection. Because this advisory is synthetic, a public audit tool cannot establish that `FIXTURE-P-21` is cleared; verify it against the supplied fixture rule.

**Completed:** reviewed the snapshot, skill, and Python guidance. No dependencies were changed, installed, tested, or scanned.

**Open questions:** Exact CI export/audit commands and enabled extras/groups were not supplied; preserve their existing selection.

**Rollback:** Revert `pyproject.toml` and `uv.lock` together. Rolling back restores vulnerable `1.4.0`.
