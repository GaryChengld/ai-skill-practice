Could this ALTER take prod down? We're on PostgreSQL 15 and the orders table has about 55 million rows.

```sql
ALTER TABLE orders ALTER COLUMN external_ref SET NOT NULL;
```
