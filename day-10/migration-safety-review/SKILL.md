---
name: migration-safety-review
description: Review an existing PostgreSQL or MySQL migration for locks, rewrites, downtime, and safer rollout options. Use when asked to assess SQL or schema changes before deployment. Not for writing new migrations or tuning slow queries.
---

# Migration Safety Review

1. Read the supplied migration as text. Identify the engine, version, affected table sizes, and transaction context from the request and SQL. Ask which engine to use if it remains ambiguous. Treat unknown table sizes as large and state material assumptions.
2. Read `references/postgres.md` for PostgreSQL or `references/mysql.md` for MySQL. For each statement, identify its locks, rewrites, transaction restrictions, and compatibility risks. Propose a safer alternative for each material finding.
3. For a column rename or drop, check whether deployed code still uses the column. If it does, use expand/contract and deploy compatible code before removing the old schema. Ask about application usage if unclear.
4. Use `small` below 1 million rows and `large` otherwise. Choose `application_breakage` or `execution_blocker` with size `any` only when the SQL or request establishes it. Otherwise choose the most likely effect (`rewrite`, `sustained_write_blocking`, or `online_or_metadata_only`) and list unverified conditions as questions.
5. Read `assets/risk-matrix.csv` and use only the rows for the `table_size,operation_effect` pairs you selected. Set the overall risk to the highest finding rating.
6. For a completed review, copy and fill `assets/review-template.md`. Use only the template's headings and section content. Put source links inside the Why column. Indent any continuation text or code under its list item.
