## Dependency fix plan

**Upgrade `@fixture/banner-builder` from exact `3.6.0` to exact `3.6.1`, then regenerate `package-lock.json`.** This updates the direct parent to a compatible patch that requires the fixed child; no override is needed.

Ownership: storefront asset pipeline, rooted at the snapshot’s `package.json` and `package-lock.json`; npm **10.9.2**, development dependency graph.  
Guidance: `dependency-fix-plan/references/npm.md`. Advisory evidence comes from the supplied synthetic scanner finding and publisher notes.

| Package / advisory | Current → Target | Direct or transitive | Fix | Verification | Risk |
| --- | --- | --- | --- | --- | --- |
| `@fixture/template-reader`, `FIXTURE-N-17`; affected `>=1.8.0,<1.9.2` | Locked `1.9.0` → minimum fixed `1.9.2`; parent permits `>=1.9.2,<2` | Transitive through direct devDependency `@fixture/banner-builder@3.6.0`; sole affected path | Change `devDependencies["@fixture/banner-builder"]` to `"3.6.1"` in `package.json`; let npm regenerate `package-lock.json` | **Proposed:** clean install, inspect every resolved occurrence, rerun scanner, and run asset snapshot and malformed-template tests | Patch compatibility is supported by supplied notes, but template handling or generated assets could change. Build/CI exposure remains relevant despite dev-only classification. |

Proposed commands, run from the owning project root using npm 10.9.2:

```powershell
npm --version
npm install --save-dev --save-exact @fixture/banner-builder@3.6.1
git diff -- package.json package-lock.json
npm ci --include=dev
npm ls @fixture/banner-builder @fixture/template-reader --all
npm explain @fixture/template-reader
npm test
npm audit --include=dev
```

`--save-dev --save-exact` preserves the existing dependency section and exact-version policy. `npm ci` checks that the regenerated lock supports a clean installation. See [npm install documentation](https://docs.npmjs.com/cli/v10/commands/npm-install/) and [npm ci documentation](https://docs.npmjs.com/cli/v10/commands/npm-ci/).

Acceptance checks—all **Proposed**, not executed:

- The manifest and lock resolve builder `3.6.1`; every reader occurrence resolves within `>=1.9.2,<2`, with none in the affected range. Review the actual selected version rather than assuming npm chooses `1.9.2`.
- The diff contains only the intended dependency changes and necessary lock metadata.
- `npm test` passes asset snapshots and malformed-template tests; investigate unexpected snapshot changes.
- Rerun the original scanner with development dependencies included and confirm `FIXTURE-N-17` clears. [`npm audit`](https://docs.npmjs.com/cli/v10/commands/npm-audit/) provides supplementary registry checks; it cannot establish clearance of this synthetic advisory.

Open questions: Installed versions and the regenerated child resolution are **Unknown** until installation. No missing information blocks this proposal.

Rollback: Revert `package.json` and `package-lock.json` together and run `npm ci`. This restores reader `1.9.0` and reintroduces the finding.

No files were changed or dependency checks executed.
