## Migration Review: input-4.sql

**Database:** PostgreSQL 15  
**Overall risk:** Low

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | [Add nullable `label` column](C:/Users/Gary/AppData/Local/Temp/day10-review-_6wfhepa/after-followup/input-4.sql:2) | Low | On the stated ~500-row table, adding a nullable column without a default is metadata-only; existing rows read as `NULL`. It requires an `ACCESS EXCLUSIVE` lock, which blocks reads and writes while held and can wait behind existing transactions. The lock is held until the transaction ends. [PostgreSQL `ALTER TABLE` documentation](https://www.postgresql.org/docs/15/sql-altertable.html), [locking documentation](https://www.postgresql.org/docs/15/explicit-locking.html). | No SQL change needed. Use a bounded lock timeout if the table is busy, and commit promptly. |

### Recommended rollout

1. Run the migration with a short `lock_timeout`, such as 5 seconds, and retry if lock acquisition times out.
2. Ensure the migration runner commits promptly after the statement. Check that consumers tolerate `label` being `NULL`; backfill separately if values are needed.

### Questions for the author

- Does the migration runner wrap this statement in a longer transaction?
- Is `NULL` acceptable for existing rows and for new rows that omit `label`?