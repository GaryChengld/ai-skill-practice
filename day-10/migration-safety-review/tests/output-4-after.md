## Migration Review: input-4.sql

**Database:** PostgreSQL 15  
**Overall risk:** Low

### Findings

| # | Statement | Risk | Why | Safer alternative |
|---|---|---|---|---|
| 1 | Add nullable `label text` to `offices` | Low | This is a metadata-only change with no table rewrite. It requires an `ACCESS EXCLUSIVE` lock, which can wait behind other transactions and remains held until the migration transaction commits. Existing rows receive `NULL`. | No change needed. Consider a bounded `lock_timeout` so the migration fails rather than waiting indefinitely for the lock. |

### Recommended rollout

1. Confirm the application accepts `NULL` for existing rows and that any positional inserts or consumers expecting a fixed column list remain compatible.
2. Run the migration in a short transaction, optionally with a bounded `lock_timeout`, and commit promptly after the statement.

### Questions for the author

- Does the migration runner wrap this statement in a larger transaction?
- Should existing offices have a label populated, or is `NULL` the intended initial value?