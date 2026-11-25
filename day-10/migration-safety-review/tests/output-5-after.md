## Migration Review: input-5.sql

**Database:** PostgreSQL 15  
**Overall risk:** High

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | Add `recorded_at` with `DEFAULT clock_timestamp()` | High | The volatile default rewrites the table and its indexes while holding an `ACCESS EXCLUSIVE` lock, blocking reads and writes. Table size is unknown, so this rating assumes at least one million rows. [PostgreSQL 15 ALTER TABLE documentation](https://www.postgresql.org/docs/15/sql-altertable.html) | Add the nullable column without a default, then set the default for future inserts. Backfill existing rows in batches if needed, after agreeing on the intended historical timestamp. |
| 2 | Rename `status` to `lifecycle_status` | Low | The rename is metadata-only but needs an `ACCESS EXCLUSIVE` lock. Any deployed code or external consumer still querying `status` will fail after the rename; usage is unverified. [PostgreSQL 15 ALTER TABLE documentation](https://www.postgresql.org/docs/15/sql-altertable.html) | If consumers still use `status`, use an expand/contract rollout: add the new column, keep both values synchronized, migrate consumers, and remove the old column only after they no longer use it. |

### Recommended rollout

1. Before merging, replace the volatile-default column addition with an add-without-default followed by setting the default. Use a bounded `lock_timeout` and keep the DDL transaction short; the timeout limits lock acquisition time, not how long an acquired lock is held.
2. Decide whether existing rows need a timestamp and backfill in batches if they do.
3. Inventory application and external uses of `status`. If any remain, deploy a synchronized transition and compatible consumers before removing the old name.

### Questions for the author

- How many rows are in `orders`, and does the migration runner wrap both statements in a transaction?
- What should `recorded_at` mean for existing orders? Is `NULL` acceptable during a backfill?
- Do any deployed services, jobs, reports, or external consumers still read or write `orders.status`? The available workspace search did not establish application usage.