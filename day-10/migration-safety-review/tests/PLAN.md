# Migration safety review evaluation plan

This plan and the SQL fixtures are committed before any sessions run. Score each listed check independently against the completed response. Accept equivalent wording and ignore formatting differences when scoring content. Verify file reads and template fidelity separately using the harness.

## Disposition of the baseline

| BEFORE section | Destination | Rationale |
| --- | --- | --- |
| Frontmatter description | Rewrite as discovery metadata | Scope the review to existing PostgreSQL and MySQL migrations and exclude authoring and query tuning. |
| Introduction | Delete | Model already knows what migrations are. Remove generic motivation. |
| What is a lock? | Delete | Model already knows the concept. The references explain the locks each operation takes. |
| Steps | Body | Keep the shared workflow, engine identification, per-statement review, and aggregation. Remove the repeated reminder. |
| PostgreSQL rules | PostgreSQL reference and body | Move engine rules to the reference. Consolidate the compatibility rule in the body. |
| MySQL rules | MySQL reference and body | Move engine rules to the reference. Use the shared compatibility rule already in the body. |
| Risk levels | Risk matrix and body | The matrix owns risk values. The body owns the unknown-size rule and chooses the highest matching risk. Treat a statement that cannot run as written as a rollout blocker. |
| Output format and embedded Migration Review heading | Template asset | Keep one copy of the output structure. |
| Example and embedded Migration Review heading | Delete | The worked example repeats the template and PostgreSQL guidance. |
| Important reminders | Delete | Repetition. Each actionable rule already has a single source. |

## Checklist

| Input | ID | Pass criterion |
| --- | --- | --- |
| 1 | 1a | Rates the migration High overall. |
| 1 | 1b | Identifies `clock_timestamp()` as volatile or per-row and attributes the table rewrite to that default. |
| 1 | 1c | Recommends adding the column without the volatile default and backfilling separately. |
| 2 | 2a | Rates the migration High overall. |
| 2 | 2b | Identifies the explicit transaction conflict and moves the concurrent build outside it. |
| 2 | 2c | Identifies that the foreign key validates existing rows and takes locks affecting writes. |
| 2 | 2d | Proposes `NOT VALID` followed by separate validation. |
| 3 | 3a | Rates the migration High overall. |
| 3 | 3b | Identifies the integer-to-`BIGINT` type change as a table copy that blocks writes. |
| 3 | 3c | Proposes an online schema-change approach for the type change. |
| 3 | 3d | Distinguishes the online secondary index build from the copy and calls out its metadata locks. |
| 4 | 4a | Rates the migration Low overall. |
| 4 | 4b | Explains that the nullable column without a default needs no rewrite or backfill. |
| 4 | 4c | Includes no fabricated Medium or High finding. A brief lock or conditional scheduling caveat is acceptable. |

Use the same ordinary request and model across BEFORE, AFTER, and zero-skill sessions. The isolated harness must expose only the tested variant when enabled. Retain final responses verbatim. For implicit triggers, use an existing `ALTER` deployment question, a migration-authoring request, and a slow SELECT question, with only AFTER discoverable.
