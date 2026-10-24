# Independent routing challenge

2026-10-24: `collaboration.spawn_agent`, `fork_turns: none`, one fresh session per query; inherited model settings, not pinned. Session suffixes: day05_review_h01, h02, h03_exact, h04.
Expected labels frozen before testing. Each case receives the five-skill catalog XML plus the same neutral selection-only instruction and one query. No expected labels, skill bodies, earlier queries, tools, or file access are supplied.
| ID | Query | Expected | Actual | Pass |
| --- | --- | --- | --- | --- |
| H01 | Clean up my feature branch before review. | NONE | NONE | Pass |
| H02 | Write up what went wrong with Tuesday's deploy for the team. | incident-postmortem | incident-postmortem | Pass |
| H03 | Summarize this diff for the reviewers. | pr-description | pr-description | Pass |
| H04 | Which of these branches can I get rid of? | stale-branches | stale-branches | Pass |

Actual reasons, retained verbatim:
- H01: "Preparing a feature branch for review does not specifically request stale-branch cleanup, a PR description, or another cataloged task."
- H02: "The user wants an internal write-up of what went wrong with a deploy, which fits a post-incident review."
- H03: "The user wants a reviewer-facing summary of a diff."
- H04: "The user wants to identify branches suitable for deletion."

Result: 4/4 labels match. H01 is the closest trap: cleanup of one active branch before review does not establish merged/inactive-branch deletion intent. NONE leaves history preparation or clarification to the general agent; it does not prove that the history needs rewriting.
H03 competes with commit summarization and code review, but the requested reviewer-facing summary fits pr-description. H02 tests post-incident intent without naming a document; H04 tests deletion intent without saying stale or merged.
No description changes: all four boundaries held in this run. The four coach-provided cases are targeted regression checks, not held-out discovery or evidence of general accuracy; each ran once with matching metadata.
Setup correction: an initial H03 session accidentally omitted "or activity" from release-notes' exclusion and returned pr-description. It was discarded for catalog mismatch; the counted H03 result comes from a new h03_exact session with the correct catalog.
This tests metadata selection only, not actual skill loading, safe branch classification, or generated artifacts. The original 12-query shared-context run remains separate.
