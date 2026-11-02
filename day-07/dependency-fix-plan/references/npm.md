# JavaScript package managers

## Detect
- `package-lock.json` or `npm-shrinkwrap.json` indicates npm; shrinkwrap takes precedence when both exist.
- `pnpm-lock.yaml` indicates pnpm; `yarn.lock` indicates Yarn. Check `packageManager` and CI for the pinned manager version.
- Identify the lockfile owner and workspace root before choosing the command working directory.
- Multiple lockfile formats in one project need clarification; do not migrate managers as part of a fix.

## Inspect the tree
- npm: `npm ls <package> --all` shows installed paths; `npm explain <package>` explains why it is present.
- pnpm: `pnpm why <package>`; use recursive workspace inspection when the finding spans members.
- Yarn: `yarn why <package>`; Yarn Classic and modern Yarn have different install flags.
- An absent `node_modules` directory makes installed-tree inspection incomplete; use the lockfile pending installation.
- Check peer and optional dependencies separately, including platform-specific lock entries.

## Fix a direct dependency
- npm: `npm install <package>@<target>` updates a production declaration and lock; retain `--save-dev` for development dependencies.
- pnpm: `pnpm add <package>@<target>`; target the owning workspace with the existing filter convention.
- Modern Yarn: `yarn up <package>@<target>`; Classic: `yarn upgrade <package>@<target>`.
- Preserve the existing range policy and dependency section; installing from the wrong workspace can add a new root dependency.
- For a parent upgrade, inspect the resulting lock entries rather than assuming the parent's range selects the fixed child.

## Override a transitive dependency
- npm reads `overrides` only in the root `package.json`; workspace-local overrides do not control resolution.
- Scope the override to the affected parent when feasible. Illustrative metadata only, not a real advisory:
```json
{"overrides": {"sample-color-theme": {"sample-palette-codec": "4.0.6"}}}
```
- npm rejects an override of a direct dependency with a different spec (`EOVERRIDE`); edit that declaration instead, or reference its spec with `$<package>` where appropriate.
- pnpm uses its own root override setting, not npm's top-level `overrides`.
- Check the pinned pnpm version: current settings document `overrides` in `pnpm-workspace.yaml`; older projects may use `pnpm.overrides` in root `package.json`.
- Yarn uses root `package.json` `resolutions`; use selectors supported by the pinned Yarn generation.
- Include a removal condition for a temporary override, such as an upstream parent release adopting the fixed dependency.

## Verify
- npm: regenerate via the chosen targeted install; `npm ci` checks a clean install against its lock.
- pnpm: regenerate with pnpm; `pnpm install --frozen-lockfile` checks the resulting lock.
- Modern Yarn: `yarn install --immutable`; Classic: `yarn install --frozen-lockfile`.
- `npm audit`, `pnpm audit`, or the applicable Yarn audit command checks the relevant registry data; modern Yarn uses `yarn npm audit`.
- Exercise peer-sensitive startup and the vulnerable code path; compare all duplicate resolved versions before and after.

## Pitfalls
- `npm audit fix --force` may introduce major changes; it is not a targeted patch strategy.
- An override can violate an upstream range even when installation succeeds; peer warnings and runtime behavior still matter.
- A workspace's apparent dependency may be hoisted from the root. Local directory placement does not establish ownership.
- Lockfiles can retain multiple copies; one fixed top-level version does not clear every vulnerable occurrence.

## Sources
- [npm overrides](https://docs.npmjs.com/cli/v10/configuring-npm/package-json/#overrides)
- [pnpm versioned settings](https://pnpm.io/10.x/settings#overrides)
- [Yarn resolutions](https://yarnpkg.com/configuration/manifest#resolutions)
