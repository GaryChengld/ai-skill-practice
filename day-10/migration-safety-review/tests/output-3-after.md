## Migration Review: input-3.sql
**Database:** MySQL 8.0.34, InnoDB  
**Overall risk:** High

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | Modify `shipment_seq` to `BIGINT NOT NULL` | High | The current column definition is unknown. If this changes the physical type, MySQL requires a table copy and blocks concurrent writes. On approximately 20 million rows, that could cause prolonged write downtime. Existing nulls, column attributes, and application dependencies also need checking. [MySQL online DDL operations](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html) | Confirm the existing definition and data first. If a type change is needed, evaluate an online schema-change tool such as gh-ost or pt-online-schema-change against the table’s constraints and deployment setup. Preserve required column attributes and test the cutover. |
| 2 | Add `orders_customer_idx` | Low | An ordinary secondary index can be built in place while allowing concurrent writes, though the build consumes resources and requires metadata locks at its boundaries. Long transactions can delay those locks and queue later queries. [MySQL online DDL operations](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html), [DDL concurrency](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-performance.html) | Keep it separate and specify `ALGORITHM=INPLACE, LOCK=NONE` so it fails if the server cannot allow concurrent DML. |

### Recommended rollout

1. Check `SHOW CREATE TABLE orders`, the null count, dependencies, and whether an equivalent customer index already exists. Confirm that the modified column definition retains all required attributes.
2. If the type must change, test an online schema-change approach on a production-like dataset, including disk capacity, replication impact, and cutover behavior.
3. Deploy the index separately with `ALTER TABLE orders ADD INDEX orders_customer_idx (customer_id), ALGORITHM=INPLACE, LOCK=NONE;`. Monitor load and available disk space.
4. Before each operation, check for long-running transactions and use a bounded metadata-lock wait with an abort plan. Account for MySQL DDL’s implicit commits when planning recovery from a partially completed migration.

### Questions for the author

- What is the current complete definition of `shipment_seq`, and are any rows null?
- Do application code, foreign keys, or other dependencies assume its current type or attributes?
- What write interruption is acceptable, and is an online schema-change tool available in this environment?