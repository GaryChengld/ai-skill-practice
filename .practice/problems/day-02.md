# day-02：Description Showdown — three descriptions for a release-notes skill

- 出题日期：2026-10-20

**学习目标**
- 理解 description 是触发的唯一依据：启动时智能体只加载 `name` + `description`
- 用 train/validation 划分来比较多个 description 版本，避免过拟合
- 在有竞争 skill 的环境里测试边界

**背景**
- agentskills.io 的建议：用祈使句（"Use this skill when..."），写用户意图而不是实现细节，可以写得"主动"一点，把没有点名领域的场景也列进去。长度控制在几句话以内，上限 1024 字符。
- 最有价值的反例是**近似反例**：关键词相同，实际需求不同。
- 模型的行为有随机性，官方建议每条查询跑多次，算触发率（> 0.5 算触发）。查询集按 60/40 分成 train 和 validation，只根据 train 的失败来改 description，最后用 validation 来选版本。
- 单行 description 在各个解析器里最稳，今天要求写成单行。

**任务步骤**
1. 写一个竞争 skill 的存根 `day-02/competitors/pr-description/SKILL.md`，负责写 PR 描述，有 frontmatter 加 3-5 行正文就够了。
2. 写 `release-notes` skill：根据两个 tag 之间的 commit/PR 列表生成面向用户的 release notes。正文简短即可，今天的重点是 description。
3. 在 `DESCRIPTIONS.md` 里写 3 个版本：
   - V1：只写"做什么"
   - V2：加上 "Use this skill when..." 和用户可能说的话（比如 "what's new in v2.3"、"summarize changes since last tag"）
   - V3：在 V2 的基础上写清和 conventional-commits、pr-description 的边界
4. 写 `evals/trigger-queries.json`，至少 16 条，格式如下：
   `{ "query": "...", "should_trigger": true, "split": "train" }`
5. 测试时同时放 3 个 skill：release-notes、day-01 的 conventional-commits、pr-description 存根。可以真的装到某个平台上跑，也可以开一个全新的会话，粘贴 3 个 skill 的 name/description，让模型对每条查询回答"用哪个 skill，还是都不用"。先用 train 测三个版本，选出最好的一个，再跑 validation。
6. 把选中的版本写进 SKILL.md，结果写进 `EVAL-RESULTS.md`。

**交付物**
- `day-02/release-notes/SKILL.md`
- `day-02/release-notes/DESCRIPTIONS.md`
- `day-02/release-notes/evals/trigger-queries.json`
- `day-02/release-notes/EVAL-RESULTS.md`
- `day-02/competitors/pr-description/SKILL.md`
- （可选）`day-02/NOTES.md`

**完成标准**
1. `name` 为 `release-notes`，和目录同名；frontmatter 只有 `name` 和 `description`；description 是单行字符串（不用 `>`、`>-`、`|`）。
2. DESCRIPTIONS.md 里有 V1/V2/V3，标出字符数，都不超过 1024；V2 用祈使句；V3 写了排除范围。
3. 查询至少 16 条，每条都有 `query`、`should_trigger`、`split`，按约 60/40 划分，两组里都有正例和反例。
4. 至少 3 条正例里不出现 "release notes" 字样。
5. 至少 5 条近似反例：至少 2 条应该交给 conventional-commits，至少 2 条应该交给 pr-description。
6. 测试时同时提供 3 个 skill，EVAL-RESULTS.md 写明测试方法。
7. EVAL-RESULTS.md 有表格：三个版本各自的 train 通过率，以及选中版本的 validation 通过率。
8. EVAL-RESULTS.md 分析至少 2 条失败的查询，说明选了哪个版本、为什么，以及有没有过拟合的迹象。
9. SKILL.md 正文不超过 40 行，包括：输入说明、按用户能感知到的类别分组、跳过内部改动（chore/ci/test）的规则、1 个输出示例；不依赖特定厂商的工具名或路径。
10. skill 内容使用英文。

**预计用时**：约 30 分钟（存根和 skill 正文 8 分钟，3 个 description 7 分钟，查询集 8 分钟，测试和记录 7 分钟）

**可选加分项**
- 每条查询跑 3 次，记录触发率而不是单次结果
- 再写 4 条全新的查询做最后一轮检查
- 在 NOTES.md 里写：V3 的排除范围有没有让正例的触发率下降？

**参考链接**
- [Optimizing skill descriptions（agentskills.io）](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Agent Skills Specification](https://agentskills.io/specification)
- [anthropics/skills 里的 skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
