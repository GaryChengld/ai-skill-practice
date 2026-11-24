# Day 09 results

Estimated tokens (one per four characters, rounded up).

| Layer | Original | Slim | Reduction |
| --- | ---: | ---: | ---: |
| Metadata | 78 | 57 | 26.9% |
| Description | 73 | 52 | 28.8% |
| Body | 1,322 | 447 | 66.2% |

The original [checklist](CHECKLIST.md) preceded the first four behavior tests, and the new criteria preceded the raw-diff runs. [Preflight hashes](harness/preflight.json) pin the review fixtures and rubric. All 15 scored sessions used `gpt-6.1-terra`. Input 5 used the same raw diff and isolated workspace across all three runs. The baseline had zero enabled skills.

| Check | Original | Slim | No skill |
| --- | --- | --- | --- |
| 1a uses `fix` | Pass | Pass | — |
| 1b describes token refresh before retry | Pass | Pass | — |
| 1c uses a fenced code block | Pass | Pass | — |
| 2a names the removal of `legacyMode` | Pass | Pass | — |
| 2b marks the breaking change | Pass (`!` and footer) | Pass (`!` and footer) | — |
| 2c gives the migration step | Pass | Pass | — |
| 3a recommends splitting | Pass | Pass | — |
| 3b proposes a CSV export `feat` | Pass | Pass | — |
| 3c proposes a login timeout `fix` | Pass | Pass | — |
| 4a identifies an empty diff | Pass | Pass | — |
| 4b asks for a diff or summary | Pass | Pass | — |
| 4c proposes no commit message | Pass | Pass | — |
| 5a marks the removed parameter as breaking | Pass (`!` and footer) | Pass (`!` and footer) | Fail |
| 5b tells callers to remove the second argument | Pass | Pass | Fail |
| **Total** | **14/14** | **14/14** | **0/2** |

The [registry snapshot](harness/registry.json) shows that only the slim copy was enabled for T1–T4. The [manifest](harness/manifest.json) identifies each fresh session. The empty-diff rerun and validator output are recorded in [Day 09 notes](../../NOTES.md).

| Trigger | Expected | Observed | Evidence |
| --- | --- | --- | --- |
| T1 commit message | Active | One verified slim file read | [Log excerpt](harness/t1.jsonl) |
| T2 PR description | Inactive | Zero skill read attempts | [Log excerpt](harness/t2.jsonl) |
| T3 release notes | Inactive | Zero skill read attempts | [Log excerpt](harness/t3.jsonl) |
| T4 “write a commit msg for this” | Active | One verified slim file read | [Log excerpt](harness/t4.jsonl) |

Removing the worked breaking-change example was the riskiest cut. Input 2 supplied the migration step. Input 5 showed only the signature and call-site changes: both skills inferred the compatibility break and told callers to remove the second argument. The baseline named the removal and omitted both the breaking marker and the migration step. This comparison covers one raw diff. No body text was added back.
