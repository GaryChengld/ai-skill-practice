This PostgreSQL 15 SELECT takes 20 seconds on a large table. How would you speed it up?

```sql
SELECT customer_id, MAX(created_at)
FROM orders
WHERE status = 'paid'
GROUP BY customer_id;
```
