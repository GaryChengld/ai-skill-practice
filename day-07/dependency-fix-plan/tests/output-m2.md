## Dependency fix plan

Ownership: **Unknown.** Both `web` (npm) and `jobs` (Python/uv) have active lockfiles. The finding does not identify which project owns the package.

Guidance: Applied `dependency-fix-plan`; no ecosystem reference selected until ownership is established.

| Package / advisory | Current → Target | Direct or transitive | Fix | Verification | Risk |
| --- | --- | --- | --- | --- | --- |
| `fixture-payload-codec` / `FIXTURE-M2-12`. Supplied synthetic affected range: `>=4.2.0,<4.2.3`. | Scanner reports `4.2.0` → supplied remediation `4.2.3`. Declared, locked, and installed versions remain Unknown. | Unknown; no dependency chain supplied. | Defer file edits until ownership is known. Then prefer upgrading the package if direct, or its direct parent if transitive, and regenerate the owning lockfile. | **Proposed:** inspect declarations and every dependency path; regenerate using the existing manager; perform a clean install, resolved-tree inspection, advisory scan, and focused tests. No verification executed. | Editing either project now could miss the vulnerable path. Compatibility and parent upgrade requirements remain Unknown. |

Open questions: **Please provide the scanner’s manifest/lockfile path or dependency chain**, plus the corresponding declaration and lockfile entry. The package name alone cannot establish ownership.

Rollback: Revert the owning manifest and generated lockfile together; restoring affected version `4.2.0` would restore the reported exposure.
