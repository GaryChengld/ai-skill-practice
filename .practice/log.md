# 练习进度记录

由教练维护。每个条目记录出题日期、交付物、完成标准，以及之后的检查和评审结果。
每道题的完整题目保存在 `.practice/problems/day-NN.md`（每题一个文件）。

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
