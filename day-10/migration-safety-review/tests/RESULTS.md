# Migration safety review results

Estimated with the Day 09 counter at one token per four characters, rounded up. The AFTER body is 75.9% smaller.

| Context layer | BEFORE | AFTER |
| --- | ---: | ---: |
| Metadata (description only in parentheses) | 128 (122) | 63 (57) |
| Body | 1,511 | 364 |
| PostgreSQL / MySQL references | — | 481 / 314 |
| Review template / risk matrix | — | 112 / 67 |

The [original rubric](PLAN.md) (`c62bfd5`) and [input 5 rubric](FOLLOWUP.md) (`72801c8`) preceded their runs. P = pass, F = fail. The [manifest](harness/manifest.json) records session IDs, file reads, template checks, and hashes.

| Input | BEFORE | AFTER | Baseline |
| --- | --- | --- | --- |
| 1 · volatile default | a P, b P, c P | a P, b P, c P | a P, b P, c P |
| 2 · transaction and foreign key | a P, b P, c P, d P | a P, b P, c P, d P | a F, b P, c P, d P |
| 3 · type change and index | a P, b P, c P, d P | a P, b P, c P, d P | a F, b P, c P, d P |
| 4 · nullable column | a P, b P, c P | a P, b P, c P | a F, b P, c P |
| 5 · unknown table size and column rename | a P, b P, c P | a P, b P, c P | a F, b F, c F |
| **Total** | **17/17** | **17/17** | **11/17** |

| AFTER input | Reference | Assets and matrix rows matching reported ratings |
| --- | --- | --- |
| [1](harness/1-after.jsonl) | `postgres.md` | Template, full matrix · `large,rewrite,High` |
| [2](harness/2-after.jsonl) | `postgres.md` | Template, full matrix · `any,execution_blocker,High` and `large,sustained_write_blocking,High` |
| [3](harness/3-after.jsonl) | `mysql.md` | Template, full matrix · `large,rewrite,High` and `large,online_or_metadata_only,Low` |
| [4](harness/4-after.jsonl) | `postgres.md` | Template, full matrix · `small,online_or_metadata_only,Low` |
| [5](harness/5-after.jsonl) | `postgres.md` | Template, full matrix · `large,rewrite,High` and `large,online_or_metadata_only,Low` |

| Implicit request | Expected | Observed |
| --- | --- | --- |
| [T1](harness/t1.jsonl) existing ALTER and production impact | Active | Active |
| [T2](harness/t2.jsonl) write a migration | Inactive | Inactive |
| [T3](harness/t3.jsonl) tune a SELECT | Inactive | Inactive |

Input 5 distinguished the skill variants from the baseline on content. Both variants assumed a large table, asked who still uses the old name, and gave an expand/contract sequence. The baseline identified both risks and mentioned a staged migration, but left the size assumption, explicit dependency question, and transition steps unstated. BEFORE and AFTER tied on the rubric. AFTER kept the rename's compatibility risk conditional because the SQL did not establish any dependent consumers.

[Day 10 notes](../../NOTES.md) records validation and retained retries.
