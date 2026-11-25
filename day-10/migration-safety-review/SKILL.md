---
name: migration-safety-review
description: Review an existing PostgreSQL or MySQL migration for locks, rewrites, downtime, and safer rollout options. Use when asked to assess SQL or schema changes before deployment. Not for writing new migrations or tuning slow queries.
---

# Migration Safety Review

1. Read the supplied migration as text. Identify the engine, version, affected table sizes, and transaction context from the request and SQL. Ask which engine to use if it remains ambiguous. Treat unknown table sizes as large and state material assumptions.
2. For PostgreSQL, read `references/postgres.md`. For MySQL, read `references/mysql.md`. Inspect each statement in order for lock scope and duration, rewrites, transaction restrictions, and application compatibility. Identify rollout blockers and propose a safer alternative for each material finding. Finish classifying the statements before opening either asset.
3. For a column rename or drop, check whether deployed code still uses the column. If it does, use expand/contract and deploy compatible code before removing the old schema. Ask about application usage if unclear.
4. Use `small` below 1 million rows and `large` otherwise. Choose one effect per statement, in order: `application_breakage`, `execution_blocker`, `rewrite`, `sustained_write_blocking`, `online_or_metadata_only`. Use `any` for the first two only when the available evidence establishes them. Put unverified prerequisites in the questions and use the most material expected effect for the lookup.
5. Use `assets/risk-matrix.csv` to look up only the selected exact `table_size,operation_effect` keys. Use a filtered or row-range read that returns the header and those rows. Do not open the whole CSV or look up speculative alternatives. Set the overall risk to the highest finding rating.
6. For a completed review, copy and fill `assets/review-template.md`. Use the template as the complete response structure, including its headings and table columns. Ground the rollout and questions in the actual SQL and its deployment context.
