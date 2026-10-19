# 练习进度记录

由教练维护。每个条目记录出题日期、交付物、完成标准，以及之后的检查和评审结果。

---

## day-01：Your First SKILL.md — a Conventional Commits writer

- 出题日期：2026-10-19
- 阶段：第一阶段 · 格式基础
- 状态：已出题，待完成

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
