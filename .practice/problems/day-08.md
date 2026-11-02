# day-08：Ship the Template, Not the Prose — assets/ for an on-call handoff skill

- 出题日期：2026-11-02
- 阶段：第二阶段 · 渐进式披露（第 3 题：assets/ 的使用）

**学习目标**
- 区分 references/ 和 assets/：前者是“读了之后改变做法”的知识，后者是“拿来用”的材料（复制的模板、查一行的表、用来校验的 schema）。
- 让输出结构、判定规则、数据字段各自只有一个来源，正文只说“何时用哪个 asset、怎么用”。
- 测试 asset 的按需使用和信息不足时不猜。

**背景知识**
Agent Skills 规范把可选目录分成三类：scripts/（可执行代码）、references/（按需阅读的文档）、assets/（静态资源：文档或配置模板、图片、数据文件，如查找表和 schema）。三者都按需加载，引用时用相对 skill 根目录的路径，只保持一层深度。

关键区别在于“用法”：
- **模板**：智能体复制骨架再填写，而不是读完后凭记忆重写，所以标题、顺序、占位符应完全保留。把模板放进 assets/ 后，正文就不用再贴一遍完整模板（day-03 到 day-07 的输出模板都写在正文里）。
- **查找表**（CSV）：确定性规则写成数据，智能体只查需要的那一行；改规则只需改表，不改指令。
- **Schema**（JSON Schema）：定义机器可读输出的字段、类型和必填项，可以用校验器检查输出，比“请输出合法 JSON”可靠得多。

今天的 skill 是值班交接（on-call handoff）：把一个班次的告警、未关闭事项和注意事项整理成给下一位值班工程师的交接单。默认输出 Markdown；下游机器人需要时输出 JSON。

**任务步骤**
1. 新建 `day-08/oncall-handoff/`，写 SKILL.md：单行 description（做什么、何时用、排除边界，如 postmortem 或排班表），以及 ≤ 50 行的正文：输入要求、证据规则（只用输入中的事实，缺的写 Unknown）、asset 使用规则、返回前自检。
2. 写 `assets/handoff-template.md`：固定标题（例如 Shift summary / Open items / Watch list / Recently resolved / Open questions）和占位符（如 `<service>`、`<SEV1-SEV4 or Unknown>`）。
3. 写 `assets/severity-matrix.csv`：列为 `impact,urgency,severity`，覆盖全部组合，例如 impact ∈ {all-users, some-users, internal-only}，urgency ∈ {worsening, stable, no-current-impact}。
4. 写 `assets/handoff.schema.json`（draft 2020-12）：字段与模板对应，`required`、severity `enum`（SEV1-SEV4、Unknown）、`additionalProperties: false`。
5. 在正文中写明使用条件和用法，例如：
   `Copy assets/handoff-template.md and fill every placeholder; keep headings and their order.`
   `If an open item has no declared severity, look up one row in assets/severity-matrix.csv by impact and urgency. If either value is missing, use Unknown and add an open question.`
   `Only when the user asks for JSON, produce output that validates against assets/handoff.schema.json.`
6. 自己写 4 个输入 A/B/C/D（要求见完成标准第 5 条），各开一个全新会话，用普通请求（如 “I'm ending my shift, can you write the handoff from these notes?”）。从 harness 日志中提取实际打开的文件。
7. 用 JSON Schema 校验器（如 `check-jsonschema --schemafile assets/handoff.schema.json tests/output-c.json`，或 Python `jsonschema`）校验 C 的输出；检查 A/B/D 的标题是否与模板一致。写 ASSETS.md；如有多读、漏读或模板被改写，修改正文措辞后重跑。

**交付物**
- `day-08/oncall-handoff/SKILL.md`
- `day-08/oncall-handoff/assets/handoff-template.md`、`handoff.schema.json`、`severity-matrix.csv`
- `day-08/oncall-handoff/tests/input-a.md`、`input-b.md`、`input-c.md`、`input-d.md`
- `day-08/oncall-handoff/tests/` 下原样保存的输出（`output-a.md`、`output-b.md`、`output-c.json`、`output-d.md`）
- `day-08/oncall-handoff/tests/ASSETS.md`
- `tests/` 下的读取证据和提取脚本
- （可选）`day-08/NOTES.md`

**完成标准**
1. 目录为 `day-08/oncall-handoff/`；`name` 与目录同名；description 单行纯字符串，写明做什么、何时用、至少一条排除边界（如写事故复盘 postmortem、制定值班排班表）；`agentskills validate` 通过。
2. SKILL.md 正文 ≤ 50 行，不含 references/ 目录；每个 asset 用相对路径引用并带使用条件和用法动词：模板“复制并填写、保持标题和顺序”，查找表“只在缺少已声明严重级别时查一行”，schema“只在请求 JSON 时使用并按它校验”。
3. 单一来源：输出结构只存在于 handoff-template.md（正文不重复完整模板）；严重级别规则只存在于 severity-matrix.csv（正文不写“全站故障=SEV1”之类的规则）；JSON 字段只定义在 schema 中。
4. 三个 asset 都是可直接使用的数据而不是说明文：模板含占位符和固定标题；CSV 有表头、覆盖 impact × urgency 的全部组合（至少 3×3）；schema 使用 draft 2020-12，含 `required`、severity 的 `enum`（含 Unknown）和 `additionalProperties: false`。
5. tests/ 下 4 个自己编写的输入（每个 8-20 行，服务名、人名、工单号前后一致，用全名不用简写）：A 所有事项都已声明严重级别、要 Markdown（预期只用模板）；B 有一项没有严重级别但给出了 impact 和 urgency（预期模板 + 查找表，输出级别与 CSV 那一行一致）；C 要 JSON 给机器人用（预期用 schema，输出通过 JSON Schema 校验器）；D 有一项缺 urgency（不应猜级别：输出 Unknown 并列入待确认问题）。
6. 每个输入在全新会话中运行，加载磁盘上的原始 skill 文件夹，提示词是普通请求、不提“测试/加载”；读取证据由脚本从 harness 会话日志中提取。
7. ASSETS.md ≤ 30 行：表格列出输入、预期打开的 asset、实际打开（来自日志）、是否通过；B 写出查到的 CSV 行和输出级别；C 写出校验命令和结果；A/B/D 的输出标题与模板标题逐个、按顺序一致；至少一段分析 asset 多读/漏读或模板被改写的情况，以及对正文措辞的修改。
8. skill 内容、assets 和 tests/ 下文档使用英文。

**预计用时**：约 35 分钟（3 个 asset 都很短；提取脚本可复用 day-07 的）

**可选加分**
- 加一个输入 E：用户要 JSON，但有一项缺 impact，验证 JSON 中 severity 为 "Unknown" 且仍通过校验。
- 修改 CSV 中的一行（如 some-users × worsening 从 SEV2 改为 SEV1），不改 SKILL.md 重跑 B，确认输出跟着表变化，证明规则确实只来自数据。
- day-07 遗留：把 input-h 的简写包名改成全名；在 dependency-fix-plan 正文里允许“归属未确定时只输出 Ownership + Open questions”的简短形式。

**参考链接**
- [Agent Skills specification](https://agentskills.io/specification)（Optional directories：assets/；File references）
- [Skill authoring best practices（Anthropic）](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)（Template pattern；Progressive disclosure）
- [JSON Schema: Getting started（draft 2020-12）](https://json-schema.org/learn/getting-started-step-by-step)
- [check-jsonschema](https://check-jsonschema.readthedocs.io/)
- [Python jsonschema](https://python-jsonschema.readthedocs.io/)
