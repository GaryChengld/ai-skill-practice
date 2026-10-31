# day-06：Split the Body — progressive disclosure for incident-postmortem

- 出题日期：2026-10-25
- 阶段：第二阶段 · 渐进式披露（第 1 题）

**学习目标**
- 分清哪些内容每次都要加载、该留在正文，哪些是条件性的细节、该放进 `references/`。
- 写出明确的加载条件，让智能体只在需要时打开对应文件。
- 用会话记录验证参考文件确实被按需读取：该读的读了，不该读的没读。

**背景知识**
Agent Skills 规范定义了三层加载：
1. **元数据**（约 100 tokens），启动时为所有 skill 加载。
2. **正文**（建议 < 5000 tokens），skill 被触发时加载。
3. **`scripts/`、`references/`、`assets/` 里的资源**，只在需要时加载。

规范还要求：SKILL.md 控制在 500 行以内；引用其他文件用“相对 skill 根目录”的路径；引用只保持一层深度，也就是正文 → 参考文件，不要再从参考文件链到别的参考文件。Anthropic 的最佳实践补充了两点：超过 100 行的参考文件开头要放目录，因为智能体可能只读文件的前一部分；正文里要写清楚“什么情况下读哪个文件”，而不是只列一个文件清单。

day-03 的 incident-postmortem 正文 72 行，里面有一些规则只对部分事故有用：时区换算 Gotchas、因果树这种替代 RCA 方法、敏感信息处理。这正是渐进式披露要处理的情况。先在这些地方补充更多细节，再把它们拆出去。

**任务步骤**
1. 把 `day-03/incident-postmortem/` 复制到 `day-06/incident-postmortem/`，day-03 保持原样。删掉复制过来的 BEFORE.md、REWRITE-NOTES.md 和旧的 tests/。
2. 新建三个参考文件，每个文件只讲一个主题：
   - `references/timezones.md`：把时区相关的 Gotchas 移过来，再补上 DST 切换时“不存在的本地时间”（春季跳过的那一小时）和“重复的本地时间”（秋季重复的那一小时）怎么处理。
   - `references/rca-methods.md`：写默认的 5 Whys 怎么做、什么时候切换到因果树，再加一个因果树的完整小例子。例子的领域不能是结账/支付。
   - `references/sensitive-incidents.md`：泄露凭证或客户数据时，写清楚要脱敏的内容清单、怎么引用受限证据，以及文档对外分发前需要谁审阅。
3. 把正文压缩到 ≤ 55 行。在需要的位置加上加载条件，例如：
   `Read references/timezones.md when source times use more than one timezone, a named local zone, or fall near a DST change.`
4. 自己写 3 个测试输入，每个 10-25 行即可：
   - A：只需要正文（全部 UTC、单一时区、无敏感信息）
   - B：跨时区，且有事件落在 DST 切换附近
   - C：涉及泄露的 API key 或客户数据
5. 每个输入都在全新会话中运行，加载磁盘上的原始 skill 文件夹（放进 `.claude/skills/` 或 `.agents/skills/` 之类的发现目录，或者在支持 SKILL.md 的工具里直接安装）。然后从会话记录或工具调用日志里看实际打开了哪些参考文件。
6. 写 LOADING.md，记录结果。如果有多读或漏读，修改加载条件的措辞后重跑。

**交付物**
- `day-06/incident-postmortem/SKILL.md`
- `day-06/incident-postmortem/references/timezones.md`
- `day-06/incident-postmortem/references/rca-methods.md`
- `day-06/incident-postmortem/references/sensitive-incidents.md`
- `day-06/incident-postmortem/tests/input-a.md`、`input-b.md`、`input-c.md`
- `day-06/incident-postmortem/tests/LOADING.md`
- （可选）`day-06/NOTES.md`

**完成标准**
1. 目录为 `day-06/incident-postmortem/`，day-03 原样保留；`name` 与目录同名；description 是单行纯字符串；`agentskills validate` 通过。
2. SKILL.md 正文 ≤ 55 行，并且仍包含每次都需要的内容：证据规则、blameless 规则、行动项规则、输出模板、返回前自检。
3. 每个参考文件都在正文里用相对路径（`references/<file>.md`）引用，并带明确的加载条件（“Read … when …”）。正文没有“先读完所有参考文件”之类的指令。参考文件之间不互相引用。
4. 每个参考文件 30-120 行，只讲一个主题；超过 100 行的开头有目录。每个文件至少有一项 day-03 里没有的新内容。
5. 每条规则只写在一个地方：正文和参考文件之间没有重复规则，正文只用一句话指向参考文件。参考文件里的例子不用 INC-482 结账场景，也不和 tests/ 的输入同题。
6. 3 个测试输入由你自己编写，分别覆盖 A/B/C 三种情况；每个都在全新会话中跑，加载的是原始文件夹，不手工转写。
7. LOADING.md ≤ 30 行，包含三部分：
   - 一张表：输入、预期加载的文件、实际打开的文件（以会话记录为依据）、是否通过。
   - 各层大小：description 字符数、正文行数和约 tokens、每个参考文件的约 tokens（按字符数 ÷ 4 估算）。
   - 至少一段分析：哪里多读或漏读了，你对加载条件的措辞做了什么修改。
8. skill 内容和 tests/ 下的文档使用英文。

**预计用时**：约 30-35 分钟

**可选加分**
- 加一个输入 D，同时需要两个参考文件（例如跨 DST 的数据泄露事故），验证两个文件都会被加载。
- 顺手修正 day-04 的 Edge cases 措辞，改成：`hold for owner review; do not recommend deletion.`
- 在 NOTES.md 里写 2-3 句：如果改用 Codex 或 Copilot，怎么确认它读了哪个参考文件？

**参考链接**
- [Agent Skills specification](https://agentskills.io/specification)（Progressive disclosure、File references 两节）
- [Skill authoring best practices（Anthropic）](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)（参考文件目录、避免深层引用）
- [IANA Time Zone Database](https://www.iana.org/time-zones)（DST 规则）
