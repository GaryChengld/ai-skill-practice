## Dependency fix plan

**Propose a temporary, parent-scoped override to `@fixture/svg-chunk@1.2.2`.** No changes or dependency checks were executed.

Ownership: `apps/preview`, managed from the workspace root with npm **10.9.2** and root `package-lock.json`. Guidance: `references/npm.md`.

The [supplied synthetic finding](C:/Workspaces/ai-skill-practice/day-07/dependency-fix-plan/tests/input-o.md) establishes:

| Package / advisory | Current → Target | Direct or transitive | Fix | Verification | Risk |
| --- | --- | --- | --- | --- | --- |
| `@fixture/svg-chunk`, FIXTURE-O-09; affected `>=1.2.0,<1.2.2` | Locked `1.2.0` → fixed `1.2.2`; installed version Unknown | Runtime transitive: preview → `@fixture/vector-loader@2.4.0` → svg-chunk | Add the root override below; regenerate root lockfile | **Proposed:** clean install, tree inspection, original scanner, malformed SVG and snapshot tests | Overrides the publisher’s exact pin; loader compatibility remains untested |

Merge into root `package.json`:

```json
{
  "overrides": {
    "@fixture/vector-loader@2.4.0": {
      "@fixture/svg-chunk": "1.2.2"
    }
  }
}
```

npm supports version-qualified parent selectors and reads overrides only from the root manifest. [npm override documentation](https://docs.npmjs.com/cli/v10/configuring-npm/package-json/#overrides)

Keep `apps/preview/package.json` at loader `2.4.0`. A parent upgrade is preferred, but none currently fixes the pin; replacing the loader requires a larger feature migration.

From the repository root, using npm 10.9.2, **proposed commands** are:

```sh
npm --version
npm install --package-lock-only
npm ci
npm ls @fixture/vector-loader @fixture/svg-chunk --all
npm explain @fixture/svg-chunk
npm test --workspace apps/preview
npm audit
```

`--package-lock-only` regenerates the lockfile without installing dependencies. [npm install documentation](https://docs.npmjs.com/cli/v10/commands/npm-install/#package-lock-only)

Verify that:

- The lockfile and installed tree resolve the affected path to `1.2.2`, with no remaining affected copies or unrelated dependency changes.
- Installation reports no unresolved dependency or peer conflicts.
- Malformed SVG tests and preview snapshots pass; API-preserving patch notes alone do not prove loader compatibility.
- The original scanner clears FIXTURE-O-09. This advisory is synthetic, so a clean public `npm audit` result cannot establish that.

**Remove the override only when** a compatible upstream loader release adopts a safe svg-chunk dependency, you upgrade to it, and regeneration **without the override** passes the same tree, scanner, and behavior checks. Publication alone is insufficient.

Open questions: loader compatibility with `1.2.2` remains unverified.

Rollback: revert root `package.json` and `package-lock.json` together; rollback restores the vulnerable `1.2.0` resolution.
