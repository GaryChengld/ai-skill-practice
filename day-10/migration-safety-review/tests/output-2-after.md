## Migration Review: input-2.sql

**Database:** PostgreSQL 15  
**Overall risk:** High

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | `CREATE INDEX CONCURRENTLY` inside `BEGIN` | High | PostgreSQL rejects a concurrent index build inside a transaction block, so this migration cannot complete as written. [PostgreSQL documentation](https://www.postgresql.org/docs/15/sql-createindex.html) | Run the index build separately, outside both the explicit transaction and any migration-runner transaction wrapper. |
| 2 | `ADD FOREIGN KEY` | High | Once the transaction issue is fixed, the default validation scans approximately 40 million orders while holding `SHARE ROW EXCLUSIVE` locks on both tables, blocking writes until commit. Existing orphan rows would also cause it to fail. [PostgreSQL documentation](https://www.postgresql.org/docs/15/sql-altertable.html) | Add the constraint with `NOT VALID`, commit promptly, then validate it in a separate transaction. |

### Recommended rollout

1. Confirm the table and application conditions below. Configure a bounded `lock_timeout` for the migration session.
2. Build `orders_customer_idx` concurrently in a standalone operation. If it fails, inspect for an invalid index and remove it before retrying.
3. Add the foreign key with `NOT VALID` and commit immediately. This still briefly requires write-blocking locks on both tables and begins enforcing the constraint for subsequent writes.
4. Check and repair existing orphan rows, then run `VALIDATE CONSTRAINT` separately. Validation scans existing rows but permits concurrent writes; it takes `SHARE UPDATE EXCLUSIVE` on `orders` and `ROW SHARE` on `customers`.

### Questions for the author

- Does the migration runner support a migration without a transaction wrapper?
- Is `orders` partitioned? PostgreSQL 15 restricts concurrent index builds and `NOT VALID` foreign keys on partitioned tables.
- Is `customers.id` backed by an eligible unique or primary key, and are existing and new `orders.customer_id` values compatible with the constraint?