-- MySQL 8.0.34 InnoDB, orders ~20M rows
ALTER TABLE orders MODIFY COLUMN shipment_seq BIGINT NOT NULL;
ALTER TABLE orders ADD INDEX orders_customer_idx (customer_id);
