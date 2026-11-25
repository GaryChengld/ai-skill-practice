-- PostgreSQL 15, orders ~40M rows, customers ~2M rows
BEGIN;
CREATE INDEX CONCURRENTLY orders_customer_idx ON orders (customer_id);
ALTER TABLE orders ADD CONSTRAINT orders_customer_fk
    FOREIGN KEY (customer_id) REFERENCES customers (id);
COMMIT;
