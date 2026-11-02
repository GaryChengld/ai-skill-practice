---
name: dependency-fix-plan
description: Plan minimal fixes for vulnerable dependencies from scanner or advisory findings (CVE/GHSA alerts, Dependabot, npm audit, pip-audit), using manifests, lockfiles, and dependency paths. Use when the user asks what to change after a dependency vulnerability alert or needs a direct or transitive remediation plan. Do not use for routine feature upgrades, general dependency modernization, or writing commit messages.
---

# Dependency Fix Plan

## Scope and evidence
- Produce a plan and proposed commands. Apply changes only when requested; a scanner alert alone does not authorize installation or lockfile changes.
- Record the advisory source, affected range, resolved version, and fixed range. Cite user-supplied advisory data as the source; when none is supplied, verify against the advisory. Use Unknown for missing facts, because guessed versions can leave the vulnerability present.
- Distinguish declared ranges, locked versions, and installed versions. Label checks Proposed or Executed with evidence; a suggested command is not a successful verification.

## Select one domain
Read only the reference for the ecosystem that owns the vulnerable package. A repository that also contains other manifests does not need their references.
1. Locate the finding's manifest/lockfile path and dependency chain; match it to the owning project or workspace. Package names or the repository's dominant language alone are insufficient.
2. Use the table only after ownership is established. Read the selected file directly; do not glob or concatenate the references directory.

| Ownership evidence in the affected project | Reference to read |
| --- | --- |
| `package.json` with `package-lock.json`, `npm-shrinkwrap.json`, `pnpm-lock.yaml`, or `yarn.lock` | `references/npm.md` |
| `pyproject.toml` with Python dependency declarations or `uv.lock`, or `requirements*.txt` / `Pipfile.lock` | `references/python.md` |
| `pom.xml`, `build.gradle`, or `build.gradle.kts`; optionally `gradle.lockfile` | `references/jvm.md` |
| Other ecosystems, including `go.mod` / `go.sum` or `Cargo.toml` / `Cargo.lock` | None |

- If a lockfile is absent, use manifest dependency declarations plus scanner identity; leave the manager Unknown if its identity is unclear.
- If ownership is ambiguous, ask for the finding's file path or dependency chain before reading a domain file; do not load several files to guess.
- For an unsupported ecosystem, read no references. Follow the common workflow, identify missing ecosystem guidance in the output, and verify native mechanisms against official documentation before proposing specific commands.
- For separate findings owned by different ecosystems, handle each independently and load only its relevant reference.

## Common workflow
1. Confirm package identity, current resolution, affected scope, and the smallest supported fixed target; note runtime, development, and platform conditions.
2. Determine direct or transitive status from the manifest and dependency chain. For transitive packages, identify the direct parent and every affected path.
3. Prefer upgrading the direct dependency (the package itself or its direct parent) to a compatible release that resolves the finding. If that cannot work, propose a scoped transitive override or constraint with compatibility checks. If neither is supported, defer with a reason, mitigation, owner, and review date; do not silently suppress the alert.
4. Name the exact files and ranges to change, including manager-generated lock changes. Explain why the candidate is smaller than the alternatives and what evidence is still needed.
5. Propose regeneration with the existing manager, a clean reproducible install, resolved-tree inspection, the relevant advisory scan, and focused behavior tests. Confirm every affected path is fixed, then record residual risks and rollback files.

## Output template
```markdown
## Dependency fix plan
Ownership: <project path, manifest/lockfile evidence, ecosystem and manager>
Guidance: <selected reference, or no dedicated guidance for this ecosystem>
| Package / advisory | Current → Target | Direct or transitive | Fix | Verification | Risk |
| --- | --- | --- | --- | --- | --- |
| <identity and evidence> | <resolved → smallest supported fix, or Unknown> | <status and parent paths> | <files and proposed edits, or justified deferral> | <commands, assertions, Proposed/Executed> | <compatibility and remaining exposure> |
Open questions: <missing evidence, decisions, or None>
Rollback: <manifest/lock changes to revert together; exposure after rollback>
```

## Before returning
- [ ] Ownership is supported by a finding path and dependency evidence; unrelated domain files were not read, and unsupported ecosystems use none.
- [ ] Package identity, affected/fixed versions, all paths, and direct/transitive status are evidenced or Unknown.
- [ ] The direct-upgrade preference, override compatibility, or deferral reason is explicit; unrelated upgrades are excluded.
- [ ] All six table cells are present; verification distinguishes planned checks from observed results, and risks include rollback exposure.
