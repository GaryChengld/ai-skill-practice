## Dependency fix plan

Upgrade **`fixture-index-client==2.8.0` to `==2.8.1`** in `services/indexer/pyproject.toml`, then regenerate `services/indexer/uv.lock` targeting **`fixture-linkdecode==2.3.4`**.

Ownership: `services/indexer/uv.lock` identifies the Python indexer service, using uv **0.9.5** and Python **3.12**.  
Guidance: `references/python.md` from the requested skill. Advisory evidence is the supplied synthetic fixture.

| Package / advisory | Current → Target | Direct or transitive | Fix | Verification | Risk |
| --- | --- | --- | --- | --- | --- |
| `fixture-linkdecode` / `FIXTURE-M-44`; affected `>=2.3.0,<2.3.4` | Locked `2.3.1` → `2.3.4`; installed version Unknown | Runtime transitive; one path: `fixture-index-client 2.8.0` → `fixture-linkdecode 2.3.1` | Change the direct client pin to `2.8.1`; regenerate the service lockfile with uv | **Proposed:** clean locked install, dependency-tree and installed-version checks, original scanner, link-normalization tests | Publisher describes the parent patch as compatible; regression tests must confirm behavior |

The parent patch requires `fixture-linkdecode>=2.3.4,<3`, preventing future resolution into the affected range. Although the existing parent permits a lock-only fix, the patch establishes that safe minimum without an override or broader upgrades.

**Proposed commands**, using uv 0.9.5 from `services/indexer`, after editing the client pin:

```powershell
uv --version
uv lock --upgrade-package fixture-index-client --upgrade-package "fixture-linkdecode==2.3.4"
uv lock --check
```

Review the generated diff for the two intended version changes and necessary metadata/hashes. uv supports targeting individual package versions during locking. [uv locking documentation](https://docs.astral.sh/uv/concepts/projects/sync/#upgrading-locked-package-versions)

In a fresh CI checkout/environment on the deployment platform:

```powershell
uv sync --locked --python 3.12
uv tree --locked --invert --package fixture-linkdecode
uv run --locked python -c "from importlib.metadata import version; print(version('fixture-index-client')); print(version('fixture-linkdecode'))"
uv run --locked pytest
```

Use the service’s deployment groups/extras for installation and scanning; include its test dependencies for pytest. `--locked` makes verification fail if the manifest requires lockfile changes. [uv verification behavior](https://docs.astral.sh/uv/concepts/projects/sync/#automatic-lock-and-sync)

Accept the fix when:

- The runtime path resolves to client **2.8.1** → decoder **2.3.4**, including the installed environment.
- The original scanner, using the synthetic advisory data, reports no `FIXTURE-M-44` on the service’s runtime graph.
- Link-normalization regression tests pass.

**Open questions:** Deployment platform, enabled groups/extras, and original scanner invocation are unspecified. No installation, edits, or verification checks were executed.

**Rollback:** Revert `services/indexer/pyproject.toml` and `services/indexer/uv.lock` together. This restores the vulnerable resolution and reopens the finding.
