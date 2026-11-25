## Migration Review: input-3.sql

**Database:** MySQL 8.0.34, InnoDB  
**Overall risk:** High — I would address the first statement before merging.

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | `MODIFY COLUMN shipment_seq BIGINT NOT NULL` | High | If this changes the existing data type, MySQL must rebuild the roughly 20-million-row table and cannot allow concurrent writes during the operation. The current column definition is unknown: `MODIFY` also drops omitted attributes such as `UNSIGNED`, defaults, and comments. Existing `NULL` or out-of-range values could cause failure or conversion issues. [MySQL online DDL operations](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html), [ALTER TABLE](https://dev.mysql.com/doc/refman/8.0/en/alter-table.html) | Inspect `SHOW CREATE TABLE orders` and preserve intended attributes. If a type change is necessary, evaluate an online schema change tool such as gh-ost or pt-online-schema-change against the table’s keys, foreign keys, triggers, and replication setup. |
| 2 | `ADD INDEX orders_customer_idx (customer_id)` | Low | InnoDB can build a secondary index in place while allowing concurrent writes. It still needs metadata locks, consumes I/O and disk, and can wait behind long transactions. [MySQL online DDL operations](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html), [DDL concurrency](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-performance.html) | Specify `ALGORITHM=INPLACE, LOCK=NONE` to fail if the requested online behavior is unavailable. Check whether an existing index already serves this access pattern. |

### Recommended rollout

1. Inspect the existing column definition, indexes, dependencies, and data; check for `NULL` values and values incompatible with the intended signed `BIGINT`.
2. Test the chosen schema-change method on representative data. Plan for disk usage, replication lag, metadata-lock waits, and rollback.
3. Run the index addition separately with `ALGORITHM=INPLACE, LOCK=NONE`, after checking for long-running transactions and setting an appropriate session `lock_wait_timeout`.
4. Verify the resulting schema and index, and monitor application latency and replication.

### Questions for the author

- What is the current definition of `shipment_seq`, including its default and whether it is unsigned or nullable?
- Does `orders` have foreign keys or triggers, and what replication setup is in use?
- Is there already an index beginning with `customer_id`?