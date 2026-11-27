# 练习进度记录

由教练维护。每个条目记录出题日期、交付物、完成标准，以及之后的检查和评审结果。
每道题的完整题目保存在 `.practice/problems/day-NN.md`（每题一个文件）。**教练出新题时，同时把完整题目（标题、出题日期、学习目标、背景、步骤、交付物、完成标准、用时、加分项、参考链接，不含上一题评审）写入 `.practice/problems/day-XX.md`，和 log 一起提交；检查未完成的题时，以该文件为准重新列出要点。**（2026-10-31 Gary 在 chat 中要求）

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
- 状态：已完成，最终评分 5/5

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

**检查与评审**
- 2026-10-21 检查：未完成（main 上没有 day-02/ 文件夹，7 项交付物全部缺失）。
- 2026-10-21 chat 评审：评分 4/5，7 条完成标准全部满足（字符数、SHA-256 指纹已核对）。主要建议：(1) 多条反例和 T05 在查询里自带“not a PR description / not for a product release”这类免责声明，等于把答案写进题目，导致 V2/V3 都是 100%、评测区分不出版本，需要补一批不带提示的难例；(2) description 开头“Write summaries of software changes”太泛，应改成以交付物为中心的写法，并删掉写给路由器看的“route by the requested deliverable”；(3) 补上 CHANGELOG.md / Keep a Changelog 文件更新这个边界，示例里加一条 Breaking Change。
- 2026-10-21 chat 复查：评分 5/5，上次 3 条建议全部改好（新增 6 条无提示难例 H01-H06 并对三个版本重跑；description 改为以交付物开头的 R1、删除元指令；正文补 changelog 更新规则和 Breaking Change 示例，并做了正文冒烟测试）。新建议：Breaking Changes 放在最前面并写清楚旧 key 不再生效；description 里的 “for a shipped version” 和保留 Unreleased 的规则略有冲突；H 组的 split 宜单独标为 challenge；评测文档篇幅偏长，注意 30 分钟的时间盒。
- 2026-10-22 检查：复查后有一次新提交 3ae4fdf，落实了遗留建议（Breaking Changes 置顶并写明旧 key 失效；description 改为 R2 “for a release”，兼容 Unreleased；H 组改标 `split: challenge`；EVAL-RESULTS 从约 140 行压缩并保留历史）。R2 未重跑路由测试，已如实注明。确认已完成，最终评分 5/5。遗留关注点：时间盒、评测文档篇幅。

---

## day-03：Calibrate the Body — rewrite a weak incident-postmortem skill

- 出题日期：2026-10-22
- 阶段：第一阶段 · 格式基础（正文指令的写法）
- 针对弱点：前两题重心在 description 和路由评测，正文指令本身练得少；文档篇幅偏长（本题对说明文档设行数上限）；day-02 的“模糊请求先澄清还是给默认值”在本题正文里以“缺失信息处理”的形式练习
- 状态：已完成，最终评分 5/5

**交付物**
- `day-03/incident-postmortem/BEFORE.md`（题目给出的糟糕版本，原样复制）
- `day-03/incident-postmortem/SKILL.md`（重写后的 skill）
- `day-03/incident-postmortem/REWRITE-NOTES.md`（问题清单 + 自由度划分表）
- `day-03/incident-postmortem/tests/input-inc-482.md`（题目给出的测试输入，原样复制）
- `day-03/incident-postmortem/tests/output-before.md`、`tests/output-after.md`
- `day-03/incident-postmortem/tests/COMPARISON.md`
- （可选）`day-03/NOTES.md`

**完成标准**
1. `name` 为 `incident-postmortem`，与目录同名；frontmatter 只有 `name` 和 `description`，description 是单行纯字符串；同时说明做什么和什么时候用，包含 postmortem / post-incident review / RCA / outage 等关键词，并至少排除 1 个边界（如正在进行的事故处置、给客户的状态页更新）。
2. BEFORE.md 与题目给出的版本一致。
3. REWRITE-NOTES.md 列出至少 6 个 BEFORE 的问题，每个标注类别（vague / over-constrained / menu-without-default / contradiction / known-to-agent / invents-data / missing-why）和对应修改；另有一张表把新正文的每个部分标为 high / medium / low freedom，并各写一句理由。
4. SKILL.md 正文 ≤ 80 行，包含：输出模板；时间线的唯一默认格式（UTC）和根因分析的默认方法（可简短提及替代方法）；blameless 规则并说明原因；缺失信息标为 Unknown/TBD 而非编造；行动项带 owner、截止日期和类型，数量由发现决定而非固定；至少 3 条 Gotchas；返回前的自检清单；至少 3 个边界情况（如事故仍在进行、涉及安全敏感细节、信息来源互相矛盾）。
5. 不出现没有理由的全大写 MUST/NEVER/ALWAYS：每条绝对规则后面都有原因。
6. 用同一个输入分别在全新会话中跑 BEFORE 和 SKILL.md，输出保存到 tests/；COMPARISON.md ≤ 20 行，至少比较时区处理、指责性措辞、是否编造数字（约 1.2k 次失败结账）、行动项数量。
7. skill 内容（SKILL.md、REWRITE-NOTES、COMPARISON）使用英文；REWRITE-NOTES.md ≤ 60 行。

**检查与评审**
- 2026-10-23 chat 评审：评分 4/5，7 条完成标准全部满足（BEFORE 与题目逐字一致；正文约 71 行；无大写绝对词；REWRITE-NOTES 37 行、10 个问题；COMPARISON 14 行，PDT 换算正确）。主要建议：(1) 过度保守：after 输出 4 条行动项全是 Investigate，canary 漏检这一已观察到的检测缺口也没有 Detect 项，需允许“条件式”修复项并要求为已观察到的防护缺口给 Detect/Mitigate；(2) Gotcha 写死了 “October 14, 2026”，是针对测试输入的声明而非可复用规则，改为按日期判断 PDT/PST 的通用规则；(3) “估计≠测量”“回滚≠原因”在 Evidence/Analysis/Gotchas 重复出现，正文可削减约 15 行；description 的 “after an outage” 过窄，补上 degradation/incident review 等说法。
- 2026-10-23 chat 复查：评分 5/5，上次 3 条建议全部改好（ab236a3：新增“已观察到的防护缺口必须有 Detect/Mitigate”和条件式修复规则，R3 输出含 1 条 Detect + 1 条条件式 Prevent；时区 Gotcha 改为按日期和地区的通用规则并设 PT 默认；重复的谨慎规则合并到 Gotchas，正文 72 行；description 扩展到 degradation/incident review）。R1-R3 迭代记录如实保留。新建议：Actions 里的示例“cap payment-client retries”和测试输入同题，R3 的条件式 Prevent 几乎照抄，属于评测污染，示例应换成其他领域；时区 Gotcha 一条塞了三件事，宜拆开；canary Gotcha 里的“propose an improvement”与 Actions 重复。
- 2026-10-23 检查：复查（ab236a3）之后没有新修改，确认已完成，最终评分 5/5。复查提出的 3 条新建议（Actions 示例与测试输入同题造成评测污染、时区 Gotcha 拆分、canary Gotcha 与 Actions 重复）尚未处理，评测污染这一点带入 day-04。

---

## day-04：Optional Frontmatter Fields — a stale-branch report skill

- 出题日期：2026-10-23
- 阶段：第一阶段 · 格式基础（可选 frontmatter 字段）
- 针对弱点：day-03 的正文示例与测试输入同题（评测污染），本题要求示例与冒烟测试场景完全不同；继续控制说明文档篇幅
- 状态：已完成，最终评分 5/5

**交付物**
- `day-04/stale-branches/SKILL.md`
- `day-04/stale-branches/LICENSE.txt`
- `day-04/stale-branches/FIELDS.md`
- `day-04/stale-branches/INVALID-EXAMPLES.md`
- `day-04/stale-branches/tests/smoke.md`
- （可选）`day-04/NOTES.md`

**完成标准**
1. `name` 为 `stale-branches`，与目录同名；description 是单行纯字符串，说明做什么和什么时候用，并至少排除 1 个边界（如 rebase/merge 冲突、git 概念讲解）。
2. frontmatter 包含全部 4 个可选字段且都合法：`license` 简短并指向同目录的 LICENSE.txt；`compatibility` 为 1-500 字符、只写真实环境需求（git、仓库访问、是否需要网络 fetch）；`metadata` 只含字符串键值（版本号加引号，键名不易冲突）；`allowed-tools` 为空格分隔的字符串（不是 YAML 列表），只预批准只读 git 命令，不包含能删除分支或推送的命令（不能用 `Bash(git:*)` 这类宽泛写法）。
3. 正文 ≤ 60 行，包含：如何确定默认分支（不能假设一定是 main）；“已合并”和“过期”的判断方法及默认阈值；输出报告格式（分支、最后提交日期、作者、是否已合并、建议）；删除命令只作为建议列出，执行前必须得到用户明确确认，并写明原因；至少 3 个边界情况（如受保护/当前分支、未推送的本地提交、squash merge 导致看起来未合并）。
4. 安全不依赖 allowed-tools：正文自己写明不执行破坏性命令，因为该字段是实验性的、只做预批准而不做限制、部分客户端会忽略它。
5. FIELDS.md ≤ 40 行：一张表覆盖 4 个可选字段（取值、为什么写/写成这样、Claude Code / GitHub Copilot / Codex 中至少两个平台对它的处理、客户端忽略它时会发生什么），外加 2-3 句说明哪些字段对这个 skill 真正必要、哪些可以删掉。
6. INVALID-EXAMPLES.md 至少 4 个故意写错的 frontmatter 片段，每个附一句英文说明违反了哪条规则，至少覆盖：metadata 值不是字符串、compatibility 超过 500 字符（可描述而不必真写满）、allowed-tools 写成 YAML 列表、name 与目录不一致或格式非法。
7. tests/smoke.md ≤ 30 行：描述一个虚构仓库状态（至少 5 个分支，含 1 个 squash merge 和 1 个有未推送提交的分支）并贴出在全新会话中加载 skill 后的输出；SKILL.md 里的示例不能使用该场景的分支名或相同情形（避免评测污染）。skill 内容全部使用英文。

**检查与评审**
- 2026-10-23 chat 评审：评分 4/5，8 条完成标准全部满足（正文约 39 行；FIELDS 18 行；INVALID 6 例；smoke 6 个分支，用 trunk 作默认分支；正文无示例，没有评测污染；skills-ref 0.1.0 通过）。主要建议：(1) description 把“执行删除”整体排除，导致最常见的说法“delete my merged branches”不会触发本 skill，应改为触发并只给建议；(2) 正文用 `git symbolic-ref` 读 origin/HEAD，但它不在 allowed-tools 里，而且带两个参数时会写入，不能按前缀预批准，改用已批准的 `git rev-parse --abbrev-ref origin/HEAD`；(3) 正文句子过密、术语化（如 “verified upstream safety”“ancestry-merged”），宜拆短；smoke 只测了基于给定证据的分类，没有测真实 git 采集，可加一个临时仓库的加分测试。
- 2026-10-23 chat 复查：评分 5/5，上次 3 条建议全部改好（f7432ae）：description 覆盖 clean up/delete 请求且只给建议；改用 `git rev-parse --abbrev-ref` 读 origin/HEAD，并顺带去掉了 `git log` 预批准、改用 for-each-ref 的 upstream:track 和 `git worktree list`；正文改成短句，45 行。新增真实 git 采集测试，我在 Git 2.43 上复跑也是 5 条 PASS。新建议：正文没覆盖“分支指向 baseline 同一提交、没有独有提交”的情况（提交时间旧不代表分支旧，可能是刚建的分支）；smoke 输出仍是初版正文跑的，宜用新正文重跑一次；测试脚本留下临时目录，可改用 TemporaryDirectory。
- 2026-10-24 检查：复查（f7432ae）之后没有新修改，确认已完成，最终评分 5/5。复查提出的 3 条新建议（分支与 baseline 指向同一提交的情况、用新正文重跑 smoke、测试脚本改用 TemporaryDirectory）尚未处理，前两条带入 day-05 的修复任务。

---

## day-05：Stage Review — what the validator catches, and what it doesn't

- 出题日期：2026-10-24
- 阶段：第一阶段 · 格式基础（阶段小结）
- 针对弱点：前几题积压的遗留建议（day-01 的 `>-` 多行 description、day-03 Actions 示例与测试输入同题、day-04 baseline 同提交情况和 smoke 未重跑）；之前路由测试每次只放 2-3 个 skill，本题第一次把全部 skill 放进同一个目录做路由；继续控制文档篇幅
- 背景核实：PyPI 上 skills-ref 当前为 0.1.1，安装后命令名是 `agentskills`（validate / read-properties / to-prompt）；它会拒绝规范外的 frontmatter 字段、超长 compatibility、非小写 name，但不检查 metadata 值是否为字符串、allowed-tools 是否写成 YAML 列表
- 状态：已完成，最终评分 5/5

**交付物**
- `day-05/VALIDATION.md`
- `day-05/AUDIT.md`
- `day-05/catalog.xml`
- `day-05/ROUTING.md`
- 对 day-01 / day-03 / day-04 已有 skill 的原地修复（提交记录在 AUDIT.md 中列出）
- （可选）`day-05/lint.py`、`day-05/NOTES.md`

**完成标准**
1. VALIDATION.md ≤ 40 行：写明工具名、版本和安装命令；贴出修复后对 5 个 skill 目录（含 pr-description 存根）的 validate 结果；另把 day-04 INVALID-EXAMPLES 中至少 4 个片段放进临时目录逐个验证，用表格列出“被拦截 / 漏过”，并用 2-3 句说明校验器的覆盖范围意味着什么（例如平台专有字段会被判为不合法）。
2. AUDIT.md ≤ 40 行：一张表，5 个 skill × 至少 6 项校验器不覆盖的质量检查（如单行 description、有 “Use when”、有排除边界、正文行数、无厂商专有工具名/路径、绝对规则带理由、示例不与测试输入同题、遗留评审建议已处理），每格 Pass / Fail / N/A。
3. 至少 3 处修复，分布在至少 2 个旧 skill 中，必须包括：day-01 description 改为单行纯字符串；day-03 Actions 示例换成与测试输入无关的领域；day-04 补上“分支与 baseline 指向同一提交、没有独有提交”的边界情况或用新正文重跑 smoke（二选一或都做）。AUDIT.md 的 Fixes 部分逐条列出提交哈希和一句说明；修复后 validate 仍全部通过，原有行数上限不被突破。
4. catalog.xml 是对修复后全部 5 个 skill 运行 `agentskills to-prompt` 的输出。
5. ROUTING.md ≤ 30 行：在全新会话中只提供 catalog.xml（只有元数据）做路由，至少 10 条查询，其中至少 5 条是目录内两个 skill 之间的近似混淆（如 changelog vs commit message、release notes vs PR description、清理分支 vs 写 commit），至少 2 条应当不触发任何 skill；表格列出 expected / actual / pass，至少分析 1 条失败或最接近失败的查询，并说明是否需要改 description。
6. skill 内容和 day-05 下所有文档使用英文。

**检查与评审**
- 2026-10-24 chat 评审：评分 4/5，6 条完成标准全部满足（已复核：5 个目录 validate 全部通过；lint.py 退出码 0；catalog.xml 去掉 location 后与我本地 to-prompt 输出一致；git-collection.py 在 Git 2.43 上 PASS 并清理临时目录；VALIDATION 34 行、AUDIT 30 行、ROUTING 24 行；修复在 bc5cf45）。主要建议：(1) 路由测试又是 12/12，和 day-02 的问题一样：几乎每条查询都直接写出了交付物名词（commit message、PR description、RCA、release notes），混淆只停留在话题层面；而且 12 条在同一个会话里依次发送，前面的查询会影响后面的判断。应补 4-5 条不带交付物名词的难例（如 “Clean up my feature branch before review.”），每条在独立会话里跑；(2) day-04 新增的“与 baseline 同一提交”规则只写在 Edge cases 里，没有接进第 3 节的 Hold 列表和最终自检，可能被删除建议规则覆盖；(3) AUDIT 中 day-01 的 Length 标成 N/A，但 day-01 有正文 ≤150 行的上限，应为 Pass（93/150），lint.py 的 SKILLS 也要补上 150；Rationale 的 3 个 Fail 可以各补一句原因来关闭。
- 2026-10-24 chat 复查：评分 5/5，上次 3 条建议全部改好（998c513 + a6c9bf0）：新增 ROUTING-CHALLENGE.md，4 条不带交付物名词的难例各开独立会话，4/4，并如实记录了一次因 catalog 抄错而作废的 H03；baseline 同提交规则已接进第 3 节的 Hold 列表、删除条件和最终自检；AUDIT 的 day-01 Length 改为 93/150，lint.py 补上 150，三个 Rationale 各补原因后改为 Pass。复核：validate 全部通过，lint 退出码 0，catalog 仍与 CLI 输出一致，ROUTING.md 26 行。新建议：Edge cases 里 “request owner review before recommending deletion” 和主流程“同提交永不建议删除”略有出入，可改为 “hold for owner review; do not recommend deletion”；4 条难例来自教练，不算留出集，下次自己写一批再跑；H03 抄错说明 catalog 应直接粘贴原始文件而不是手工转写。
- 2026-10-25 检查：复查（998c513 + a6c9bf0）之后没有新修改，确认已完成，最终评分 5/5。复查提出的 3 条新建议尚未处理：day-04 Edge cases 的 “request owner review before recommending deletion” 措辞（列为 day-06 加分项）；自己编写留出测试输入（带入 day-06 的完成标准）；直接粘贴原始文件而非手工转写（带入 day-06 的加载测试方法）。

---

## day-06：Split the Body — progressive disclosure for incident-postmortem

- 出题日期：2026-10-25
- 阶段：第二阶段 · 渐进式披露
- 针对弱点：day-05 的难例由教练提供、不算留出集（本题测试输入由自己编写）；day-05 H03 因手工转写 catalog 作废（本题要求直接加载原始文件）；继续防评测污染（参考文件里的例子不能和测试输入同题）
- 背景核实：agentskills.io 规范——元数据约 100 tokens 启动时加载；正文建议 < 5000 tokens、SKILL.md < 500 行；scripts/references/assets 按需加载；文件引用用相对 skill 根目录的路径，只保持一层深度
- 状态：已完成，最终评分 5/5

**交付物**
- `day-06/incident-postmortem/SKILL.md`
- `day-06/incident-postmortem/references/timezones.md`
- `day-06/incident-postmortem/references/rca-methods.md`
- `day-06/incident-postmortem/references/sensitive-incidents.md`
- `day-06/incident-postmortem/tests/input-a.md`、`input-b.md`、`input-c.md`（自己编写）
- `day-06/incident-postmortem/tests/LOADING.md`
- （可选）`day-06/NOTES.md`

**完成标准**
1. 目录为 `day-06/incident-postmortem/`（从 day-03 复制后重构，day-03 原样保留）；`name` 与目录同名，description 单行纯字符串；`agentskills validate` 通过。
2. SKILL.md 正文 ≤ 55 行，仍包含始终需要的内容：证据规则、blameless 规则、行动项规则、输出模板、返回前自检。
3. 每个参考文件在正文中用相对路径（`references/<file>.md`）引用，并带明确的加载条件（“Read … when …”）；正文不要求“先读完所有参考文件”；参考文件之间不互相引用（只一层深度）。
4. 每个参考文件只讲一个主题，30-120 行；超过 100 行的在开头有目录；每个文件至少有一项 day-03 正文里没有的新内容（如 timezones：DST 切换时不存在/重复的本地时间；rca-methods：因果树的完整小例子及何时从 5 Whys 切换；sensitive-incidents：脱敏清单和对外分发前的审阅要求）。
5. 同一条规则只出现在一个地方：正文与参考文件之间没有重复的规则（正文可以用一句话指向参考文件）。参考文件里的例子不能使用 INC-482 结账场景，也不能与 tests/ 的输入同题。
6. tests/ 下 3 个自己编写的输入：A 只需正文（单一时区 UTC、无敏感信息），B 涉及跨时区且跨 DST 切换，C 涉及泄露的凭证或客户数据。每个在全新会话中运行，加载的是磁盘上的原始 skill 文件夹（不手工转写）。
7. LOADING.md ≤ 30 行：表格列出每个输入的预期加载文件、实际打开的文件（依据会话记录/工具调用日志）、是否通过；列出各层大小（description 字符数、正文行数和约 tokens、每个参考文件约 tokens，按字符数/4 估算）；至少一段分析多读或漏读的情况及对加载条件措辞的修改。
8. skill 内容和 tests/ 下的文档使用英文。


**检查与评审**
- 2026-10-26 检查：未完成（main 上没有 day-06/ 文件夹，8 项交付物全部缺失；远端也没有其他分支）。
- 2026-10-27 检查：未完成（main 上仍没有 day-06/ 文件夹，8 项交付物全部缺失；远端只有 main 分支，自上次检查后没有新提交）。
- 2026-10-28 检查：未完成（main 上仍没有 day-06/ 文件夹，8 项交付物全部缺失；远端只有 main 分支，自 10-27 检查后没有新提交）。
- 2026-10-29 检查：未完成（main 上仍没有 day-06/ 文件夹，8 项交付物全部缺失；远端只有 main 分支，自 10-28 检查后没有新提交）。
- 2026-10-30 检查：未完成（main 上仍没有 day-06/ 文件夹，8 项交付物全部缺失；远端只有 main 分支，自 10-29 检查后没有新提交）。
- 2026-10-31 chat 评审：评分 4/5，8 条完成标准全部满足（正文 54 行；3 个参考文件 41/46/40 行，各有新内容；正文与参考无重复规则，例子不与测试同题；A/B/C 自写且在独立会话加载原始文件夹，3/3 加载符合预期；LOADING 27 行；validate 结果采信提交记录，本地未能重跑）。主要建议：(1) trace 由被测模型自己书写，不是独立的工具调用日志，且提示中告知了“这是加载测试”，可能影响读取行为，应从 harness 的会话 jsonl 中提取读取记录，并用不提及测试的提示重跑；(2) rca-methods 从未被加载过，正向触发和 spring gap 未测试，补一个需要因果树的输入 D；(3) output-c 的 4 行行动项中有 3 行缺 Due 列，问题已记录但没有回馈到 skill，自检清单应改为具体可检查的条目（如 every Action Items row has five cells）。加分项（day-04 措辞）未做。
- 2026-10-31 chat 复查：评分 5/5，上次 3 条建议全部改好（1301f71）：(1) 用不提及测试的普通提示在 5 个新 Codex 会话中重跑，读取证据由 collect-harness.py 从 ~/.codex/sessions 的 jsonl 提取，模型自写 trace 不再作为证据（复核：各 jsonl 中出现的参考文件与 LOADING 表一致）；(2) 新增 input-d（两条独立失败路径），rca-methods 被正确加载，输出含因果树；(3) 自检改为逐行数单元格并修补，C follow-up 4/4 行完整（复核：C 首轮 4/5、D 3/4 行缺列，与记录一致）；正文重叠半句已删。新建议：最终版自检只在 C follow-up 跑过一次，应对之前同样缺列的 D 再跑一次；day-04 加分项仍未做。
- 2026-10-31 检查：复查（1301f71）之后 day-06/ 没有新修改（之后的提交只改 .practice/），确认已完成，最终评分 5/5。复查提出的新建议尚未处理：用最终版自检对 input-d 再跑一次（带入 day-07 完成标准）；day-04 Edge cases 措辞（继续列为加分项）。

---

## day-07：Load Only Your Domain — an ecosystem-aware dependency-fix skill

- 出题日期：2026-10-31
- 阶段：第二阶段 · 渐进式披露（第 2 题：按领域拆分参考文件）
- 针对弱点：day-06 最终版自检只在 C follow-up 验证过（本题要求对 D 重跑）；继续以 harness 会话日志而非模型自述作为读取证据、用不提及测试的普通提示；新增“仓库里有多个领域、但只该加载一个”和“没有匹配领域、一个都不该加载”两类过读/漏读测试
- 背景核实：Anthropic 最佳实践的 “Domain-specific organization” 模式（按领域分 reference 文件，只加载相关的一个）；npm `overrides`、uv `constraint-dependencies` / `override-dependencies`、Maven `<dependencyManagement>`、Gradle dependency constraints
- 状态：已完成，最终评分 5/5

**交付物**
- `day-07/dependency-fix-plan/SKILL.md`
- `day-07/dependency-fix-plan/references/npm.md`
- `day-07/dependency-fix-plan/references/python.md`
- `day-07/dependency-fix-plan/references/jvm.md`
- `day-07/dependency-fix-plan/tests/input-n.md`、`input-p.md`、`input-j.md`、`input-m.md`、`input-g.md`（自己编写）
- `day-07/dependency-fix-plan/tests/LOADING.md`
- 读取证据（harness 会话日志的提取结果）和提取脚本，放在 `tests/` 下
- day-06 input-d 用最终版 skill 重跑的结果（追加到 `day-06/incident-postmortem/tests/LOADING.md` 或写进 `day-07/NOTES.md`）
- （可选）`day-07/NOTES.md`

**完成标准**
1. 目录为 `day-07/dependency-fix-plan/`；`name` 与目录同名；description 单行纯字符串，写明做什么、何时用、至少一条排除边界（如普通的版本升级/新功能升级、写 commit message）；`agentskills validate` 通过。
2. SKILL.md 正文 ≤ 60 行，只放所有生态共用的内容：修复流程（确认受影响包和版本 → 判断直接/传递依赖 → 按“升级直接依赖 > 覆盖传递依赖 > 记录理由后暂缓”的顺序选最小修复 → 验证）、输出模板、返回前自检；外加一张路由表：判断依据（清单文件/锁文件名）→ 对应参考文件。
3. 路由规则明确：只加载“拥有该漏洞包”的生态对应的文件，而不是仓库里出现的所有生态；没有匹配生态（如 go.mod、Cargo.toml）时不加载任何参考文件，正文给出通用降级做法并说明没有该生态的专门指导。
4. 三个领域文件各 40-120 行，使用相同的小节骨架（如 Detect / Inspect the tree / Fix a direct dependency / Override a transitive dependency / Verify / Pitfalls），超过 100 行的开头有目录；每个文件至少 1 条该生态特有的坑（如 npm overrides 只在根 package.json 生效、pip 的 constraints 文件本身不安装任何包、Maven 的“最近者优先”依赖调解）；领域文件之间不互相引用，也不重复正文的共用规则。
5. tests/ 下 5 个自己编写的输入（每个 8-20 行）：N 只有 npm；P 是 Python（uv 或 pip）；J 是 Maven 或 Gradle；M 是同时含 package.json 和 pyproject.toml 的 monorepo，但漏洞只在 Python 侧（预期只加载 python.md）；G 是 Go 或 Rust 项目（预期不加载任何参考文件）。参考文件里的例子不能与这些输入使用同一个包或同一情形。
6. 每个输入在全新会话中运行，加载磁盘上的原始 skill 文件夹，提示词是普通请求、不提“测试/加载”；读取证据由脚本从 harness 会话日志中提取，模型自述不作为证据。
7. LOADING.md ≤ 30 行：表格列出输入、预期加载、实际加载（来自日志）、是否通过；各层大小（description 字符数、正文行数和约 tokens、每个领域文件约 tokens，按字符数 ÷ 4）；每次运行实际加载的总 tokens 与“全部内容塞进一个 SKILL.md”的 tokens 对比；至少一段分析过读或漏读（尤其是 M 和 G）及对路由措辞的修改。
8. day-06 遗留：用 day-06 最终版 skill 在全新会话中重跑 input-d，记录行动项每行是否都有 5 个单元格（附日志依据）。
9. skill 内容、tests/ 下文档使用英文。

**检查与评审**
- 2026-11-01 检查：未完成（main 上没有 day-07/ 文件夹，全部交付物缺失；day-06 input-d 重跑也未记录；远端只有 main 分支，自出题提交 3fc66b2 后没有新提交）。
- 2026-11-02 chat 评审：评分 4/5，9 条完成标准全部满足（正文 48 行；3 个领域文件 51/53/62 行，骨架一致，各有生态特有的坑；本地重跑 agentskills validate 通过；5 个输入 11-12 行；复核 jsonl：各参考文件的独有示例字符串只出现在预期的那次运行中，M 只读 python.md，G 不读参考文件；day-06 input-d 重跑 [5,5,5,5]；day-04 加分项已改）。主要建议：(1) M 的输入直接写明了“finding path 是 services/indexer/uv.lock”“web 侧无 findings”，路由答案已经给出，应加一个只给包名、不给路径的歧义输入，验证“ask before reading”规则（预期不读领域文件）；(2) 5 个输入全是“升级直接依赖/父依赖就能修”的路径，领域文件的 Override 小节和暂缓分支从未被用到，应加一个父依赖没有修复版本、必须覆盖传递依赖的输入；(3) SKILL.md 第 10 行 “Treat supplied synthetic findings as fixtures” 是测试情境泄漏进 skill 的措辞，应改为通用写法；description 可补充 CVE/GHSA、Dependabot、npm audit、pip-audit 等触发关键词。
- 2026-11-02 chat 复查：评分 5/5，上次 3 条建议全部改好（e784182）：(1) 新增 M2（只给包名、无路径），日志确认只读 SKILL.md，输出 ownership Unknown 并先询问 finding 路径；(2) 新增 O（npm workspace，父依赖无修复版本）读 npm.md、在根 package.json 用带版本的父级 override 并写移除条件，H（Python 无兼容修复）读 python.md、按暂缓分支给出缓解、owner 和复审日期，并指出 pip constraint 无效；(3) 第 10 行测试情境措辞已改为通用写法，description 已补充 CVE/GHSA、Dependabot、npm audit、pip-audit 关键词；本地 validate 通过。新的小问题：input-h 的依赖图用了简写包名（rule-eval / calendar-engine），模型把它列为待确认问题，输入应统一用全名；M2 这类只需提问的情况仍套用完整 6 列表格，大部分是 Unknown，可在正文允许“归属未确定时只输出 Ownership + Open questions”的简短形式。
- 2026-11-02 检查：复查（e784182）之后 day-07/ 没有新修改（之后的提交只改 .practice/），确认已完成，最终评分 5/5。复查提出的两个小问题尚未处理：测试输入统一用全名（带入 day-08 完成标准）；归属/信息不足时的简短输出形式（带入 day-08 的 input-d）。

---

## day-08：Ship the Template, Not the Prose — assets/ for an on-call handoff skill

- 出题日期：2026-11-02
- 阶段：第二阶段 · 渐进式披露（第 3 题：assets/ 的使用）
- 状态：已完成，最终评分 5/5
- 针对弱点：day-07 input-h 用了简写包名（本题测试输入必须用全名、前后一致）；day-07 M2 信息不足时仍套完整表格（本题 input-d 要求信息不足时不猜、给出 Unknown + 待确认问题）；继续以 harness 会话日志作为读取证据、普通提示词
- 背景核实：agentskills.io 规范 assets/ = 静态资源（模板、图片、数据文件如查找表和 schema），与 references/（按需阅读的文档）区分；文件引用用相对 skill 根目录的路径、一层深度；JSON Schema 2020-12（`required`、`enum`、`additionalProperties`）

**交付物**
- `day-08/oncall-handoff/SKILL.md`
- `day-08/oncall-handoff/assets/handoff-template.md`
- `day-08/oncall-handoff/assets/handoff.schema.json`
- `day-08/oncall-handoff/assets/severity-matrix.csv`
- `day-08/oncall-handoff/tests/input-a.md`、`input-b.md`、`input-c.md`、`input-d.md`（自己编写）
- `day-08/oncall-handoff/tests/output-*.md` / `output-c.json`（原样保存的模型输出）
- `day-08/oncall-handoff/tests/ASSETS.md`
- `tests/` 下的读取证据和提取脚本（可复用 day-07 的 collect-harness.py）
- （可选）`day-08/NOTES.md`

**完成标准**
1. 目录为 `day-08/oncall-handoff/`；`name` 与目录同名；description 单行纯字符串，写明做什么、何时用、至少一条排除边界（如写事故复盘 postmortem、制定值班排班表）；`agentskills validate` 通过。
2. SKILL.md 正文 ≤ 50 行，不含 references/ 目录；每个 asset 用相对路径引用并带使用条件和用法动词：模板“复制并填写、保持标题和顺序”，查找表“只在缺少已声明严重级别时查一行”，schema“只在请求 JSON 时使用并按它校验”。
3. 单一来源：输出结构只存在于 handoff-template.md（正文不再重复完整模板）；严重级别规则只存在于 severity-matrix.csv（正文不写“全站故障=SEV1”之类的规则）；JSON 字段只定义在 schema 中。
4. 三个 asset 都是可直接使用的数据而不是说明文：模板含占位符和固定标题；CSV 有表头、覆盖 impact × urgency 的全部组合（至少 3×3）；schema 使用 draft 2020-12，含 `required`、severity 的 `enum`（含 Unknown）和 `additionalProperties: false`。
5. tests/ 下 4 个自己编写的输入（每个 8-20 行，服务名、人名、工单号前后一致、用全名不用简写）：A 所有事项都已声明严重级别、要 Markdown（预期只用模板）；B 有一项没有严重级别但给出了 impact 和 urgency（预期模板 + 查找表，输出级别与 CSV 那一行一致）；C 要 JSON 给机器人用（预期用 schema，输出通过 JSON Schema 校验器）；D 有一项缺 urgency（不应猜级别：输出 Unknown 并列入待确认问题）。
6. 每个输入在全新会话中运行，加载磁盘上的原始 skill 文件夹，提示词是普通请求、不提“测试/加载”；读取证据由脚本从 harness 会话日志中提取。
7. ASSETS.md ≤ 30 行：表格列出输入、预期打开的 asset、实际打开（来自日志）、是否通过；B 写出查到的 CSV 行和输出级别；C 写出校验命令和结果；A/B/D 的输出标题与模板标题逐个、按顺序一致（可手工或脚本检查）；至少一段分析 asset 多读/漏读或模板被改写的情况及对正文措辞的修改。
8. skill 内容、assets 和 tests/ 下文档使用英文。

**检查与评审**
- 2026-11-03 检查：未完成（main 上没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自出题提交 9adf20e 后没有新提交）。
- 2026-11-04 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 2e8f463 后没有新提交）。
- 2026-11-05 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 94aed08 后没有新提交）。
- 2026-11-06 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 c973770 后没有新提交）。
- 2026-11-07 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 fd30b35 后没有新提交）。
- 2026-11-08 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 6bf38f9 后没有新提交）。
- 2026-11-09 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 cd9174b 后没有新提交）。
- 2026-11-10 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 8946ec4 后没有新提交）。
- 2026-11-11 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 00953b7 后没有新提交）。
- 2026-11-12 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 1ee7bdb 后没有新提交）。
- 2026-11-13 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 f57dac7 后没有新提交）。
- 2026-11-14 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 6f5ff93 后没有新提交）。
- 2026-11-15 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 57022e9 后没有新提交）。
- 2026-11-16 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 9881e24 后没有新提交）。
- 2026-11-17 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 edebea9 后没有新提交）。
- 2026-11-18 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 ebc6e82 后没有新提交）。
- 2026-11-19 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 8bab7d3 后没有新提交）。
- 2026-11-20 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 eaaec9f 后没有新提交）。
- 2026-11-21 检查：未完成（main 上仍没有 day-08/ 文件夹，全部交付物缺失；远端只有 main 分支，自上次检查提交 c3e5860 后没有新提交）。
- 2026-11-22 chat 评审（45133ef）：评分 5/5，8 条完成标准全部满足（verify.py 本地复跑通过，日志证据完整）。主要建议：①模板里 Watch list / Recently resolved 的条目没有固定格式，B/D 输出的已解决条目写法各不相同，B 的 "None reported" 少了句号，verify.py 也没查出来；②严重级别查表那一条前后重复（"Skip the lookup…" 应放在最前面），"line filter" 依赖 shell，应写成不限平台的说法；③测试提示词直接点名了 skill 和路径，所以 description 的触发没有测到，下次应加一个不点名的触发测试。
- 2026-11-22 chat 复查（3fc0545）：上次 3 条建议全部改好（Watch list/Recently resolved 条目格式固定，verify.py 检查所有列表段；查表规则先跳过再查，不依赖 shell；新 description，新增不点名 skill 的 E 并自动触发成功）。verify.py 本地复跑通过。新发现：JSON 的 watch_list/recently_resolved 仍是自由字符串（output-c 写成 "IDN-219, Account Sign-In Service. …"），建议在 schema 里改成对象；E 只测了正向触发，可加一个 postmortem 请求测排除边界。最终评分 5/5。
- 2026-11-22 检查：复查（3fc0545）之后 day-08/ 没有新修改（之后只有 48233a6 改了 .practice/log.md），确认已完成，最终评分 5/5。复查提出的两个小问题未处理：schema 中 watch_list/recently_resolved 仍是自由字符串（列为 day-09 加分项）；排除边界的反向触发测试（带入 day-09 完成标准）。


---

## day-09：Pay for What You Load — a context budget audit and a slimmer conventional-commits

- 出题日期：2026-11-22
- 阶段：第二阶段 · 渐进式披露（第 4 题：上下文预算）
- 状态：已完成，最终评分 5/5
- 针对弱点：day-08 的触发测试只有正向（本题加入不点名 skill 的正向 + 近似反例 + 反例触发测试）；day-08 schema 中列表项为自由字符串（列为加分项）；检查清单必须先于输出写好，避免事后对答案
- 背景核实：agentskills.io 规范：元数据约 100 token（启动时为所有 skill 加载）、正文建议 < 5000 token、SKILL.md 500 行以内、资源按需加载；Anthropic best practices “Concise is key”
- 完整题目：`.practice/problems/day-09.md`

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

**检查与评审**
- 2026-11-23 检查：未完成（main 上没有 day-09/ 文件夹，全部交付物缺失；远端只有 main 分支，自出题提交 8b97efa 后没有新提交）。
- 2026-11-24 chat 评审（5455d40）：评分 4/5，10 条完成标准基本满足（count_tokens.py 本地复跑，表格与 BUDGET.md 完全一致；正文 1322→447，减 66%；day-01 未改；触发 T1 激活、T2/T3 零读取；agentskills validate 本次无法复跑且提交中没有记录输出，手工检查 frontmatter 合规）。主要建议：①行为测试有天花板效应：输入已把答案写进摘要（如 input-2 自带迁移说明），原版和瘦身版都 12/12，无法检测删减带来的退化，“最危险的删减”分析证据不足，应加 1-2 个只给原始 diff、不预先说明 breaking/迁移的输入，最好再加无 skill 基线；②新 description 的 “when asked what a commit should say” 与 T1 提示词几乎同句，触发测试偏向自证，"Excludes" 不如 "Not for" 明确，建议改写并加一个措辞不同的正向提示词（如 “write a commit msg for this”）；③在 RESULTS.md 或 NOTES.md 记录 agentskills validate 的输出；count_tokens.py 依赖 PyYAML，可改用标准库解析两字段以便移植。
- 2026-11-24 chat 复查（3371b24）：上次 3 条建议全部改好（新增只给原始 diff 的 input-5 和无 skill 基线：原版/瘦身版 2/2、基线 0/2；description 改为建议版本并新增措辞不同的 T4，自动触发成功；NOTES.md 记录 skills-ref validate 通过，count_tokens.py 改为纯标准库，本地 python3 -I 复跑表格与 BUDGET.md 一致）。新发现：output-5-slim 用了 `chore(config)!`（原版为 `feat(config)!`），公开 API 变更不应归为 chore，清单未检查 type，可加 5c 并在 type 规则里补一句；RESULTS.md 正好 40 行，已到上限。最终评分 5/5。
- 2026-11-24 检查：复查（3371b24）之后 day-09/ 没有新修改（之后只有 44f29c9 改了 .practice/log.md），确认已完成，最终评分 5/5。复查提出的 output-5-slim 用 `chore(config)!` 的 type 问题未处理（列为 day-10 加分项）。

---

## day-10：Unpack the Kitchen Sink — refactor an everything-in-one-file migration review skill

- 出题日期：2026-11-24
- 阶段：第二阶段 · 渐进式披露（第 5 题：阶段小结）
- 状态：已完成，最终评分 5/5
- 针对弱点：day-09 行为测试有天花板效应（本题输入只给原始 SQL 和一行数据库/规模注释，不写风险；加无 skill 基线）；day-09 T1 提示词与 description 同句（本题 T1 必须换措辞）；validate 输出要记录；检查清单先于输出提交；day-09 type 问题列为加分项
- 背景核实：agentskills.io 规范（元数据约 100 token、正文 < 5000 token / 500 行、资源按需加载；文件引用用相对路径、一层深度）；PostgreSQL CREATE INDEX CONCURRENTLY 不能在事务块中、ADD COLUMN 常量默认值 PG11+ 不重写表、SET NOT NULL 可借已验证的 CHECK 约束跳过扫描（PG12+）；MySQL 8.0 INSTANT ADD COLUMN（8.0.12，任意位置 8.0.29）
- 完整题目：`.practice/problems/day-10.md`（含需原样保存的 BEFORE 版 SKILL.md）

**交付物**
- `day-10/BEFORE/migration-safety-review/SKILL.md`（原样保存的起点，不修改）
- `day-10/migration-safety-review/SKILL.md`
- `day-10/migration-safety-review/references/postgres.md`、`references/mysql.md`
- `day-10/migration-safety-review/assets/review-template.md`、`assets/risk-matrix.csv`
- `day-10/migration-safety-review/tests/PLAN.md`
- `day-10/migration-safety-review/tests/input-1.sql` ~ `input-4.sql`
- `day-10/migration-safety-review/tests/output-N-before.md`、`output-N-after.md`、`output-N-baseline.md`（共 12 个）
- `tests/` 下的读取 / 触发日志证据和提取脚本
- `day-10/migration-safety-review/tests/RESULTS.md`
- （可选）`day-10/NOTES.md`

**完成标准**
1. BEFORE 版与题目给出的文本一致；重构版 `name` 与目录同名，description 为单行纯字符串，写明做什么、何时用、至少两条排除边界，且 token 少于 BEFORE；`agentskills validate`（或 `skills-ref validate`）通过并把输出记在 RESULTS.md 或 NOTES.md。
2. 重构版正文 token 比 BEFORE 少至少 50%（以 count_tokens.py 为准），且正文 ≤ 40 行；正文中没有某一个数据库专有的规则（如 `CONCURRENTLY`、`ALGORITHM=`）。
3. 单一来源：输出结构只在 review-template.md；风险等级规则只在 risk-matrix.csv（覆盖原文的全部情况，含“未知大小按大表”或在正文写明这一条）；共有规则只出现一次；每个 references/assets 文件在正文中都有相对路径、使用条件和用法动词，且只引用一层深度。
4. PLAN.md 的去向表覆盖 BEFORE 的每一个二级标题段落，并且提交时间早于任何 output 文件（git log 可见）。
5. 4 个输入只含 SQL 和一行数据库/规模注释，不含风险提示；CHECKLIST（写在 PLAN.md 中）每个输入 2-4 条可判断的检查项，至少一条检查 risk 等级，input-4 至少一条检查“没有虚构的 High/Medium 发现”。
6. 12 次运行都在全新会话中、普通提示词；输出原样保存；重构版的通过条数不少于 BEFORE 版。
7. 读取证据来自 harness 日志：PostgreSQL 输入没有读 mysql.md，MySQL 输入没有读 postgres.md。
8. 3 个触发测试提示词不提 skill 名称、路径或“测试”；T1 激活、T2 和 T3 不激活，证据由脚本提取。
9. RESULTS.md ≤ 40 行，包含 token 对比表和至少一段“区分度”分析。
10. skill 内容、references/assets、tests/ 下文档使用英文（NOTES.md 可以用中文）。

**检查与评审**
- 2026-11-25 chat 评审（da26c44）：评分 5/5，10 条完成标准全部满足（BEFORE 与题目逐字一致；count_tokens.py 本地复跑：元数据 128→63、正文 1511→449，减 70%；正文无数据库专有规则；PLAN.md 在 c62bfd5 先于输出提交；manifest 显示 PG 输入只读 postgres.md、MySQL 只读 mysql.md；T1 激活、T2/T3 零读取；skills-ref validate 通过）。主要建议：①output-3-after 在 Findings 和 Rollout 之间多了一段模板外的文档链接，manifest 的 template 检查仍判通过，模板校验应检查标题之间没有多余段落；②第 5 步要求“filtered or row-range read”一个 8 行、67 token 的 CSV，收益很小却导致了重跑，并隐含依赖 shell 工具，建议改为整表读取后只用选中的行；正文 6 步都是长段落，第 2、4 步各混了 3-4 件事，建议拆短；③before 和 after 没有被任何检查项区分，baseline 只在“给出总体评级”这一格式项失分，下次加一个能测出内容差异的输入（如未知表大小、或 rename 列）。
- 2026-11-25 chat 复查（2155914 / 1247425）：上次 3 条建议全部改好（collect-harness.py 的 matches_template 拒绝标题之间的多余段落，新增 test_template.py 3 个单测本地通过，旧版 output-3-after 被判不通过、5 个新 AFTER 输出全部通过；第 5 步改为整表读取，第 2、4 步拆短，正文 449→364 token；新增 input-5（未知表大小 + rename 列）并先在 72801c8 冻结 FOLLOWUP.md 评分标准，skill 两版 3/3、基线 0/3，内容上测出了区分）。新发现：output-5-after 把 rename `status` 评为 Low（理由是应用使用情况未确认），与“未知表大小按大表处理”的保守原则不一致，基线反而评 High；FOLLOWUP 也没有检查 rename 的风险等级。建议把“rename/drop 列在作者确认无人使用前按 application_breakage 处理”写进正文第 3 步，并加一条检查项。最终评分 5/5。
- 2026-11-25 检查：复查（2155914 / 1247425）之后 day-10/ 没有新修改（之后只有 38fc584 改了 .practice/log.md），确认已完成，最终评分 5/5。复查提出的 rename 风险等级问题未处理（列为 day-11 加分项）。

---

## day-11：Run It, Don't Reason It — a first scripts/ for a next-version skill

- 出题日期：2026-11-25
- 阶段：第三阶段 · 配套脚本（第 1 题：第一个 scripts/）
- 状态：已完成，最终评分 5/5
- 针对弱点：day-10 复查发现模型在“保守规则”上判断不一致（本题把确定性计算交给脚本，用日志证明是执行而非阅读源码）；延续先冻结 EXPECTED.md、无 skill 基线、输入不含答案；day-10 rename 风险等级问题列为加分项
- 背景核实：agentskills.io Using scripts 指南（非交互、--help、可行动的错误信息写 stderr、结构化输出、标准库或 PEP 723 依赖）；Conventional Commits 1.0.0（`!` 与 `BREAKING CHANGE` / `BREAKING-CHANGE` footer）；SemVer 2.0.0（0.y.z、预发布）
- 完整题目：`.practice/problems/day-11.md`（含脚本必须实现的规则表）

**交付物**
- `day-11/semver-next/SKILL.md`
- `day-11/semver-next/scripts/next_version.py`
- `day-11/semver-next/scripts/test_next_version.py`
- `day-11/semver-next/tests/EXPECTED.md`
- `day-11/semver-next/tests/input-1.txt` ~ `input-4.txt`
- `day-11/semver-next/tests/output-N-skill.md`、`output-N-baseline.md`（共 8 个）
- `tests/` 下的 harness 日志证据和提取脚本
- `day-11/semver-next/tests/RESULTS.md`
- （可选）`day-11/NOTES.md`

**完成标准**
1. `name` 为 `semver-next`，与目录同名；description 为单行纯字符串，写明做什么、何时用、至少两条排除边界；validate 通过，输出记在 RESULTS.md 或 NOTES.md。
2. `next_version.py` 只用标准库（或 PEP 723 + 正文写明运行方式）；无交互；`--help` 写明参数、输入格式、输出字段和退出码。
3. 脚本实现规则表每一行；stdout 只输出 JSON，错误只写 stderr；退出码 0 / 2 / 3 与表一致；错误信息说明原因和下一步。
4. `python3 -m unittest` 可直接运行并全部通过，至少 6 个用例，覆盖每种结果，breaking 的 `!` 和 footer 各至少一个。
5. 正文 ≤ 50 行，含 git 命令、相对路径的确切脚本命令、JSON 字段解读、每个退出码的处理、“不要自己重算”、“运行而不必阅读源码”、最终回复内容（含 unparsed 提醒）。
6. EXPECTED.md 提交时间早于任何 output；每个输入 2-3 条可判断检查项，input-4 至少一条检查“没有编造版本号”。
7. 4 个输入不含期望结果或提示；8 次运行全新会话、普通提示词；输出原样保存。
8. 日志证据由脚本提取：4 次 skill 运行都执行了 next_version.py 且没有读取其源码；基线没有加载 skill。
9. RESULTS.md ≤ 30 行，含单测结果、validate 输出（或指向 NOTES.md）、逐条检查结果和“区分度”分析。
10. skill 内容、脚本（注释、--help、错误信息）和 tests/ 文档使用英文（NOTES.md 可以用中文）。

**检查与评审**
- 2026-11-26 chat 评审（efbd172 / b437259）：评分 5/5，10 条完成标准全部满足（本地 `python3 -I -m unittest` 18 个用例通过；4 个输入复跑脚本结果与 EXPECTED.md 一致，退出码 0/0/0/3；另测 none、0.x feat→patch、缺 `--END--`、非法版本、`BREAKING-CHANGE` 均符合规则表；EXPECTED.md 在 efbd172 先于输出提交；manifest 显示 4 次 skill 运行都执行了 next_version.py、零源码读取，基线未启用 skill；skill 10/10、基线 4/10；在 Codex CLI 的 .agents/skills 下运行，跨平台）。主要建议：①0.y.z 规则只解释了 breaking→minor，feat→patch 没有说明也没有行为测试；建议 JSON 加 `major_zero_shift` 之类字段，第 4 步改为通用说明，加一个 0.x 只有 feat 的输入；②第 2 步“从 skill 根目录运行 / 或用绝对路径 / 或 python”三选一写得绕，实际 4 次都是从工作目录用 `.agents/skills/semver-next/scripts/...` 运行，建议改为一条明确规则；③git 命令加 `--no-merges`，否则 merge 提交会堆进 unparsed；footer 检测会匹配紧跟标题或正文段落里的 `BREAKING CHANGE:`，要么限定在最后一个段落，要么在 --help 里写明是宽松匹配；manifest 里基线的 `activation: true` 实际表示“未激活符合预期”，建议改名。
- 2026-11-26 chat 复查（fdfb899 / 38fdc3c / 6e81ed5）：上次 3 条建议全部改好（JSON 新增 `major_zero_shift`，第 4 步改为通用的 major-zero 说明；新增 input-5（0.9.3 只有 feat），FOLLOWUP.md 在 fdfb899 先于输出冻结，skill 2/2 答 0.9.4、基线 0/2 答 0.10.0；第 2 步改为“从用户工作目录按 skill 内路径运行”；git 命令加 `--no-merges`；footer 检测限定最后一段并写进 --help；manifest 改为 `activation_as_expected`；本地 21 个单测通过，5 次 skill 运行都执行了脚本且零源码读取）。新发现：footer 只看最后一段会漏判，`BREAKING CHANGE:` 段落后面再隔一个空行跟 `Signed-off-by:` / `Refs:`（例如 `git commit -s` 追加 trailer）时返回 minor，漏掉 breaking 比误报更危险；建议检查标题后所有“全是 trailer 形式的行”的段落，或在不确定时偏向 breaking，并加一个单测。最终评分 5/5。
- 2026-11-26 检查：复查之后有新修改（7add794）：`has_breaking_footer` 改为检查标题之后所有 trailer 段落，新增 `Refs:` / `Signed-off-by:` 跟在 breaking 段落后的回归用例，`--help` 同步更新，并刷新了 5 次 skill 运行的日志证据；本地 `python3 -I -m unittest` 22 个用例通过。上次的建议已改好；剩余小问题：breaking 段落里不缩进的续行仍会被当成正文而漏判（列为 day-12 加分项）。确认已完成，最终评分 5/5。

---

## day-12：Fail Loud, Fail Useful — a robust frontmatter linter script

- 出题日期：2026-11-26
- 阶段：第三阶段 · 配套脚本（第 2 题：脚本的健壮性）
- 针对弱点：day-11 的 footer 漏判是评审发现的（本题要求先写边界情况清单并冻结夹具，再写脚本）；延续先冻结检查清单、无 skill 基线、日志证明“运行而非阅读”；新增依赖缺失的优雅失败和差分测试；day-11 续行问题列为加分项
- 背景核实：agentskills.io 规范（name 1-64、小写字母数字和连字符、不能首尾/连续连字符、与目录同名；description 1-1024；compatibility 1-500；metadata 字符串映射；allowed-tools 空格分隔字符串、实验性）；Using scripts 指南（PEP 723 + `uv run`、固定版本、可行动错误信息、不同失败用不同退出码并写进 --help、reject ambiguous input）
- 完整题目：`.practice/problems/day-12.md`（含接口约定表）

**交付物**
- `day-12/skill-frontmatter-lint/SKILL.md`
- `day-12/skill-frontmatter-lint/scripts/lint_frontmatter.py`
- `day-12/skill-frontmatter-lint/scripts/test_lint_frontmatter.py`
- `day-12/skill-frontmatter-lint/tests/EDGE-CASES.md`
- `day-12/skill-frontmatter-lint/tests/fixtures/`（≥ 12 个夹具目录）
- `day-12/skill-frontmatter-lint/tests/diff_reference.py`
- `day-12/skill-frontmatter-lint/tests/CHECKLIST.md`
- `day-12/skill-frontmatter-lint/tests/output-1-skill.md` ~ `output-3-skill.md`、`output-1-baseline.md`
- `tests/` 下的 harness 日志证据和提取脚本
- `day-12/skill-frontmatter-lint/tests/RESULTS.md`
- （可选）`day-12/NOTES.md`

**完成标准**
1. `name` 为 `skill-frontmatter-lint`，与目录同名；description 单行纯字符串，写明做什么、何时用、至少两条排除边界；有 `compatibility` 字段；validate 通过，输出记在 RESULTS.md 或 NOTES.md。
2. EDGE-CASES.md ≥ 12 行，含题目步骤 1 的全部情况，每行有期望退出码和 `code`；它和 fixtures 的提交早于 `lint_frontmatter.py` 的第一次提交。
3. CRLF、BOM、非 UTF-8 夹具的字节确实如此（用 `xxd` 检查）。
4. 脚本有 PEP 723 块并固定 PyYAML 版本；无交互；`--help` 写明参数、输出字段、退出码 0/1/2/3/4 及优先级、运行方式。
5. stdout 只输出 JSON（退出码 2、4 时为空）；每条 finding 有 `code`、`field`、`message`、`fix`，能确定时有 `line`；`parse_error` 含行号。
6. 单测可直接运行并全部通过（运行方式写进 RESULTS.md）；每个夹具至少一个用例；有 `python3 -I -S` 的依赖缺失用例（退出码 4、stdout 空、stderr 含 `uv run`）。
7. 正文 ≤ 50 行，含确切命令、每个退出码的处理（含 4 的回退和“不要自己判断”）、转述 `fix`、只在用户要求时修改文件、“运行而不必阅读源码”。
8. 差分表覆盖全部夹具，每处分歧有一句判断；旧 skill 汇总覆盖 day-01 ~ day-11 的所有 skill，旧文件未被修改。
9. CHECKLIST.md 早于任何 output 提交；4 次运行全新会话、普通提示词，输出原样保存；日志证据由脚本提取：3 次 skill 运行都执行了脚本且没读源码，基线没有加载 skill。
10. RESULTS.md ≤ 35 行，含上述各项和“哪个边界情况最难”的分析；skill 内容、脚本和 tests/ 文档使用英文（NOTES.md 可以用中文）。

**检查与评审**
- 2026-11-26 chat 评审（5b47a11 / f72ce10 / 04e3a29）：评分 5/5，10 条完成标准全部满足（27 个夹具，EDGE-CASES.md 在 5b47a11 先于脚本冻结；od 确认 15 号为 BOM + CRLF、16 号含 0xFF；本地 9 个单测含 27 个子测试通过，`python3 -I -S` 退出码 4、不存在路径退出码 2 且 stdout 为空；正文 22 行；差分表覆盖 27 个夹具，8 处分歧都有判断；旧 skill 12 个均 0 问题且未修改；3 次 skill 运行都执行了脚本、零源码读取）。主要建议：①行为测试没有区分度：基线在 19 号夹具上也全对，而 RESULTS 自己说最难的是 YAML 类型强制转换，应把 13/17/23（或 15、16）这类“肉眼看不出”的夹具放进行为测试；②`fix` 太泛：基线给出了 `bad-name`，skill 只说 “Lowercase it”，脚本可以利用 node.value 给出具体改法（如 `name: bad-name`、`version: "1.0"`），description-missing 的 line 1 指向开头 `---` 不准确，可改为 null 或结束分隔符行；③PyYAML 固定在 6.0.2，但 6.0.3 才提供 Python 3.14 wheel，本地单测实际跑的是 6.0.3，而 `requires-python = ">=3.10"` 不设上限，建议固定 6.0.3（同步 compatibility）或在 RESULTS 记录 uv 实际解析到的版本；旧 skill 汇总三条 bullet 内容相同，可合并为一句。
