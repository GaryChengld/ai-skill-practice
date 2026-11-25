# day-11：Run It, Don't Reason It — a first scripts/ for a next-version skill

- 出题日期：2026-11-25
- 阶段：第三阶段 · 配套脚本（第 1 题：第一个 scripts/）

**学习目标**
- 判断 skill 里哪一步是“确定性的”（同样输入必须得到同样结果，例如解析、计数、按规则计算），把它交给 `scripts/` 里的脚本，而不是让模型每次自己推理。
- 按 agentskills.io 的脚本指南写一个对智能体友好的脚本：非交互、有 `--help`、结构化输出到 stdout、诊断信息到 stderr、有意义的退出码、只用标准库（或用 PEP 723 内联声明依赖）。
- 在正文里写清“怎么运行、怎么读输出、出错时怎么办”，并用 harness 日志证明智能体是**运行**了脚本，而不是读脚本源码再自己算。
- 延续 day-10 的测试做法：先冻结期望结果，再跑；用无 skill 基线证明脚本带来了内容上的区别。

**背景知识**
`scripts/` 是 Agent Skills 格式的第三种资源目录（另外两种是 references/ 和 assets/）。和 references 不同，脚本的价值在于**执行**：智能体通过 shell 运行它，只有输出进入上下文，源码本身不需要加载。所以正文要像写 CLI 文档一样写：给出确切命令（路径相对 skill 根目录）、输入格式、输出字段的含义、每个退出码对应的处理方式。

agentskills.io 的 Using scripts 指南里几条要点：
- **不要交互式提示**：智能体通常无法回答 `input()`；所有输入走参数、文件或 stdin。
- **`--help` 写清用法**：这是智能体了解接口的主要方式，比读源码便宜。
- **错误信息要可行动**：说明哪里错了、期望什么、可以怎么做，写到 stderr，配合非 0 退出码。
- **结构化输出**：JSON 到 stdout，便于智能体和其他工具解析；数据和诊断分开。
- **依赖**：优先标准库；如果需要第三方包，用 PEP 723 内联元数据并在正文写运行方式（例如 `uv run`），同时在 `compatibility` 字段说明运行环境要求。

今天的领域：根据上一个版本号和自那以后的 Conventional Commits 提交，算出下一个语义化版本号。规则看似简单，但模型自己算时容易在这些地方出错：藏在提交正文里的 `BREAKING CHANGE:` footer、`0.y.z` 阶段的特殊规则、前缀 `v`、不符合规范的提交、没有可发布提交。这些正是适合交给脚本的部分；“把结果解释给用户、写一句发布摘要”仍然由模型完成。

**今天的规则（脚本必须实现，写进正文的只保留模型需要知道的部分）**
| 情况 | 结果 |
|---|---|
| 任一提交 type 后有 `!`（如 `feat(api)!:`），或正文/footer 含 `BREAKING CHANGE:` / `BREAKING-CHANGE:` | breaking |
| 否则有 `feat` | minor |
| 否则有 `fix` 或 `perf` | patch |
| 否则（只有 docs/chore/test/ci/refactor/style/build 等） | none：next = current |
| 当前主版本为 0（`0.y.z`） | breaking → 升 minor；minor 和 patch → 都升 patch |
| 当前版本是预发布版（如 `2.0.0-rc.3`） | 不计算：stderr 给出可行动的错误信息，退出码 3 |
| 当前版本无法解析 | stderr 报错，退出码 2 |
| 提交首行不符合 `type(scope)!: subject` | 不参与计算，列入输出的 `unparsed` 数组 |
| 当前版本带 `v` 前缀 | 输出保留同样的前缀 |

**任务步骤**
1. 建 `day-11/semver-next/`。先写 `scripts/next_version.py`（只用标准库）：
   - 用法示例：`python3 scripts/next_version.py --current v1.4.2 --commits commits.txt`；`--commits -` 表示从 stdin 读。
   - 提交文件格式由你定，但要能直接由 git 生成，并写进 `--help` 和正文。建议：`git log --format='%B%n--END--' v1.4.2..HEAD`（每个提交以单独一行 `--END--` 结束）。
   - stdout 输出一个 JSON 对象，至少包含 `current`、`next`、`bump`（`major`/`minor`/`patch`/`none`）、`reasons`（每个决定性提交的首行和它触发的规则）、`unparsed`。
   - 退出码：0 成功（包括 `none`），2 输入无法解析，3 预发布版本不支持。错误信息写到 stderr，说明原因和下一步（例如“pass the last stable tag with --current, or ask the user which version line to continue”）。
2. 写 `scripts/test_next_version.py`（`unittest`，标准库），至少 6 个用例，覆盖上表的每一种“结果”行（breaking 的两种写法各一个）。
3. 写 `SKILL.md`：
   - description 单行：做什么（根据自上个 tag 以来的提交算下一个语义化版本号）、何时用（问“下一个版本号是多少 / 该打什么 tag / 这次是 major 还是 minor”）、至少两条排除边界（例如写 commit message、写 release notes 正文、解释 semver 概念）。
   - 正文 ≤ 50 行：如何收集提交（给出 git 命令）、确切的脚本命令、如何解读 JSON 和每个退出码、`unparsed` 不为空时要告诉用户、**不要自己重新计算或修改脚本给出的版本号**、最终回复格式（下一个版本号、bump 类型、1-3 条决定性提交、unparsed 提醒）。
   - 写清“运行这个脚本，不需要阅读它的源码”。
4. 先写并提交 `tests/EXPECTED.md`（在任何 output 之前提交，git log 可见）：4 个输入各自的期望 `next`/退出码，以及每个输入 2-3 条可判断的检查项。
5. 准备 4 个输入 `tests/input-1.txt` ~ `input-4.txt`，格式与脚本一致，第一行用注释或单独文件写当前版本（例如 `# current: v1.4.2`；如果用注释，脚本或正文要说明怎么处理这行）。**输入里不写期望结果或提示**：
   - 1：`v1.4.2`，若干 `fix`、`feat`、`chore` 混合 → 普通 minor。
   - 2：`1.4.2`，看起来全是 `fix`/`docs`，但其中一个 `fix:` 提交的 footer 里有 `BREAKING CHANGE:` → major。
   - 3：`0.9.3`，有一个 `feat!:` 和若干 `fix` → 按 0.y.z 规则。
   - 4：`v2.0.0-rc.3`，若干 `feat`/`fix` → 预发布，预期智能体说明无法计算并问用户，而不是自己编一个版本号。
6. 每个输入跑两次，全新会话、普通提示词（例如 “What should the next release tag be? Commits since the last tag are in input-2.txt, last tag is 1.4.2.”）：装了 skill 的一次、无 skill 基线一次。输出原样保存为 `output-N-skill.md`、`output-N-baseline.md`。
7. 从 harness 会话日志用脚本提取证据（可复用 day-10 的 `collect-harness.py` 思路）：skill 运行里**执行**了 `scripts/next_version.py`，并且**没有读取**它的源码。
8. 写 `tests/RESULTS.md`（≤ 30 行）：单元测试结果、`skills-ref validate`（或 `agentskills validate`）输出、8 次运行逐条检查结果、执行/读取证据，以及一段分析：哪个输入最能区分 skill 和基线；脚本有没有让某个检查项变得“必然通过”，这说明了什么。

**交付物**
- `day-11/semver-next/SKILL.md`
- `day-11/semver-next/scripts/next_version.py`
- `day-11/semver-next/scripts/test_next_version.py`
- `day-11/semver-next/tests/EXPECTED.md`
- `day-11/semver-next/tests/input-1.txt` ~ `input-4.txt`
- `day-11/semver-next/tests/output-N-skill.md`、`output-N-baseline.md`（共 8 个）
- `day-11/semver-next/tests/` 下的 harness 日志证据和提取脚本
- `day-11/semver-next/tests/RESULTS.md`
- （可选）`day-11/NOTES.md`

**完成标准**
1. `name` 为 `semver-next`，与目录同名；description 为单行纯字符串，写明做什么、何时用、至少两条排除边界；`skills-ref validate`（或 `agentskills validate`）通过，输出记在 RESULTS.md 或 NOTES.md。
2. `next_version.py` 只用标准库（或有 PEP 723 元数据且正文写明运行方式）；没有 `input()` 等交互；`--help` 写明参数、输入格式、输出字段和退出码。
3. 脚本实现“今天的规则”表的每一行；stdout 只输出 JSON，错误只写 stderr；退出码 0 / 2 / 3 与表一致；错误信息说明原因和下一步。
4. `test_next_version.py` 用 `python3 -m unittest` 可直接运行并全部通过（不写死绝对路径），至少 6 个用例，覆盖表中每一种结果，breaking 的 `!` 和 footer 两种写法各至少一个。
5. 正文 ≤ 50 行，包含：收集提交的 git 命令、相对 skill 根目录的确切脚本命令、JSON 字段解读、每个退出码的处理方式、“不要自己重算版本号”、“运行而不必阅读源码”、最终回复要包含的内容（含 `unparsed` 提醒）。
6. EXPECTED.md 的提交时间早于任何 output 文件（git log 可见）；每个输入 2-3 条可判断的检查项，input-4 至少一条检查“没有编造版本号”。
7. 4 个输入不含期望结果或提示；8 次运行都在全新会话、普通提示词；输出原样保存。
8. harness 日志证据由脚本提取：4 次 skill 运行都执行了 `scripts/next_version.py`，且没有读取它的源码；基线运行没有加载 skill。
9. RESULTS.md ≤ 30 行，包含单元测试结果、validate 输出（或指向 NOTES.md）、逐条检查结果和一段“区分度”分析。
10. skill 内容、脚本（含注释、`--help`、错误信息）和 tests/ 下文档使用英文（NOTES.md 可以用中文）。

**预计用时**：约 35 分钟（脚本和单测约 15 分钟，8 次运行可以并行开会话）

**可选加分**
- day-10 遗留：在 day-10 的 migration-safety-review 正文第 3 步写明“rename/drop 列在作者确认无人使用前按 application_breakage 处理”，在 FOLLOWUP.md 加一条检查 rename 风险等级的检查项，重跑 input-5 after。
- 给脚本加 `--format text`（人类可读）但默认保持 JSON，并在正文说明智能体应使用默认 JSON。
- 加一个 input-5：提交里有大量（≥ 30 个）chore/docs 和一个 `perf:`，看基线会不会漏掉。

**参考链接**
- [Agent Skills: Using scripts](https://agentskills.io/skill-creation/using-scripts)（非交互、`--help`、可行动的错误信息、结构化输出、依赖声明）
- [Agent Skills specification](https://agentskills.io/specification)（`scripts/` 目录、`compatibility` 字段、相对路径引用）
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)（`!`、`BREAKING CHANGE` / `BREAKING-CHANGE` footer）
- [Semantic Versioning 2.0.0](https://semver.org/)（0.y.z 与预发布版本）
- [PEP 723 – Inline script metadata](https://peps.python.org/pep-0723/)
