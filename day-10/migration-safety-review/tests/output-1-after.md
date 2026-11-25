## Migration Review: input-1.sql

**Database:** PostgreSQL 15  
**Overall risk:** High

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | Add `orders.recorded_at` with `DEFAULT clock_timestamp()` | High | `clock_timestamp()` is volatile, so PostgreSQL rewrites the roughly 40-million-row table and its indexes. The `ALTER TABLE` takes an `ACCESS EXCLUSIVE` lock, blocking reads and writes while held; it remains held until the transaction commits. The rewrite can also require substantial disk space and generate heavy I/O. [PostgreSQL 15 documentation](https://www.postgresql.org/docs/15/sql-altertable.html) | Add the nullable column without a default, then set the default for future inserts. Backfill existing rows in bounded batches only if needed. |

### Recommended rollout

1. Confirm what `recorded_at` should mean for existing orders and whether the application can tolerate `NULL` during rollout.
2. In a short transaction with a bounded `lock_timeout`, add the column without a default and set the default before committing:

   ```sql
   SET LOCAL lock_timeout = '5s';
   ALTER TABLE orders ADD COLUMN recorded_at timestamptz;
   ALTER TABLE orders ALTER COLUMN recorded_at SET DEFAULT clock_timestamp();
   ```

   Run these inside an explicit transaction if the migration runner does not already provide one. The DDL still needs an exclusive lock, so retry if lock acquisition times out, and commit promptly.
3. If historical values are required, backfill in small committed batches using the agreed source or timestamp semantics. Monitor database load, replication lag, and progress. A backfill-time timestamp will differ from the per-row timestamps the original migration would generate during its rewrite.
4. Deploy readers that handle existing `NULL` values until the backfill is complete, if applicable.

### Questions for the author

- Should existing orders have a historical timestamp, a migration-time timestamp, or `NULL`?
- Does the migration runner wrap this statement in a transaction, and can the application tolerate `NULL` values while any backfill runs?