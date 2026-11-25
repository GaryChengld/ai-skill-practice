-- PostgreSQL 15
ALTER TABLE orders ADD COLUMN recorded_at timestamptz DEFAULT clock_timestamp();
ALTER TABLE orders RENAME COLUMN status TO lifecycle_status;
