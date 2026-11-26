# day-12：Fail Loud, Fail Useful — a robust frontmatter linter script

- 出题日期：2026-11-26
- 阶段：第三阶段 · 配套脚本（第 2 题：脚本的健壮性）

**学习目标**
- 在写代码之前先列出边界情况清单，并把它们变成冻结的测试夹具（fixtures），而不是等评审来发现漏洞（day-11 的 footer 漏判就是评审发现的）。
- 写出“可行动”的错误信息：每条错误都有位置（行号或字段）、期望值和修复建议，智能体看了就能改，而不用去读脚本源码。
- 用 PEP 723 声明第三方依赖，并在依赖缺失时优雅失败（专用退出码 + 告诉智能体正确的运行命令），在 `compatibility` 字段写明运行环境要求。
- 设计一组互不重叠的退出码，并规定多个文件、多种失败同时出现时的优先级。
- 用差分测试（differential testing）把自己的脚本和一个参考实现（`skills-ref validate`）对照，解释每一处分歧。

**背景知识**
day-11 的脚本是“happy path 正确”：规则表里的每一行都实现了，但真实输入里的边界情况（后面又跟一段 trailer）让它漏判。脚本的健壮性主要看三件事：

1. **边界情况**：先问“输入可能长什么样”，再写代码。对 SKILL.md 来说，常见的坑有：YAML 把未加引号的 `yes`/`no` 解析成布尔值、把 `1.0` 解析成浮点数；description 里未加引号的 `: ` 会让 YAML 报错；Windows 换行（CRLF）和 UTF-8 BOM；缺少结束的 `---`；非 UTF-8 文件。
2. **错误信息**：agentskills.io 的 Using scripts 指南要求错误信息说明“哪里错了、期望什么、可以怎么做”，例如 `Error: --format must be one of: json, csv, table.`，而不是 `Error: invalid input.`。诊断写 stderr，数据写 stdout；不同类型的失败用不同的退出码，并写进 `--help`。还要“对含糊的输入给出明确错误，而不是猜”。
3. **依赖**：指南推荐 Python 脚本用 PEP 723 内联元数据（`# /// script` 块）声明依赖并用 `uv run scripts/xxx.py` 运行，版本要固定（PEP 508 写法）。但智能体可能直接用 `python3` 运行，这时要捕获 `ImportError`，告诉它应该用什么命令重跑。环境要求写进 frontmatter 的 `compatibility` 字段（1-500 字符）。

今天的领域正好是你天天用的东西：按 agentskills.io 规范检查 SKILL.md 的 frontmatter。规范要点（已核对最新版）：
- `name`：必填，1-64 字符，只允许小写 `a-z`、`0-9` 和 `-`，不能以 `-` 开头或结尾，不能有连续的 `--`，必须和父目录同名。
- `description`：必填，1-1024 字符，不能为空。
- `license`：可选，简短的许可证名或文件引用。
- `compatibility`：可选，如果写了就是 1-500 字符。
- `metadata`：可选，字符串键到字符串值的映射（`version: 1.0` 不加引号会变成浮点数）。
- `allowed-tools`：可选、实验性，空格分隔的**字符串**，不是 YAML 列表。

**今天的接口约定（脚本必须实现）**
| 情况 | 结果 |
|---|---|
| 所有文件都没有 error（可以有 warning） | 退出码 0 |
| 至少一个文件有 lint error，且没有解析失败 | 退出码 1 |
| 参数错误或路径不存在（在检查任何文件之前发现） | 退出码 2，stdout 为空，stderr 说明原因和正确用法 |
| 至少一个文件无法解析（无 frontmatter、缺结束 `---`、YAML 语法错误、非 UTF-8） | 退出码 3（优先于 1），该文件的结果里有 `parse_error`，含行号 |
| 依赖缺失（直接用 `python3` 运行且没装 PyYAML） | 退出码 4，stderr 给出确切的 `uv run ...` 命令 |
| 未知的顶层字段 | warning，不影响退出码 |

**任务步骤**
1. 建 `day-12/skill-frontmatter-lint/`。**先写 `tests/EDGE-CASES.md`**：至少 12 个边界情况，每行写明输入特征、期望退出码、期望的 error/warning `code`。必须包含：合法的最小 skill；合法且带全部可选字段；name 含大写；name 有前导/结尾/连续连字符；name 与目录不同名；description 缺失或为空；description 超过 1024 字符；description 含未加引号的 `: `（YAML 报错）；缺少结束 `---`；`metadata` 值不是字符串；`allowed-tools` 写成 YAML 列表；CRLF + BOM（你自己决定接受还是报错，在表里写明理由）；非 UTF-8 文件；name 写成 `yes`（YAML 布尔值）；未知字段。
2. 按清单建 `tests/fixtures/`：每个夹具是一个独立的 skill 目录（因为要测“name 与目录同名”，目录名要有意义，例如 `tests/fixtures/05-name-mismatch/pdf-tools/SKILL.md`）。CRLF、BOM、非 UTF-8 夹具用脚本或 `printf` 生成，提交前用 `file` 或 `xxd` 确认字节正确。**把 EDGE-CASES.md 和 fixtures 单独提交一次，早于脚本。**
3. 写 `scripts/lint_frontmatter.py`：
   - 顶部用 PEP 723 声明 `requires-python` 和固定版本的 PyYAML（例如 `pyyaml==6.0.2`，以你查到的为准）；`import yaml` 包在 `try/except ImportError` 里，失败时按上表走退出码 4。
   - 用法：`uv run scripts/lint_frontmatter.py PATH [PATH ...]`，PATH 可以是 skill 目录或 SKILL.md 文件；无交互。
   - stdout 只输出一个 JSON 对象：`{"results": [{"path", "ok", "parse_error", "errors": [...], "warnings": [...]}], "summary": {"files", "errors", "warnings", "parse_failures"}}`；每条 finding 至少有 `code`（稳定的机器可读标识，如 `name-uppercase`）、`field`、`line`（能确定时）、`message`（哪里错了、期望什么）和 `fix`（具体怎么改）。
   - `--help` 写清参数、输出字段、每个退出码和优先级、依赖与运行方式。
4. 写 `scripts/test_lint_frontmatter.py`（`unittest`）：每个夹具至少一个用例，断言退出码和 `code`；再加一个用例用 `python3 -I -S` 运行脚本（`-S` 不加载 site-packages，模拟没装 PyYAML），断言退出码 4、stdout 为空、stderr 含 `uv run`。
5. 写 `SKILL.md`：
   - description 单行：做什么（按 Agent Skills 规范检查 SKILL.md frontmatter）、何时用（“我的 skill 格式对不对 / 为什么不被识别 / 发布前检查一下”）、至少两条排除边界（例如改进 description 的触发效果、评审正文指令质量、检查 MCP 配置）。
   - `compatibility` 写明需要 `uv`（或 Python 3.x + PyYAML）。
   - 正文 ≤ 50 行：确切命令（路径相对 skill 根目录）、每个退出码的处理（特别是 4：用 `uv run` 重跑；没有 uv 时告诉用户前提条件，**不要自己读 YAML 凭感觉判断**）、如何把 `fix` 转述给用户、只在用户要求时才修改文件、“运行而不必阅读源码”。
6. 差分测试：对所有夹具运行 `skills-ref validate`（或 `agentskills validate`），写一个小脚本 `tests/diff_reference.py` 把两边的通过/失败放在一起；RESULTS.md 里列出每一处分歧，并判断是你的 bug、参考实现的 bug，还是规范没写清楚。
7. 用脚本检查仓库里 day-01 ~ day-11 的所有 skill，把汇总（每个 skill 的 error/warning 数）写进 RESULTS.md。**不要修改那些旧 skill**，只记录。
8. 行为测试，全新会话、普通提示词（例如 “Can you check whether this skill is set up correctly? It's in fixtures/…”），装了 skill 的 3 次：一个有多个 lint error 的夹具、一个 YAML 解析失败的夹具、一个合法夹具；外加 1 次无 skill 基线（用有多个 error 的夹具）。先写并提交 `tests/CHECKLIST.md`（早于 output），每次运行 2-3 条可判断检查项，至少一条检查“报告的问题都来自脚本输出、没有编造”，一条检查“合法夹具没有被报出问题”。输出原样保存为 `output-N-skill.md`、`output-1-baseline.md`；用脚本从 harness 日志提取证据：skill 运行执行了 `lint_frontmatter.py`、没有读取其源码。
9. 写 `tests/RESULTS.md`（≤ 35 行）：单测结果、validate 输出、差分表、旧 skill 汇总、4 次运行逐条检查结果和执行证据，以及一段分析：哪个边界情况你最初没想到（或最容易写错），清单先行有没有帮你发现问题。

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
1. `name` 为 `skill-frontmatter-lint`，与目录同名；description 为单行纯字符串，写明做什么、何时用、至少两条排除边界；有 `compatibility` 字段写明运行环境；validate 通过，输出记在 RESULTS.md 或 NOTES.md。
2. EDGE-CASES.md 至少 12 行，包含任务步骤 1 列出的全部情况，每行有期望退出码和 `code`；它和 fixtures 的提交早于 `lint_frontmatter.py` 的第一次提交（git log 可见）。
3. CRLF、BOM、非 UTF-8 夹具的字节确实如此（评审时会用 `xxd` 检查）。
4. 脚本有 PEP 723 块并固定 PyYAML 版本；无交互；`--help` 写明参数、输出字段、退出码 0/1/2/3/4 及优先级、运行方式。
5. stdout 只输出 JSON（退出码 2、4 时 stdout 为空）；每条 finding 都有 `code`、`field`、`message`、`fix`，能确定行号时有 `line`；YAML 解析失败的 `parse_error` 含行号。
6. `python3 -m unittest`（在已安装 PyYAML 的环境，或 `uv run --with pyyaml==<版本> -m unittest`，二选一并写进 RESULTS.md）可直接运行并全部通过；每个夹具至少一个用例；有 `python3 -I -S` 的依赖缺失用例。
7. 正文 ≤ 50 行，包含确切命令、每个退出码的处理（含 4 的回退和“不要自己判断”）、转述 `fix`、只在用户要求时修改文件、“运行而不必阅读源码”。
8. 差分表覆盖全部夹具，每处分歧都有一句判断；旧 skill 汇总覆盖 day-01 ~ day-11 的所有 skill 且旧文件未被修改。
9. CHECKLIST.md 早于任何 output 提交；4 次运行全新会话、普通提示词，输出原样保存；日志证据由脚本提取：3 次 skill 运行都执行了脚本且没有读取源码，基线没有加载 skill。
10. RESULTS.md ≤ 35 行，含上述各项和“哪个边界情况最难”的分析；skill 内容、脚本（注释、`--help`、错误信息）和 tests/ 文档使用英文（NOTES.md 可以用中文）。

**预计用时**：约 35-40 分钟（清单和夹具约 10 分钟，脚本和单测约 15 分钟，差分和 4 次运行约 10 分钟；运行可以并行开会话）

**可选加分**
- day-11 遗留：`BREAKING CHANGE:` 段落如果有一行不缩进的续行（自动换行的长说明），`has_breaking_footer` 会把整段当成正文而漏判。加一个单测，决定是放宽续行规则还是在 `--help` 写明限制。
- 加 `--format text`（人类可读）但默认保持 JSON，并在正文说明智能体应使用默认 JSON。
- 加一个检查：description 是否包含 “Use when” 一类的触发语（warning 级别），并在差分表里说明这是规范之外的风格规则。
- 用 `uv lock --script` 生成锁文件并提交，在 NOTES.md 比较锁文件和只写 `==` 固定版本的差别。

**参考链接**
- [Agent Skills specification](https://agentskills.io/specification)（frontmatter 字段与约束）
- [Agent Skills: Using scripts](https://agentskills.io/skill-creation/using-scripts)（PEP 723、`uv run`、错误信息、退出码、“reject ambiguous input”）
- [PEP 723 – Inline script metadata](https://peps.python.org/pep-0723/)
- [uv: Running scripts](https://docs.astral.sh/uv/guides/scripts/)（`uv run`、`--with`、`uv lock --script`）
- [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)（`safe_load`、`MarkedYAMLError` 的 `problem_mark` 行号）
- [Python `-S` / `-I` command line options](https://docs.python.org/3/using/cmdline.html)
