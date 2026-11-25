## Migration Review: input-2.sql

**Database:** PostgreSQL 15  
**Overall risk:** High — the migration fails as written, and the foreign key would block writes for a potentially long scan if the transaction issue were fixed alone.

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | `BEGIN` / `COMMIT` | High | The explicit transaction makes the concurrent index build fail. PostgreSQL does not allow `CREATE INDEX CONCURRENTLY` inside a transaction block; the foreign key will therefore not be installed in this run. | Run the index build outside a transaction, including any transaction automatically supplied by the migration runner. [PostgreSQL documentation](https://www.postgresql.org/docs/15/sql-createindex.html) |
| 2 | `CREATE INDEX CONCURRENTLY` | Medium | Once run outside a transaction, it permits concurrent writes, but scans the 40M-row table twice and can create substantial load. A failed build can leave an invalid index behind. | Build concurrently in a separate nontransactional migration. Monitor load and inspect for an invalid index on failure; drop it before retrying. |
| 3 | `ADD CONSTRAINT ... FOREIGN KEY` | High | It validates existing orders immediately and holds locks that block writes on both `orders` and `customers` until the transaction commits. Existing orphaned IDs also cause it to fail. | Add the foreign key with `NOT VALID`, commit promptly, then validate it separately. New inserts and updates are enforced immediately; validation checks existing rows without blocking concurrent updates. [PostgreSQL documentation](https://www.postgresql.org/docs/15/sql-altertable.html) |

### Recommended rollout

1. Configure a short `lock_timeout`, such as `5s`, for the migration session, and ensure the runner does not wrap the concurrent index build in a transaction.
2. Build `orders_customer_idx` concurrently. Check its validity and recover from any failed build before continuing.
3. In a short, separately committed transaction, add the foreign key with `NOT VALID`. Make sure application writes already satisfy it: new violations will be rejected immediately.
4. Run `ALTER TABLE orders VALIDATE CONSTRAINT orders_customer_fk` separately. If it fails, repair existing orphaned rows and retry validation. Monitor database load during the scan.

### Questions for the author

- Does the migration runner automatically wrap migrations in a transaction, and can it run a nontransactional migration?
- Is `customers.id` backed by an eligible primary key or unique index, and are there existing orphaned `orders.customer_id` values?
- Is `orders` partitioned? PostgreSQL 15 does not support a concurrent index build directly on a partitioned table, and its `NOT VALID` foreign-key restrictions would affect this rollout.