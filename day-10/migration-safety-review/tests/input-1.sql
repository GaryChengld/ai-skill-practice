-- PostgreSQL 15, orders ~40M rows
ALTER TABLE orders ADD COLUMN recorded_at timestamptz DEFAULT clock_timestamp();
