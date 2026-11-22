# day-09：Pay for What You Load — a context budget audit and a slimmer conventional-commits

- 出题日期：2026-11-22
- 阶段：第二阶段 · 渐进式披露（第 4 题：上下文预算）

**学习目标**
- 把渐进式披露的三层（元数据 / 正文 / 资源）量化成 token 数，知道每一层什么时候付费、付给谁。
- 学会“删”：去掉模型本来就知道的内容、重复的规则和过长的示例，而不是只把内容搬到别的文件。
- 用前后对比证明瘦身没有让行为变差：同样的输入，原版和瘦身版输出都满足同一份检查清单；description 变短后正向触发和排除边界都还成立。

**背景知识**
Agent Skills 规范给出的预算大致是：元数据（name + description）约 100 token，在启动时为**每一个**已安装的 skill 加载；正文建议少于 5000 token、500 行以内，只在 skill 被激活时加载；scripts/、references/、assets/ 只在需要时读取。所以三层的“价格”不一样：
- **元数据**的成本乘以 skill 数量，而且每次对话都付。装 50 个 skill 时，每个 description 多 40 token 就是 2000 token 的常驻开销，还会让 description 之间更难区分。
- **正文**只在激活时付，但会和用户的代码、日志一起竞争注意力。上限是 5000 token，不代表应该写到 5000。
- **资源**按需读取，但读一次就付全价，所以一个经常被读的 references 文件实际上和正文一样贵。

Anthropic 的最佳实践有一句很实用的检查：对每一段问“模型真的需要这段解释吗？”。最常见的浪费有：解释模型已经知道的概念（比如 Conventional Commits 是什么）、同一规则在步骤和边界情况里各写一遍、示例过长或过多、礼貌性和动机性的句子。

token 计数没有统一标准，不同模型的分词器不同。今天可以用三种方法中的任意一种，在 BUDGET.md 里写明用的是哪一种：字符数 ÷ 4 的粗略估计；`tiktoken`（如 `o200k_base` 编码）；或 Anthropic 的 count tokens API（`/v1/messages/count_tokens`）。重点是用同一种方法前后对比。

今天的瘦身对象是你在 day-01 写的 `conventional-commits`：它是你最早的 skill，正文 98 行，是目前最长的。

**任务步骤**
1. 写 `day-09/tests/count_tokens.py`：扫描仓库里所有 `SKILL.md`（跳过 `tests/` 目录），对每个 skill 分别统计元数据（frontmatter 的 name + description）、正文（frontmatter 之后的内容）、每个资源文件的 token 数，输出 Markdown 表格。脚本只用参数传入的根目录，不写死路径。
2. 运行脚本，写 `day-09/BUDGET.md`：全部 skill 的表格、元数据总和（相当于全部装上时的常驻成本）、计数方法，以及你给自己定的预算（例如：description ≤ 60 token，正文 ≤ 1000 token）。指出哪些 skill 超出预算。
3. 把 `day-01/conventional-commits/` 复制到 `day-09/conventional-commits/`（原版不动，用来对比），对副本瘦身：正文 token 减少至少 35%，description 也要缩短但保留触发关键词和排除边界。每删一类内容，在 `day-09/conventional-commits/tests/CUTS.md` 记一行：删了什么、为什么可以删（模型已知 / 重复 / 示例过多 / 其他）。
4. 写 4 个行为输入 `tests/input-1.md` ~ `input-4.md`（每个是一段 diff 摘要或 `git diff --stat` 加几行改动，覆盖：普通 feat 或 fix、breaking change、混杂多个目的的改动、空 diff 或只有空格变化），再写一份 `tests/CHECKLIST.md`：每个输入 2-4 条可判断的检查项（例如 “type is `fix`”、“footer contains `BREAKING CHANGE:`”、“asks to split the commit”）。检查清单要在跑测试**之前**写好。
5. 每个输入分别用原版（day-01）和瘦身版（day-09）各跑一次，全新会话、普通提示词；输出原样保存为 `output-N-original.md` 和 `output-N-slim.md`。
6. 写 3 个触发测试，提示词都**不点名** skill 和路径，在只安装瘦身版的环境中跑：T1 正向（例如 “Here's my staged diff, what should the commit say?”）；T2 近似反例：要写 PR description；T3 反例：要写 release notes。从 harness 日志中提取 skill 是否被激活（可复用 day-07/day-08 的 collect-harness.py）。
7. 写 `tests/RESULTS.md`：瘦身前后 token 对比、8 次行为运行的检查结果（原版 vs 瘦身版逐条对比）、3 个触发测试结果，以及至少一段分析：哪一处删减最“危险”、有没有引起行为退化，如果有，你加回了什么（加回后的 token 数也要写）。

**交付物**
- `day-09/tests/count_tokens.py`
- `day-09/BUDGET.md`
- `day-09/conventional-commits/SKILL.md`（瘦身版；如确有必要可加 references/，但要在 CUTS.md 说明理由）
- `day-09/conventional-commits/tests/CUTS.md`
- `day-09/conventional-commits/tests/input-1.md` ~ `input-4.md`、`CHECKLIST.md`
- `day-09/conventional-commits/tests/output-N-original.md`、`output-N-slim.md`（共 8 个）
- `day-09/conventional-commits/tests/` 下 3 个触发测试的提示词、日志证据和提取脚本
- `day-09/conventional-commits/tests/RESULTS.md`
- （可选）`day-09/NOTES.md`

**完成标准**
1. `count_tokens.py` 可以用 `python3 day-09/tests/count_tokens.py <repo-root>` 直接运行，不写死路径，跳过 `tests/` 目录；按 skill 输出元数据、正文、每个资源文件三层的 token 数。
2. BUDGET.md 包含全部 skill（含 day-02 的 competitors）的表格、元数据总和、写明的计数方法、自定预算，以及超出预算的 skill 列表。
3. `day-09/conventional-commits/`：`name` 与目录同名，description 为单行纯字符串，仍写明做什么、何时用、至少一条排除边界（PR description / changelog / release notes），且 token 数少于原版；`agentskills validate` 通过；`day-01/` 下的原版没有被修改。
4. 瘦身版正文 token 比原版少至少 35%（以 count_tokens.py 的输出为准），并且仍保留：允许的 type 列表、breaking change 的写法、多目的改动和空 diff 的处理规则。
5. CUTS.md 每一行写明删除的内容和理由类别；至少有一行属于“模型已知”、一行属于“重复”。
6. 4 个行为输入覆盖普通改动、breaking change、多目的改动、空 diff / 空白改动；CHECKLIST.md 每个输入 2-4 条检查项，且提交时间早于输出文件（git log 可见，或写在同一次提交中并在 RESULTS.md 声明是先写的）。
7. 8 次行为运行都在全新会话中、普通提示词、加载磁盘上的 skill 文件夹；输出原样保存；RESULTS.md 逐条列出原版和瘦身版的检查结果，瘦身版的通过条数不少于原版。
8. 3 个触发测试的提示词不提 skill 名称、路径或“测试”；T1 激活、T2 和 T3 不激活，证据由脚本从 harness 会话日志提取。
9. RESULTS.md ≤ 40 行，包含前后 token 对比和至少一段“最危险的删减”分析。
10. skill 内容、tests/ 下文档使用英文（BUDGET.md 和 NOTES.md 可以用中文）。

**预计用时**：约 35 分钟（脚本约 30 行；行为运行可以并行开会话）

**可选加分**
- day-08 遗留：把 `handoff.schema.json` 里 `watch_list` / `recently_resolved` 从自由字符串改成对象（例如 `{ticket, service, note}`，`additionalProperties: false`），重跑 C 和 E 并通过校验。
- 用两种计数方法（如字符 ÷ 4 和 tiktoken）跑同一张表，在 BUDGET.md 写一句两者差多少。
- 对 BUDGET.md 里另一个超预算的 skill 只做 description 瘦身，并跑一次正向 + 一次近似反例触发测试。

**参考链接**
- [Agent Skills specification](https://agentskills.io/specification)（Progressive disclosure：元数据约 100 token、正文建议 < 5000 token、SKILL.md 500 行以内）
- [Skill authoring best practices（Anthropic）](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)（Concise is key；Default assumption: Claude is already very smart）
- [Anthropic token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)
- [tiktoken](https://github.com/openai/tiktoken)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
