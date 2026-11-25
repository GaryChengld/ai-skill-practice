## Migration Review: input-1.sql

**Database:** PostgreSQL 15  
**Overall risk:** High

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | Add `recorded_at` with `DEFAULT clock_timestamp()` | High | The volatile default rewrites the approximately 40 million-row table and its indexes. The `ALTER TABLE` takes an `ACCESS EXCLUSIVE` lock, blocking reads and writes while held; a surrounding transaction can extend that time. The rewrite also requires substantial I/O and temporary disk space. [PostgreSQL 15 ALTER TABLE documentation](https://www.postgresql.org/docs/15/sql-altertable.html) | Add the nullable column without a default, then set the default for future inserts. Backfill existing rows in batches only if needed, using agreed timestamp semantics. |

### Recommended rollout

1. Before merging, replace the statement with a short transaction that adds the column and sets the future default. Use a bounded lock timeout and commit promptly:

   ```sql
   SET LOCAL lock_timeout = '5s';
   ALTER TABLE orders ADD COLUMN recorded_at timestamptz;
   ALTER TABLE orders ALTER COLUMN recorded_at SET DEFAULT clock_timestamp();
   ```

   `SET LOCAL` requires a transaction; use the migration runner’s transaction wrapper or an explicit transaction. These operations still need a brief exclusive lock, and the timeout limits the wait to acquire it, not the time it is held.

2. If existing rows need values, backfill them in small, committed batches. Monitor database load and replication lag. The resulting timestamps will reflect the chosen backfill strategy, not necessarily the values the original rewrite would have produced.

### Questions for the author

- What should `recorded_at` mean for existing orders, and can it remain `NULL` until a backfill completes?
- Does the migration runner wrap this file in a transaction, and can application code tolerate existing rows having a null value?