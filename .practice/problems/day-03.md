# day-03：Calibrate the Body — rewrite a weak incident-postmortem skill

- 出题日期：2026-10-22

**学习目标**
- 判断正文里每一部分该给多少自由度（high / medium / low），按任务的脆弱程度来定严格程度
- 掌握几种好写法：给默认值而不是一串选项、绝对规则后面讲清原因、写 Gotchas 段落、给输出模板、加返回前的自检清单
- 识别几类坏写法：含糊、过度约束、自相矛盾、解释模型本来就懂的东西、让模型编造数据

**背景知识**
前两天主要练 description，决定的是 skill 什么时候被加载。今天练正文，决定的是加载之后模型做得好不好。agentskills.io 的最佳实践有几条核心观点：
1. **Match specificity to fragility**：任务容易出错、要求一致时就写死（例如时间格式）；有多种合理做法时给目标和理由，让模型自己判断（例如根因分析）。
2. **Provide defaults, not menus**：给一个默认做法，再简短提一句替代方案，不要罗列一堆同等地位的选项。
3. **Explain why**：讲清原因比全大写的 MUST 更有效，模型懂了目的，遇到规则没覆盖的情况也能判断对。
4. **Gotchas**：价值最高的内容往往是“模型不被提醒就一定会犯的错”。
5. **Add what the agent lacks**：不用解释什么是 incident 或 postmortem。
6. 输出格式用模板表达比用文字描述可靠，返回前加一个自检清单（validation loop）。

**任务步骤**
1. 把下面的糟糕版本原样存为 `day-03/incident-postmortem/BEFORE.md`：

```markdown
---
name: incident-postmortem
description: >
  Helps with incidents.
---
# Incident Postmortem Skill

An incident is an unplanned event that disrupts a service. Postmortems are documents written after incidents so teams can learn from them. They are very important in modern software engineering.

You MUST ALWAYS be thorough and write a high-quality postmortem. NEVER skip any section.

## Steps
1. Gather all the information about the incident.
2. Write the timeline. You can use local time, UTC, or relative times (T+5m), whichever you like.
3. Find the root cause. You could use 5 Whys, a fishbone diagram, fault tree analysis, or any other method.
4. Identify who caused the incident and what they should have done differently.
5. Write action items. ALWAYS write exactly 5 action items.
6. Make it sound professional.

## Format
Use sections: Summary, Impact, Timeline, Root Cause, Lessons Learned, Action Items, Appendix.
If any information is missing, fill it in with reasonable estimates so the document is complete.

Keep it short but cover everything in detail.
```

2. 把下面的测试输入原样存为 `tests/input-inc-482.md`：

```text
Slack export, #inc-482, 2026-10-14 (times in PT)
09:12 alert: checkout p95 latency 8s, error rate 23%
09:15 maria: I'm on it
09:21 maria: looks like db connection pool exhausted on orders-db
09:30 dev: rolled back deploy 7f3a (added retry loop to payment client)
09:34 errors dropping
09:41 all green
customers affected: ? maybe ~1.2k failed checkouts, finance to confirm
q: why didn't canary catch it? -> canary is only 2% traffic for 5 min
```

3. 在 `REWRITE-NOTES.md` 里找出 BEFORE 的问题（至少 6 个），逐条标类别并写出你的修改。
4. 重写 `SKILL.md`。写之前先想清楚哪些部分该写死、哪些该放开，并把这个划分写进 REWRITE-NOTES.md 的自由度表。
5. 开两个全新会话，分别只提供 BEFORE.md 和新的 SKILL.md，加上同一个输入，让模型写 postmortem。输出分别存为 `tests/output-before.md` 和 `tests/output-after.md`，再写一份简短的 `COMPARISON.md`。

**交付物**（都放在 `day-03/incident-postmortem/` 下）
- `BEFORE.md`
- `SKILL.md`
- `REWRITE-NOTES.md`
- `tests/input-inc-482.md`
- `tests/output-before.md`、`tests/output-after.md`
- `tests/COMPARISON.md`
- （可选）`day-03/NOTES.md`

**完成标准**
1. `name` 为 `incident-postmortem`，和目录同名；frontmatter 只有 `name` 和 `description`，description 是单行纯字符串；要同时写清做什么、什么时候用，包含 postmortem、post-incident review、RCA、outage 等关键词，并至少排除一个边界（例如正在进行的事故处置、给客户看的状态页更新）。
2. BEFORE.md 和上面给出的版本一致。
3. REWRITE-NOTES.md 至少列出 6 个问题，每个都标上类别（vague / over-constrained / menu-without-default / contradiction / known-to-agent / invents-data / missing-why）并写明修改；另附一张表，把新正文的每个部分标为 high、medium 或 low freedom，各写一句理由。
4. SKILL.md 正文不超过 80 行，包含以下内容：
   - 输出模板
   - 时间线只有一个默认格式（UTC），根因分析有一个默认方法（可以简短提一句替代方法）
   - blameless 规则，并说明原因
   - 缺失的信息标为 Unknown 或 TBD，不能编造
   - 行动项带 owner、截止日期和类型，数量由分析结果决定，不是固定数字
   - 至少 3 条 Gotchas
   - 返回前的自检清单
   - 至少 3 个边界情况（例如事故仍在进行、涉及安全敏感细节、信息来源互相矛盾）
5. 不出现没有理由的全大写 MUST、NEVER、ALWAYS：每条绝对规则后面都写原因。
6. 两次测试都在全新会话里跑，输出保存在 tests/ 下。COMPARISON.md 不超过 20 行，至少比较四点：时区处理、有没有指责个人的措辞、有没有编造数字（约 1.2k 次失败结账）、行动项数量。
7. skill 内容（SKILL.md、REWRITE-NOTES、COMPARISON）用英文写；REWRITE-NOTES.md 不超过 60 行。

**预计用时**：约 30 分钟（找问题 8 分钟、重写 12 分钟、两次测试加对比 10 分钟）。这次文档有行数上限，就是为了练时间盒。

**可选加分项**
- 在输入里故意加一条互相矛盾的信息（例如另一个人说 09:38 才恢复），看新 skill 会不会把矛盾标出来，而不是悄悄选一个。
- 换一个小一些的模型跑 after 版本，看指令是否依然够用。
- 把输入里的时间换算成 UTC 时，留意 10 月 14 日太平洋时间是 PDT（UTC−7）还是 PST。这正好可以写成一条 Gotcha。

**参考链接**
- [Best practices for skill creators（agentskills.io）](https://agentskills.io/skill-creation/best-practices.md)：重点读 Calibrating control 和 Patterns for effective instructions 两节
- [Skill authoring best practices（Claude 文档）](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)：Set appropriate degrees of freedom 和 Examples pattern
- [Agent Skill best practices（Gemini CLI）](https://geminicli.com/docs/cli/skills-best-practices/)：其他平台对自由度的写法，可以对照看
