# day-05：Stage Review — what the validator catches, and what it doesn't

- 出题日期：2026-10-24

**学习目标**
- 会用官方参考校验器检查 skill，并知道它的覆盖范围在哪里结束。
- 把“规范合法”和“写得好”分开：自己定义一套校验器不管的质量检查。
- 第一次把全部 skill 放进同一个目录做路由，找出 skill 之间互相抢触发的地方。
- 把前几题积压的遗留建议清掉。

**背景知识**
- 参考实现 `skills-ref` 目前在 PyPI 上是 0.1.1，**安装后的命令名是 `agentskills`**，不是 `skills-ref`。它有三个子命令：`validate`、`read-properties`、`to-prompt`。`to-prompt` 可以一次接收多个目录，生成平台注入系统提示词的那段 `<available_skills>` XML，也就是路由时模型真正看到的全部内容。
- 出题时实测：现有的 5 个 skill 目录全部 `Valid`。但是“通过校验”只说明规范意义上合法。校验器会拦一部分错误，也会漏一部分。到底拦哪些、漏哪些，请你自己测出来。
- 规范只允许 6 个 frontmatter 字段，所以某个平台的专有字段放进 frontmatter 会让校验失败。这一点和第五阶段的可移植性直接相关。

**任务步骤**
1. 建一个虚拟环境，运行 `pip install skills-ref`，然后对 5 个 skill 目录（包括 pr-description 存根）跑 `agentskills validate`。
2. 从 day-04 的 INVALID-EXAMPLES 里挑至少 4 个片段，分别放进临时目录（不要提交）逐个验证，记下哪些被拦截、哪些漏过。
3. 定义至少 6 项校验器不覆盖的质量检查，给 5 个 skill 逐项打 Pass / Fail / N/A。
4. 按审计结果修复旧 skill，必须包括以下三处：
   - day-01：description 从 `>-` 改成单行纯字符串。
   - day-03：Actions 里的示例换成和 INC-482 测试输入无关的领域。
   - day-04：补上“分支与 baseline 同一提交、没有独有提交”这个边界情况，或者用新正文重跑 smoke，两者选一个或都做。
5. 修复后重新跑 validate，再运行 `agentskills to-prompt <5 个目录> > day-05/catalog.xml`。
6. 开一个全新会话，只粘贴 catalog.xml，然后逐条问模型“该用哪个 skill，还是都不用”，把结果记进 ROUTING.md。

**交付物**
- `day-05/VALIDATION.md`
- `day-05/AUDIT.md`
- `day-05/catalog.xml`
- `day-05/ROUTING.md`
- day-01、day-03、day-04 里的原地修复
- （可选）`day-05/NOTES.md`

**完成标准**
1. VALIDATION.md 不超过 40 行，写明工具名、版本和安装命令，贴出修复后 5 个目录的 validate 结果，并用一张表列出至少 4 个错误片段是被拦截还是漏过。另用 2-3 句说明这个覆盖范围意味着什么。
2. AUDIT.md 不超过 40 行，用一张表覆盖 5 个 skill × 至少 6 项质量检查，比如单行 description、有 “Use when”、有排除边界、正文行数、没有厂商专有工具名或路径、绝对规则带理由、示例不和测试输入同题、遗留建议已处理。
3. 至少 3 处修复，分布在至少 2 个旧 skill 中，并且包含第 4 步要求的三处。AUDIT.md 的 Fixes 部分逐条写出提交哈希和一句说明。修复后 validate 仍然全部通过，各题原来的行数上限也不能被突破。
4. catalog.xml 是对修复后 5 个 skill 运行 `to-prompt` 的原始输出。
5. ROUTING.md 不超过 30 行，至少 10 条查询，满足以下要求：
   - 至少 5 条是目录内两个 skill 之间的近似混淆，比如 changelog 和 commit message、release notes 和 PR description、清理分支和写 commit。
   - 至少 2 条应当不触发任何 skill。
   - 表格有 expected、actual、pass 三列。
   - 至少分析 1 条失败或最接近失败的查询，并说明 description 要不要改。
6. skill 内容和 day-05 下的所有文档都用英文。

**预计用时**：约 30-35 分钟。修复部分只做最小改动，不要借机重写。

**可选加分**
- 写一个 `day-05/lint.py`，把审计里 2-3 项机械检查自动化，比如是否为单行 description、是否含 “Use when”、正文行数。这算是第三阶段配套脚本的预热。
- 把 catalog.xml 的字符数除以 4，粗略估算元数据层的 token，看看 5 个 skill 一共占多少。这是第二阶段上下文预算的预热。

**参考链接**
- [Agent Skills specification](https://agentskills.io/specification)
- [skills-ref (agentskills/agentskills)](https://github.com/agentskills/agentskills/tree/main/skills-ref)
- [skills-ref on PyPI](https://pypi.org/project/skills-ref/)
