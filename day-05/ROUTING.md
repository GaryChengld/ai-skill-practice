# Five-skill routing

2026-10-24: fresh `collaboration.spawn_agent`, `fork_turns: none`, session `day05_routing_raw`; inherited model settings, not pinned.
Provided only the generated catalog XML as task knowledge plus a neutral routing-only instruction; no bodies, examples, expected labels, tools, or file access. Sent the queries individually, in order, to that session; earlier queries remain in its context.
Expected labels were fixed before querying. CC = conventional-commits; RN = release-notes; PR = pr-description; IP = incident-postmortem; SB = stale-branches.
| ID | Query | Expected | Actual | Pass |
| --- | --- | --- | --- | --- |
| Q01 | Suggest a commit message for my staged CHANGELOG.md update. | CC | CC | Pass |
| Q02 | Update CHANGELOG.md from the commits merged since v2.0. | RN | RN | Pass |
| Q03 | Write a reviewer-facing PR body for the new release announcement feature. | PR | PR | Pass |
| Q04 | Turn these merged PRs into a What's New announcement for customers. | RN | RN | Pass |
| Q05 | Delete my merged branches. | SB | SB | Pass |
| Q06 | Write a commit message for the branch cleanup script I added. | CC | CC | Pass |
| Q07 | Draft a PR description for my stale-branch report feature. | PR | PR | Pass |
| Q08 | Write an RCA from yesterday's resolved outage chat export. | IP | IP | Pass |
| Q09 | Announce the outage fix to customers in the v2.1 release notes. | RN | RN | Pass |
| Q10 | Explain how git rebase works. | NONE | NONE | Pass |
| Q11 | Checkout is failing right now; help me restore service. | NONE | NONE | Pass |
| Q12 | Summarize what the team shipped this sprint for Friday's demo. | NONE | NONE | Pass |

Result: 12/12 label matches. Q01-Q04, Q06-Q07, and Q09 probe cross-skill confusion; Q10-Q12 expect no skill. Q05's actual reason explicitly retained confirmation and report-only behavior.
Closest to failure: Q12's actual reason was "This is an internal sprint summary for a team demo, not customer-facing release notes." Its NONE label matches our conservative policy, but the audience is unspecified; clarification is warranted rather than confidently calling it internal.
No description change: release-notes already distinguishes customer deliverables from internal reports; this ambiguous result does not justify another wording rule. Q12 reuses a day-02 challenge, so it is not held-out evidence.
This is one conversational metadata-selection run, not application activation or skill-body execution; 100% here does not establish general routing accuracy or correct follow-up behavior.

Review follow-up: these explicit-deliverable queries remain an easy historical baseline. See [four harder independent-session cases](ROUTING-CHALLENGE.md) for the added test; do not pool its score with this context-sharing run.
