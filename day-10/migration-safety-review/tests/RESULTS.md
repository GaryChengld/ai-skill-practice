# Migration safety review results

Estimated with the Day 09 counter at one token per four characters, rounded up. The AFTER body is 70.3% smaller.

| Context layer | BEFORE | AFTER |
| --- | ---: | ---: |
| Metadata (description only in parentheses) | 128 (122) | 63 (57) |
| Body | 1,511 | 449 |
| PostgreSQL / MySQL references | — | 481 / 314 |
| Review template / risk matrix | — | 112 / 67 |

The [rubric](PLAN.md) was committed in `c62bfd5`. P = pass, F = fail. The [manifest](harness/manifest.json) records the session IDs, read evidence, and hashes.

| Input | BEFORE | AFTER | Baseline |
| --- | --- | --- | --- |
| 1 · volatile default | a P, b P, c P | a P, b P, c P | a P, b P, c P |
| 2 · transaction and foreign key | a P, b P, c P, d P | a P, b P, c P, d P | a F, b P, c P, d P |
| 3 · type change and index | a P, b P, c P, d P | a P, b P, c P, d P | a F, b P, c P, d P |
| 4 · nullable column | a P, b P, c P | a P, b P, c P | a F, b P, c P |
| **Total** | **14/14** | **14/14** | **11/14** |

| AFTER input | Reference | Assets and verified matrix rows |
| --- | --- | --- |
| [1](harness/1-after.jsonl) | `postgres.md` | Template, matrix header + `large,rewrite,High` |
| [2](harness/2-after.jsonl) | `postgres.md` | Template, matrix header + `any,execution_blocker,High` and `large,sustained_write_blocking,High` |
| [3](harness/3-after.jsonl) | `mysql.md` | Template, matrix header + `large,rewrite,High` and `large,online_or_metadata_only,Low` |
| [4](harness/4-after.jsonl) | `postgres.md` | Template, matrix header + `small,online_or_metadata_only,Low` |

| Implicit request | Expected | Observed |
| --- | --- | --- |
| [T1](harness/t1.jsonl) existing ALTER and production impact | Active | Active |
| [T2](harness/t2.jsonl) write a migration | Inactive | Inactive |
| [T3](harness/t3.jsonl) tune a SELECT | Inactive | Inactive |

Input 2 best distinguished the reviews. All three identified the transaction failure and foreign-key lock. AFTER rated the invalid statement as High and presented it separately from the High foreign-key finding. The baseline gave sound advice but left the overall risk unrated, as it also did for inputs 3 and 4. No rubric item separated BEFORE from AFTER. A version-sensitive engine case near the one-million-row boundary would test whether the split preserves both nuanced operation classification and the assigned rating.

[Day 10 notes](../../NOTES.md) records validation and retained retries.
