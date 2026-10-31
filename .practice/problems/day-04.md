# day-04：Optional Frontmatter Fields — a stale-branch report skill

- 出题日期：2026-10-23

**学习目标**
- 掌握 4 个可选字段 `license`、`compatibility`、`metadata`、`allowed-tools` 的合法写法和各自的取舍
- 理解 `allowed-tools` 只是“预批准”，不是“限制”，所以安全规则必须写在正文里
- 让正文示例和测试场景互不重叠，避免评测污染

**背景知识**（来自 agentskills.io 规范，出题时已核对）
- `license`：写许可证名称，或指向同目录的许可证文件，例如 `MIT. See LICENSE.txt`。尽量短。
- `compatibility`：1-500 字符，只在确实有环境要求时写，比如需要哪些系统包、是否要联网、面向哪个产品。规范原话是 “Most skills do not need it”。
- `metadata`：键和值都必须是字符串，所以版本号要写成 `"1.0"`。键名尽量取得独特一些，避免和客户端自己的字段冲突。
- `allowed-tools`：空格分隔的**字符串**，属于实验字段，各客户端支持程度不同。在 Claude Code 里它只表示“这些工具不用再问权限”，并不会禁止其他工具。GitHub Copilot 的文档也警告不要随意预批准 shell。工具名的写法因客户端而异，比如 `Bash(git log:*)` 是 Claude Code 的语法，所以这个字段天然不可移植。规范示例里的 `Bash(git:*)` 范围太宽，会把 `git branch -D` 和 `git push --delete` 也一并放行。
- Copilot 文档只列出 name、description、license 三个字段，客户端遇到不认识的字段一般会忽略。所以每个可选字段都要问一句：如果客户端忽略它，会发生什么？

**任务步骤**
1. 写一个 skill：`stale-branches`。它负责找出已合并或长期没动的 git 分支，生成报告和建议的清理命令，但自己**从不删除**。
2. 写 frontmatter，4 个可选字段全部用上。`allowed-tools` 只放只读 git 命令，比如 `for-each-ref`、`log`、`branch --merged`、`rev-parse`。
3. 写正文（≤ 60 行）：先确定默认分支，再判断“已合并”和“过期”，接着输出报告，最后列出删除建议和边界情况。
4. 写 FIELDS.md，说清楚每个字段为什么这样写、各平台怎么处理它。
5. 写 INVALID-EXAMPLES.md，故意写几个错误的 frontmatter，用来理解规则。
6. 虚构一个仓库状态，在全新会话里跑一次，结果写进 tests/smoke.md。

**交付物**（放在 `day-04/stale-branches/`）
- `SKILL.md`
- `LICENSE.txt`
- `FIELDS.md`
- `INVALID-EXAMPLES.md`
- `tests/smoke.md`
- （可选）`day-04/NOTES.md`

**完成标准**
1. `name: stale-branches` 与目录同名；description 是单行纯字符串，写明做什么、什么时候用，并至少排除 1 个边界（如解决 rebase/merge 冲突、讲解 git 概念）。
2. 4 个可选字段都合法：`license` 简短，并指向 LICENSE.txt；`compatibility` 为 1-500 字符，只写真实需求（git、仓库访问、是否需要 `git fetch` 联网）；`metadata` 只有字符串值，版本号加引号；`allowed-tools` 是字符串而不是 YAML 列表，只含只读命令，不能用 `Bash(git:*)` 这类宽泛写法。
3. 正文 ≤ 60 行，包含以下内容：
   - 如何确定默认分支，不能假设一定是 main
   - “已合并”和“过期”的判断方法，以及默认阈值
   - 报告格式：分支、最后提交日期、作者、是否已合并、建议
   - 删除命令只作为建议列出，执行前必须得到用户明确确认，并写明原因
   - 至少 3 个边界情况，比如当前分支或受保护分支、有未推送提交的分支、squash merge 导致分支看起来没合并
4. 安全不依赖 `allowed-tools`：正文自己写明不执行破坏性命令，并说明原因（该字段是实验性的、只预批准不限制、有的客户端会忽略）。
5. FIELDS.md ≤ 40 行。用一张表覆盖 4 个字段，每个字段写清：取值、为什么这样写、Claude Code / Copilot / Codex 中至少两个平台怎么处理、被忽略时会怎样。表后用 2-3 句说明哪些字段对这个 skill 真正必要，哪些可以删掉。
6. INVALID-EXAMPLES.md 至少 4 个错误片段，每个配一句英文说明，至少覆盖：metadata 值不是字符串、compatibility 超过 500 字符（可以描述，不必真写满）、allowed-tools 写成 YAML 列表、name 非法或与目录不一致。
7. tests/smoke.md ≤ 30 行：虚构仓库至少有 5 个分支，其中包括 1 个 squash merge 的分支和 1 个有未推送提交的分支，并贴出全新会话里的输出。**SKILL.md 的示例不能用这个场景的分支名或相同情形。**
8. skill 内容全部使用英文。

**预计用时**：约 30 分钟（SKILL.md 15 分钟，FIELDS 和 INVALID 10 分钟，冒烟测试 5 分钟）

**可选加分**
- 用 `skills-ref validate ./day-04/stale-branches` 校验一次（day-05 会正式用它）
- 在 NOTES.md 里写一句：如果去掉 `compatibility` 和 `allowed-tools`，这个 skill 的行为会不会变？

**参考链接**
- [Agent Skills specification](https://agentskills.io/specification)
- [Adding agent skills for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills)
- [Claude Code permissions](https://code.claude.com/docs/en/permissions)
- [Agent Skills open standard across Codex / Claude Code（第三方文章）](https://codex.danielvaughan.com/2026/05/05/agent-skills-open-standard-portable-skills-codex-cli-cross-agent/)
- [allowed-tools 只预批准、不限制（第三方文章）](https://thepromptshelf.dev/blog/claude-code-skill-allowed-tools-not-restrictive-2026/)
