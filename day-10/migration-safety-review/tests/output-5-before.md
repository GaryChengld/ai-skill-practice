## Migration Review: input-5.sql

**Database:** PostgreSQL 15  
**Overall risk:** High

I would address both statements before merging. The size of `orders` and the application’s use of `status` are unknown, so the review assumes a busy, large table and a rolling deployment.

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | `ADD COLUMN recorded_at ... DEFAULT clock_timestamp()` | High | `clock_timestamp()` is volatile, so PostgreSQL rewrites the table and its indexes while holding an `ACCESS EXCLUSIVE` lock. Reads and writes can be blocked for the duration. Existing rows receive migration-time values, which may not represent when the orders were recorded. [PostgreSQL 15 documentation](https://www.postgresql.org/docs/15/sql-altertable.html) | Add the nullable column without a default, set the default in a separate brief DDL step, then backfill existing rows in small committed batches using an agreed historical value. |
| 2 | `RENAME COLUMN status TO lifecycle_status` | High | Any running application version or external query still using `status` will fail after the rename. The rename also needs an `ACCESS EXCLUSIVE` lock, though it normally does not rewrite the table. | Use an expand-and-contract rollout: add the new column, keep both values synchronized during deployment, migrate readers and writers, then remove the old column after all consumers have moved. |

### Recommended rollout

1. Set a short `lock_timeout`, such as `5s`, for each DDL step, and retry if the lock cannot be acquired. A timeout limits the wait for the lock; it does not limit how long an acquired lock is held.
2. Add `recorded_at` without a default, then set its `clock_timestamp()` default in a separate short transaction. Backfill old rows in batches only after deciding what their timestamps should mean. Monitor the backfill’s load and replication impact.
3. Introduce `lifecycle_status` alongside `status`. Synchronize writes and backfill existing values, then deploy readers and writers that use the new column. Account for old application instances and other consumers during the transition.
4. Once all consumers have moved, remove the synchronization mechanism and retire `status` in a later migration. Keep a rollback plan that preserves both columns until reverting the application is no longer necessary.

### Questions for the author

- How large and busy is `orders`, and does the migration runner wrap both statements in one transaction?
- What should `recorded_at` mean for existing orders: a historical timestamp, the migration time, or unknown?
- Which application versions, jobs, reports, and external consumers currently read or write `status`?