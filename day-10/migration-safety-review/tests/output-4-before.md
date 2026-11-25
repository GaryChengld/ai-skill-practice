## Migration Review: input-4.sql

**Database:** PostgreSQL 15  
**Overall risk:** Low

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | [`ALTER TABLE offices ADD COLUMN label text`](C:/Users/Gary/AppData/Local/Temp/day10-review-_6wfhepa/before/input-4.sql:2) | Low | Adding a nullable column without a default does not rewrite the table. PostgreSQL still needs an `ACCESS EXCLUSIVE` lock, so a long-running transaction could delay the migration and cause other queries to queue. Existing rows will have `NULL` in `label`. | Keep the statement, but set a short `lock_timeout` before it and retry if acquiring the lock times out. Ensure application code handles `NULL`. |

### Recommended rollout

1. Set `lock_timeout`, for example to `5s`, before running the DDL.
2. Run the migration and retry after investigating blockers if it times out.
3. Deploy code that tolerates `NULL` labels; backfill separately if labels are required.

### Questions for the author

- Does the application expect every office to have a label, or is `NULL` acceptable?