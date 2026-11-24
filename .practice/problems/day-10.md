# day-10：Unpack the Kitchen Sink — refactor an everything-in-one-file migration review skill

- 出题日期：2026-11-24
- 阶段：第二阶段 · 渐进式披露（第 5 题：阶段小结）

**学习目标**
- 把第二阶段的四种手段一次用全：拆 references/（day-06）、按领域分文件（day-07）、把模板和查找表放进 assets/（day-08）、按 token 预算删减（day-09）。
- 判断每一段内容该放哪一层：留在正文、移到 references/、变成 asset，还是直接删掉。
- 用不会“泄露答案”的测试输入证明重构没有让行为变差（针对 day-09 的天花板效应），并且有一个无 skill 基线说明 skill 本身有价值。

**背景知识**
渐进式披露有三层：元数据（name + description，启动时为所有 skill 加载）、正文（激活时加载，规范建议 < 5000 token、500 行以内）、资源（scripts/、references/、assets/，只在需要时读取）。阶段小结题的重点不是“把内容搬走”，而是给每段内容做一次分类：

| 内容类型 | 放哪里 |
|---|---|
| 每次运行都要遵守的流程和硬规则 | 正文 |
| 只对某个数据库 / 某种情况有用的细节 | `references/<domain>.md`，正文写明什么时候读哪个 |
| 输出的固定结构、可查表的数据 | `assets/`（模板、CSV），正文写“复制并填写”“只在……时查一行” |
| 模型已经知道的概念、重复的规则、动机性的句子 | 删掉 |

文件引用用相对 skill 根目录的路径，只引用一层深度（SKILL.md → references/x.md，不要再从 x.md 链到 y.md）。

另一个重点是测试设计。day-09 的输入把答案写进了摘要（例如自带“这是 breaking change”），所以原版和瘦身版都满分，测不出退化。今天的输入只给**原始 migration 文件**和最少的上下文（数据库类型、表大概多大），风险要由模型自己看出来。

**今天的起点：一个“什么都塞进 SKILL.md”的 skill**
把下面的内容原样保存为 `day-10/BEFORE/migration-safety-review/SKILL.md`（这是基线，之后不要再改它），再复制到 `day-10/migration-safety-review/` 进行重构。

````markdown
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
````

**任务步骤**
1. 保存 BEFORE 版，复制到 `day-10/migration-safety-review/`。用 day-09 的 `count_tokens.py` 记下 BEFORE 的元数据和正文 token。
2. 先写 `tests/PLAN.md`（在跑任何测试**之前**提交）：每段原文的去向表（正文 / references / assets / 删除，以及理由类别），以及测试用的检查清单。
3. 重构：
   - description 重写：做什么、何时用、至少两条排除边界（例如“写新的 migration”“优化慢查询”）。不要用 BEFORE 里 “whenever the user is working with databases” 这种宽泛触发。
   - `references/postgres.md`、`references/mysql.md`：各自数据库的规则；共有的规则（例如 expand/contract、未知表大小按大表处理）只保留一份，放在正文。
   - `assets/review-template.md`：输出结构；`assets/risk-matrix.csv`：把“Risk levels”那段文字变成可查的表（列建议：`table_size, operation_effect, risk`）。
   - 正文只保留流程、硬规则和“什么时候读/用哪个文件”。删掉模型已知的解释和 “Remember…” 重复列表。
4. 写 4 个行为输入 `tests/input-1.sql` ~ `input-4.sql`，每个开头只用一行注释给数据库类型和表规模（例如 `-- PostgreSQL 15, orders ≈ 40M rows`），**不写风险、不写建议**：
   - 1：PostgreSQL，看起来无害但有坑（例如在大表上 `ADD COLUMN ... DEFAULT clock_timestamp()`，或 `SET NOT NULL`）。
   - 2：PostgreSQL，多语句：一个 `CREATE INDEX CONCURRENTLY` 放在默认事务里 + 一个外键。
   - 3：MySQL 8.0，改列类型 + 加索引。
   - 4：完全安全的小改动（例如小表上加可空列），预期输出 Low、不制造假问题。
5. 每个输入跑三次，全部全新会话、普通提示词（例如 “Can you check this migration before I merge it?”）：BEFORE 版、重构版、无 skill 基线。输出原样保存为 `output-N-before.md`、`output-N-after.md`、`output-N-baseline.md`。用 harness 会话日志记录重构版每次读了哪些文件。
6. 3 个触发测试（只安装重构版，提示词不点名 skill、路径或“测试”）：T1 正向但措辞与 description 不同（例如 “is this ALTER going to take prod down?”）；T2 近似反例：请它**写**一个新的 migration；T3 反例：优化一个慢的 SELECT。证据由脚本从日志提取（可复用 day-07/08/09 的脚本）。
7. 写 `tests/RESULTS.md`（≤ 40 行）：BEFORE/AFTER 三层 token 表、12 次行为运行的检查结果（before / after / baseline 逐条）、每次读取的 references/assets、3 个触发结果，以及一段分析：哪个输入最能区分 before 和 after（或 skill 和 baseline），如果没有区分，说明下一次怎么改输入。

**交付物**
- `day-10/BEFORE/migration-safety-review/SKILL.md`（原样保存的起点，不修改）
- `day-10/migration-safety-review/SKILL.md`
- `day-10/migration-safety-review/references/postgres.md`、`references/mysql.md`
- `day-10/migration-safety-review/assets/review-template.md`、`assets/risk-matrix.csv`
- `day-10/migration-safety-review/tests/PLAN.md`
- `day-10/migration-safety-review/tests/input-1.sql` ~ `input-4.sql`
- `day-10/migration-safety-review/tests/output-N-before.md`、`output-N-after.md`、`output-N-baseline.md`（共 12 个）
- `tests/` 下的读取 / 触发日志证据和提取脚本
- `day-10/migration-safety-review/tests/RESULTS.md`
- （可选）`day-10/NOTES.md`

**完成标准**
1. BEFORE 版与题目给出的文本一致；重构版 `name` 与目录同名，description 为单行纯字符串，写明做什么、何时用、至少两条排除边界，且 token 少于 BEFORE；`agentskills validate`（或 `skills-ref validate`）通过并把输出记在 RESULTS.md 或 NOTES.md。
2. 重构版正文 token 比 BEFORE 少至少 50%（以 count_tokens.py 为准），且正文 ≤ 40 行；正文中没有某一个数据库专有的规则（如 `CONCURRENTLY`、`ALGORITHM=`）。
3. 单一来源：输出结构只在 review-template.md；风险等级规则只在 risk-matrix.csv（覆盖原文的全部情况，含“未知大小按大表”或在正文写明这一条）；共有规则只出现一次；每个 references/assets 文件在正文中都有相对路径、使用条件和用法动词，且只引用一层深度。
4. PLAN.md 的去向表覆盖 BEFORE 的每一个二级标题段落，并且提交时间早于任何 output 文件（git log 可见）。
5. 4 个输入只含 SQL 和一行数据库/规模注释，不含风险提示；CHECKLIST（写在 PLAN.md 中）每个输入 2-4 条可判断的检查项，至少一条检查 risk 等级，input-4 至少一条检查“没有虚构的 High/Medium 发现”。
6. 12 次运行都在全新会话中、普通提示词；输出原样保存；重构版的通过条数不少于 BEFORE 版。
7. 读取证据来自 harness 日志：PostgreSQL 输入没有读 mysql.md，MySQL 输入没有读 postgres.md。
8. 3 个触发测试提示词不提 skill 名称、路径或“测试”；T1 激活、T2 和 T3 不激活，证据由脚本提取。
9. RESULTS.md ≤ 40 行，包含 token 对比表和至少一段“区分度”分析。
10. skill 内容、references/assets、tests/ 下文档使用英文（NOTES.md 可以用中文）。

**预计用时**：约 40 分钟（阶段小结题，略长；12 次行为运行可以并行开会话）

**可选加分**
- day-09 遗留：在 day-09 的 CHECKLIST 里加 5c（type 为 `feat`，公开 API 变更不能是 `chore`），并在瘦身版 type 规则里补一句，重跑 input-5 slim。
- 给 risk-matrix.csv 写一个 10 行以内的校验脚本：检查表头、每个 `table_size × operation_effect` 组合恰好一行。
- 加一个 input-5：不写数据库类型、语句里也没有明显线索，预期是先问用户而不是猜。

**参考链接**
- [Agent Skills specification](https://agentskills.io/specification)（Progressive disclosure、File references：相对路径、一层深度）
- [Skill authoring best practices（Anthropic）](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)（Concise is key；Avoid deeply nested references）
- [PostgreSQL: CREATE INDEX — Building Indexes Concurrently](https://www.postgresql.org/docs/current/sql-createindex.html#SQL-CREATEINDEX-CONCURRENTLY)
- [PostgreSQL: ALTER TABLE（Notes）](https://www.postgresql.org/docs/current/sql-altertable.html)
- [MySQL 8.0: Online DDL Operations](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html)
