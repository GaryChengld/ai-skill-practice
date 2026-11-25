## Migration Review: input-1.sql

**Database:** PostgreSQL 15  
**Overall risk:** High

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | [`ALTER TABLE orders ADD COLUMN recorded_at ... DEFAULT clock_timestamp()`](input-1.sql) | High | `clock_timestamp()` is volatile, so PostgreSQL rewrites the table and its indexes. On approximately 40 million rows, this can take substantial time and hold an `ACCESS EXCLUSIVE` lock, blocking reads and writes until the transaction commits. It also assigns migration-time values to historical rows, which may not represent when those orders were recorded. [PostgreSQL documentation](https://www.postgresql.org/docs/15/sql-altertable.html) | Add the nullable column without a default, then set the default for future inserts. Backfill existing rows in small, committed batches only if needed, using a value whose meaning is agreed upon. |

### Recommended rollout

1. Replace the migration with short metadata changes, using a lock timeout and committing promptly:

   ```sql
   SET lock_timeout = '5s';

   ALTER TABLE orders ADD COLUMN recorded_at timestamptz;
   ALTER TABLE orders ALTER COLUMN recorded_at SET DEFAULT clock_timestamp();
   ```

   Both statements still need a brief exclusive lock; the timeout limits how long they wait to acquire it. Ensure the migration runner does not keep the transaction open afterward.

2. Make application reads tolerate `NULL` for historical rows. If they need values, backfill in small, committed batches, with a `WHERE recorded_at IS NULL` guard, and monitor database load and replication lag.
3. Verify the backfill and application behavior before adding any future non-null constraint.

### Questions for the author

- What should `recorded_at` mean for existing orders? A migration or backfill timestamp may be misleading.
- Can the application tolerate `NULL` for historical rows during and potentially after rollout?