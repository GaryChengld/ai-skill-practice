# 练习进度记录

由教练维护。每个条目记录出题日期、交付物、完成标准，以及之后的检查和评审结果。

---

## day-01：Your First SKILL.md — a Conventional Commits writer

- 出题日期：2026-10-19
- 阶段：第一阶段 · 格式基础
- 状态：已完成，最终评分 5/5

**交付物**
- `day-01/conventional-commits/SKILL.md`
- `day-01/conventional-commits/TRIGGER-TESTS.md`
- （可选）`day-01/NOTES.md`

**完成标准**
1. 目录是 `day-01/conventional-commits/`，SKILL.md 以 YAML frontmatter 开头，只包含 `name` 和 `description`（可选字段今天不用）。
2. `name` 为 `conventional-commits`，与父目录同名，符合规范（小写字母/数字/连字符，1-64 字符，不以连字符开头或结尾，无连续连字符）。
3. `description` 不超过 1024 字符，同时说明"做什么"和"什么时候用"，包含用户可能说的关键词（如 commit message、git commit、staged changes、diff）。
4. 正文至少包含：步骤化指令（如何从 diff 推断 type / scope / subject）、允许的 type 列表、至少 2 个"输入 diff 摘要 → 输出 commit message"示例、至少 3 条边界情况（如 breaking change、改动混杂多个目的、diff 为空）。
5. 正文不超过 150 行，不依赖任何特定厂商的工具名或路径。
6. TRIGGER-TESTS.md 列出 5 条应触发和 5 条不应触发的提示词，其中不应触发的至少 2 条是"近似反例"（和 git/commit 相关但不该用这个 skill，如解释 git rebase、写 PR 描述）。
7. skill 内容全部使用英文。

**检查与评审**
- 2026-10-20 chat 评审：评分 4/5，7 条完成标准全部满足。主要建议：(1) 示例 3 用 `refactor!` 删除公开配置项，和自己对 refactor 的定义（不改变行为）矛盾，改成 `feat(config)!` 或调整定义；(2) description 补一句排除范围（PR 描述、changelog、release notes），并覆盖 "how should I word this commit" 这类说法；(3) 写明 `BREAKING CHANGE` 必须大写，50 字符是 git 惯例而非 Conventional Commits 规范；TRIGGER-TESTS.md 加一列实际结果并真实跑一遍。
- 2026-10-20 chat 复查：评分 5/5，上次 3 条建议全部改好（示例 3 改为 feat!、description 加排除范围、BREAKING CHANGE 大小写与 50 字符说明、语言规则、TRIGGER-TESTS 增加 Actual 列并记录了 10/10 的路由测试和局限）。新建议：路由测试只给了一个 skill，缺少竞争 skill，偏乐观；frontmatter 用了 `>-` 多行 description，可移植性上单行更稳。
- 2026-10-20 检查：复查之后没有新修改，确认已完成，最终评分 5/5。遗留建议（竞争 skill、单行 description）带入 day-02。

---

## day-02：Description Showdown — three descriptions for a release-notes skill

- 出题日期：2026-10-20
- 阶段：第一阶段 · 格式基础
- 针对弱点：day-01 路由测试没有竞争 skill；description 用了 `>-` 多行写法
- 状态：已出题，待完成

**交付物**
- `day-02/release-notes/SKILL.md`（frontmatter 用最终选中的 description，正文 ≤ 40 行）
- `day-02/release-notes/DESCRIPTIONS.md`（V1/V2/V3 三个版本及字符数）
- `day-02/release-notes/evals/trigger-queries.json`
- `day-02/release-notes/EVAL-RESULTS.md`
- `day-02/competitors/pr-description/SKILL.md`（竞争 skill 存根，只要 frontmatter + 几行正文）
- （可选）`day-02/NOTES.md`

**完成标准**
1. `name` 为 `release-notes`，与目录同名；frontmatter 只有 `name` 和 `description`；description 是单行纯字符串（不用 `>`、`>-`、`|`）。
2. DESCRIPTIONS.md 有 3 个版本并标出字符数：V1 只说“做什么”；V2 加“什么时候用”（祈使句 "Use this skill when..."）和用户意图关键词；V3 在 V2 基础上加排除范围（和 conventional-commits、pr-description 的边界）。都 ≤ 1024 字符。
3. trigger-queries.json 至少 16 条，每条有 `query`、`should_trigger`、`split`（train/validation），约 60/40 划分且两组都有正例和反例；正例至少 3 条不出现 "release notes" 字样；反例至少 5 条是近似反例，其中至少 2 条应路由到 conventional-commits、至少 2 条应路由到 pr-description。
4. 测试时同时提供至少 3 个 skill：release-notes、day-01 的 conventional-commits、pr-description 存根。EVAL-RESULTS.md 写明测试方法（平台/工具，或在全新会话中粘贴所有 skill 元数据让模型选择）。
5. EVAL-RESULTS.md 有表格：三个版本各自的 train 通过率，被选中版本的 validation 通过率；列出至少 2 条失败查询及原因分析；说明选中哪个版本、为什么，以及是否有过拟合迹象。
6. SKILL.md 正文 ≤ 40 行，至少包含：输入（commit/PR 列表或两个 tag 之间的范围）、按用户可感知的类别分组、跳过内部改动（chore/ci/test）的规则、1 个简短输出示例；不依赖特定厂商的工具名或路径。
7. skill 内容（SKILL.md、description、查询、结果说明）使用英文。

