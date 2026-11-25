## Migration Review: input-2.sql

**Database:** PostgreSQL 15  
**Overall risk:** High

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | `CREATE INDEX CONCURRENTLY` | High | It is inside `BEGIN`/`COMMIT`. PostgreSQL rejects concurrent index creation inside a transaction block, so the migration fails before adding the foreign key. [PostgreSQL documentation](https://www.postgresql.org/docs/15/sql-createindex.html) | Run the index build separately, outside both the explicit transaction and any migration-runner transaction wrapper. |
| 2 | `ADD CONSTRAINT ... FOREIGN KEY` | High | If the transaction issue is fixed alone, this validates roughly 40 million existing orders while holding locks on both tables that block writes. | Add the foreign key with `NOT VALID`, commit promptly, and validate it separately. The constraint enforces new writes immediately; existing rows are checked during validation. [PostgreSQL documentation](https://www.postgresql.org/docs/15/sql-altertable.html) |

### Recommended rollout

1. Configure a bounded `lock_timeout` for the migration session and run `CREATE INDEX CONCURRENTLY` outside a transaction. If it fails, inspect for an invalid index and remove it before retrying.
2. Check for orphaned non-null `orders.customer_id` values and resolve them. Confirm the application will not create new orphans once the constraint is enforced.
3. Add the constraint in a short transaction, then commit:

   ```sql
   ALTER TABLE orders ADD CONSTRAINT orders_customer_fk
       FOREIGN KEY (customer_id) REFERENCES customers (id) NOT VALID;
   ```

4. Run `ALTER TABLE orders VALIDATE CONSTRAINT orders_customer_fk;` separately. Validation scans existing rows under weaker locks, though it can still consume substantial resources.

### Questions for the author

- Does the migration runner support a non-transactional migration for the concurrent index build?
- Are either table partitioned? PostgreSQL 15 has additional restrictions on concurrent index builds and `NOT VALID` foreign keys on partitioned tables.
- Is `customers.id` backed by a suitable primary key or unique constraint, and are there existing orphaned orders?