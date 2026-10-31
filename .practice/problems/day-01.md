# day-01：Your First SKILL.md — a Conventional Commits writer

- 出题日期：2026-10-19

**学习目标**
- 掌握 SKILL.md 的基本结构：YAML frontmatter 加 Markdown 正文
- 学会写一个同时说明"做什么"和"什么时候用"的 description
- 开始养成为 skill 写触发测试的习惯

**背景知识**
按照开放的 Agent Skills 规范，skill 是一个文件夹，至少包含一个 `SKILL.md`。frontmatter 里只有 `name` 和 `description` 是必填的：
- `name`：1-64 字符，只能用小写字母、数字和连字符，不能以连字符开头或结尾，不能有连续的 `--`，并且**必须和父目录同名**。
- `description`：1-1024 字符，要写清楚 skill 做什么、什么时候用，并带上用户可能说的关键词。

智能体启动时只加载每个 skill 的 name 和 description（大约 100 token），并据此决定是否激活这个 skill；激活后才读取整个正文。所以 description 决定了能不能触发，正文决定了做得好不好。Cursor、Codex、Claude Code 等工具都能从 `.agents/skills/`、`.claude/skills/` 这类目录发现同一种格式的 skill。

**任务步骤**
1. 新建 `day-01/conventional-commits/SKILL.md`。这个 skill 的作用是：根据 git diff 或暂存区的改动，写出符合 Conventional Commits 规范的提交信息（`type(scope): subject`，可选 body 和 footer）。
2. frontmatter 只写 `name` 和 `description`。写 description 时想清楚：用户会怎么说？比如 "write a commit message"、"commit these changes"、"what should my commit message be"。
3. 正文写给智能体看，用祈使句。至少包括：
   - 步骤：怎么读 diff，怎么推断 type、scope 和 subject
   - 允许的 type 列表（feat、fix、docs、refactor 等）及各自何时使用
   - subject 的规则，例如祈使语气、长度上限、结尾不加句号
   - 至少 2 个 "diff 摘要 → commit message" 示例
   - 至少 3 条边界情况，例如 breaking change（`!` 或 `BREAKING CHANGE:` footer）、一次改动混了多个目的、diff 为空
4. 新建 `day-01/conventional-commits/TRIGGER-TESTS.md`，列出 5 条应触发、5 条不应触发的提示词，每条附一句理由。

**交付物**
- `day-01/conventional-commits/SKILL.md`
- `day-01/conventional-commits/TRIGGER-TESTS.md`
- （可选）`day-01/NOTES.md`

**完成标准**
1. 目录是 `day-01/conventional-commits/`，SKILL.md 以 YAML frontmatter 开头，只包含 `name` 和 `description`。
2. `name` 为 `conventional-commits`，与父目录同名，符合命名规则。
3. `description` 不超过 1024 字符，同时说明"做什么"和"什么时候用"，包含 commit message、git commit、staged changes、diff 这类关键词。
4. 正文包含步骤化指令、type 列表、至少 2 个示例、至少 3 条边界情况。
5. 正文不超过 150 行，不依赖任何特定厂商的工具名或路径。
6. TRIGGER-TESTS.md 有 5 条应触发和 5 条不应触发的提示词，其中不应触发的至少 2 条是近似反例，比如"解释 git rebase"或"帮我写 PR 描述"。
7. skill 内容全部使用英文。

**预计用时**：约 30 分钟

**可选加分项**
- 把 skill 复制到 `~/.agents/skills/` 或 `~/.claude/skills/`，在你常用的工具里真实提交一次，看它有没有被触发，把结果写进 NOTES.md。
- 安装 [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref)，运行 `skills-ref validate day-01/conventional-commits`。

**参考链接**
- [Agent Skills Specification](https://agentskills.io/specification)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Cursor: Agent Skills（skill 发现目录）](https://www.cursor.com/docs/context/skills)
