# Optional field choices

Checked against the linked official documentation on 2026-10-23. This is documentation review, not a live cross-client compatibility test.

| Field | Value and reason | Claude Code | GitHub Copilot CLI | If ignored |
| --- | --- | --- | --- | --- |
| `license` | `MIT. See LICENSE.txt`; short identifier with complete bundled terms. | Accepts this standard field; it does not grant execution permission. | Explicitly documents this optional field as a license description. | Discovery loses the license hint; LICENSE.txt still supplies the terms. Reporting behavior is unchanged. |
| `compatibility` | Git, repository history/read access; offline report, network only for a user-run refresh. These are actual environmental dependencies. | Accepts the standard field; do not treat it as dependency installation or enforcement. | The cited field summary does not document it; do not rely on enforcement or assume parser behavior. | Prerequisites may be less visible. Body checks still stop classification without a baseline/history; no automatic fetch is authorized. |
| `metadata` | `practice-stale-branches-version: "1.0"` and `practice-stale-branches-mode: "report-only"`; distinctive keys and string values avoid collisions and YAML number coercion. | Accepts the standard mapping; these custom keys are informational, not policy. | The cited field summary does not document custom metadata; consumers may ignore it. | Version/mode hints disappear; body safety and report behavior remain the same. |
| `allowed-tools` | One space-separated string with four narrow Git read prefixes; no generic shell or `Bash(git:*)` grant. Claude-specific syntax is an intentional portability tradeoff. | Matching tools are pre-approved; other tools remain callable under ordinary permissions. Managed policies can override grants. | Documents pre-approval and warns about broad `shell`/`bash` grants; the Claude `Bash(...)` patterns are not documented equivalents. Expect no portable pre-approval from this value. | Ordinary permissions apply; report-only instructions remain binding. Prefixes are not a sandbox: body rules also prohibit write options and mutations. |

None of these optional fields is necessary to produce the report; only the body defines its behavior and deletion boundary. `compatibility` is useful discovery information, while `metadata` and client-specific `allowed-tools` can be removed without changing the intended report. Keep the bundled license terms for redistribution even if the frontmatter license hint is removed.

## Sources
- [Agent Skills specification](https://agentskills.io/specification): field types, limits, and experimental pre-approval semantics.
- [Claude Code skills](https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill) and [permissions](https://code.claude.com/docs/en/permissions): grants, ordinary permissions, and command patterns.
- [Copilot CLI skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills): the basic field summary lists name, description, license; the later script section also documents allowed-tools and warns against broad shell pre-approval.
- [Git branch](https://git-scm.com/docs/git-branch) and [for-each-ref](https://git-scm.com/docs/git-for-each-ref): reachability, upstream tracking, dates, and worktree data used by the body.
