# Day 09 results

Estimated tokens (one per four characters, rounded up).

| Layer | Original | Slim | Reduction |
| --- | ---: | ---: | ---: |
| Metadata | 78 | 49 | 37.2% |
| Description | 73 | 44 | 39.7% |
| Body | 1,322 | 447 | 66.2% |

The [checklist](CHECKLIST.md) was written before any behavior runs. [Preflight hashes](harness/preflight.json) record the checklist and prompts used. Each column uses four separate `gpt-6.1-terra` sessions that read the intended on-disk skill.

| Check | Original | Slim |
| --- | --- | --- |
| 1a uses `fix` | Pass | Pass |
| 1b describes token refresh before retry | Pass | Pass |
| 1c uses a fenced code block | Pass | Pass |
| 2a names the removal of `legacyMode` | Pass | Pass |
| 2b marks the breaking change | Pass (`!` and footer) | Pass (`!` and footer) |
| 2c gives the migration step | Pass | Pass |
| 3a recommends splitting | Pass | Pass |
| 3b proposes a CSV export `feat` | Pass | Pass |
| 3c proposes a login timeout `fix` | Pass | Pass |
| 4a identifies an empty diff | Pass | Pass |
| 4b asks for a diff or summary | Pass | Pass |
| 4c proposes no commit message | Pass | Pass |
| **Total** | **12/12** | **12/12** |

For these fresh trigger sessions, session-local config enabled only the slim copy. See the [registry snapshot](harness/registry.json) and [session manifest](harness/manifest.json). `collect-harness.py` extracts the prompt, tool calls, verified skill reads, and completed answer from each cited session log.

| Trigger | Expected | Observed | Evidence |
| --- | --- | --- | --- |
| T1 commit message | Active | One verified slim file read | [Log excerpt](harness/t1.jsonl) |
| T2 PR description | Inactive | Zero skill read attempts | [Log excerpt](harness/t2.jsonl) |
| T3 release notes | Inactive | Zero skill read attempts | [Log excerpt](harness/t3.jsonl) |

The riskiest cut was removing the worked breaking-change example. It showed how to connect the header marker, the compatibility impact, and migration guidance. With the condensed rule, the slim response still included both markers, explained that old configs are rejected, and told users to remove `legacyMode`. The scored comparisons showed no regression and required no additions.
