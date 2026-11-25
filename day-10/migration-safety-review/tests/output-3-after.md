## Migration Review: input-3.sql

**Database:** MySQL 8.0.34, InnoDB  
**Overall risk:** High

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | Modify `shipment_seq` to `BIGINT NOT NULL` | High | The current column definition is unknown. If this changes its physical type, MySQL must copy the approximately 20-million-row table and block writes during the operation. If it only makes an existing `BIGINT` non-nullable, it can still rebuild the table. Existing `NULL` values can cause the change to fail, and `MODIFY COLUMN` can change attributes omitted from the new definition. | Confirm the current definition and data first. For a type change, evaluate an online schema-change tool such as gh-ost or pt-online-schema-change against the table’s constraints and deployment setup. Preserve required column attributes. |
| 2 | Add `orders_customer_idx` on `customer_id` | Low | An ordinary secondary index can be built in place with concurrent writes, although it consumes resources and needs metadata locks. A long-running transaction can delay those locks and cause other queries to queue. | Run it separately with `ALGORITHM=INPLACE, LOCK=NONE` so it fails if the requested concurrency cannot be honored. Set a bounded metadata-lock wait and monitor the build. |

MySQL documents the table rebuild and concurrency behavior for [column changes and secondary indexes](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html), and the [metadata-lock requirements for online DDL](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-limitations.html).

### Recommended rollout

1. **Hold the first statement** until the existing column definition, data, and application dependencies are checked. Verify null counts, signedness, defaults, and other attributes, and ensure the application supports the resulting range and non-null requirement.
2. Choose and rehearse an online schema-change approach if the type must change. Check available disk space, replication impact, tool compatibility, and the cutover and abort plan.
3. Deploy the index independently using the explicit online algorithm and lock options. Check for long-running transactions before starting, and monitor lock waits, resource use, and replication lag.

### Questions for the author

- What is the output of `SHOW CREATE TABLE orders`, especially the current definition of `shipment_seq` and any foreign keys?
- Are there any `NULL` values in `shipment_seq`, and can deployed application versions handle the new definition?
- What migration runner and replication setup will execute these statements, and is an online schema-change tool available?