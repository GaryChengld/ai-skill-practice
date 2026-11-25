---
name: migration-safety-review
description: This skill is a comprehensive and helpful assistant for database migrations. It can be used to review SQL migration files, schema changes, DDL statements, ALTER TABLE commands, index creation, and other database changes for PostgreSQL and MySQL, and it will help you understand whether they are safe to run in production, identify risks such as table locks, table rewrites, and downtime, and suggest safer alternatives. Use it whenever the user is working with databases or migrations.
---

# Migration Safety Review

## Introduction
Database migrations are scripts that change the schema of a database, such as creating tables, adding columns, or adding indexes. They are an important part of software development because applications evolve over time. However, migrations can be dangerous in production because they may lock tables and cause downtime. This skill helps you review migrations carefully so that they are safe. It is very important to be thorough and careful when reviewing migrations.

## What is a lock?
A lock is a mechanism that databases use to prevent conflicting concurrent access to data. When a table is locked, other queries may have to wait. If a migration holds a strong lock on a busy table for a long time, application requests will queue up and may time out.

## Steps
1. Read the migration file the user provides.
2. Figure out which database it is for (PostgreSQL or MySQL). If the user does not say, look for clues such as `CONCURRENTLY` (PostgreSQL) or `ALGORITHM=` (MySQL). If you still cannot tell, ask the user.
3. Go through each statement one by one and check whether it is risky.
4. For each risky statement, explain the risk and suggest a safer alternative.
5. Give an overall risk level.
6. Write the review using the output format below.
7. Always be careful and thorough. Remember to check every statement.

## PostgreSQL rules
- `CREATE INDEX` without `CONCURRENTLY` blocks writes to the table for the whole build. On large tables, use `CREATE INDEX CONCURRENTLY`.
- `CREATE INDEX CONCURRENTLY` cannot run inside a transaction block. Many migration tools wrap each migration in a transaction, so the migration must disable that (for example, a per-migration "no transaction" option).
- If a concurrent index build fails, it leaves an INVALID index behind that must be dropped before retrying.
- `ALTER TABLE ... ADD COLUMN` with a constant default is fast on PostgreSQL 11 and later (no table rewrite). With a volatile default such as `random()` or `clock_timestamp()`, the whole table is rewritten.
- `ALTER TABLE ... ALTER COLUMN ... TYPE` usually rewrites the table and holds an ACCESS EXCLUSIVE lock. Exceptions include increasing a `varchar` length limit or changing `varchar(n)` to `text`.
- `ALTER TABLE ... ALTER COLUMN ... SET NOT NULL` scans the whole table while holding an ACCESS EXCLUSIVE lock. Safer: add `CHECK (col IS NOT NULL) NOT VALID`, then `VALIDATE CONSTRAINT`, then `SET NOT NULL` (PostgreSQL 12+ skips the scan when a valid check constraint proves it), then drop the check.
- Adding a foreign key validates all existing rows and locks both tables. Safer: add it with `NOT VALID`, then run `VALIDATE CONSTRAINT` in a separate step.
- Always set `lock_timeout` (for example `SET lock_timeout = '5s';`) before DDL on busy tables so a blocked migration fails fast instead of queuing every other query behind it.
- Renaming or dropping a column that the running application still reads breaks the application. Use expand/contract: deploy code that stops using the column first.

## MySQL rules
- MySQL 8.0 InnoDB supports online DDL. Prefer `ALGORITHM=INSTANT` where supported (adding a column is INSTANT from 8.0.12, at any position from 8.0.29), then `ALGORITHM=INPLACE, LOCK=NONE`.
- State `ALGORITHM` and `LOCK` explicitly, so the statement fails instead of silently falling back to a table copy.
- Adding a secondary index is INPLACE and allows concurrent DML, but still takes a brief metadata lock at the start and end.
- Changing a column's data type usually requires `ALGORITHM=COPY`, which blocks writes. For large tables, use an online schema change tool such as gh-ost or pt-online-schema-change.
- Any DDL waits for a metadata lock. A long-running transaction on the table blocks the DDL, and every new query then queues behind the DDL.
- Renaming or dropping a column that the running application still reads breaks the application. Use expand/contract: deploy code that stops using the column first.

## Risk levels
If the table is small (under about 1 million rows) and the operation does not rewrite the table, the risk is low. If the table is small but the operation rewrites it, the risk is medium. If the table is large (over 1 million rows) and the operation takes a lock that blocks writes, the risk is high. If the table is large and the operation rewrites the table, the risk is high. If the operation breaks the running application (rename or drop of a column in use), the risk is high no matter the table size. If the table size is unknown, assume it is large. If the table is large and the operation is online, the risk is low.

## Output format
Always use this format exactly:

## Migration Review: <file name>
**Database:** <PostgreSQL or MySQL>
**Overall risk:** <Low / Medium / High>

### Findings
| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|

### Recommended rollout
1. ...

### Questions for the author
- ...

## Example
Input: a PostgreSQL migration with `CREATE INDEX idx_orders_user ON orders(user_id);` on a 40M-row table.
Output:

## Migration Review: 20240101_add_orders_index.sql
**Database:** PostgreSQL
**Overall risk:** High

### Findings
| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | CREATE INDEX idx_orders_user ON orders(user_id) | High | Blocks writes on a 40M-row table for the whole build | CREATE INDEX CONCURRENTLY, in a migration with the transaction wrapper disabled |

### Recommended rollout
1. Set lock_timeout.
2. Run the concurrent index build outside a transaction.
3. Check for an INVALID index if it fails.

### Questions for the author
- Does your migration tool wrap migrations in a transaction?

## Important reminders
- Remember to always check every statement.
- Remember that `CREATE INDEX CONCURRENTLY` cannot run inside a transaction.
- Remember to set `lock_timeout` on PostgreSQL.
- Remember that renaming or dropping a column in use breaks the application.
- Remember to use the output format exactly.
- Be helpful, careful and thorough.
