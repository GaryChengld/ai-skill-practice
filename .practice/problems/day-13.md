# day-13：Validate Before You Hand Off — a JSON Schema validation loop for an eval-set skill

- 出题日期：2026-11-27
- 阶段：第三阶段 · 配套脚本（第 3 题：脚本 + 参考文件组合，校验输出格式）

**学习目标**
- 把“输出格式”从正文散文里拿出来，变成一份机器可执行的 JSON Schema（放在 `assets/`），再配一份给模型看的字段说明（放在 `references/`），并在正文里写清楚什么时候读哪一个。
- 用脚本实现 agentskills.io 最佳实践里的 **validation loop**：先写草稿文件 → 运行校验脚本 → 只修改报错的位置 → 重跑，直到通过或达到次数上限。
- 分清“Schema 能表达的规则”和“只能靠代码检查的语义规则”（例如按某个属性去重），两者用同一种输出格式报告。
- 把 jsonschema 的通用报错翻译成“可直接照做”的 `fix`（延续 day-12 的经验）。
- 设计**有区分度**的行为测试：基线也能拿到同一份 schema，比的是“有没有校验循环”，而不是“知不知道格式”。

**背景知识**
1. **Validation loop**：agentskills.io 的 [Best practices](https://agentskills.io/skill-creation/best-practices) 有专门一节 “Validation loops”：让智能体在继续之前先校验自己的产出，做完 → 跑校验 → 修 → 再跑。另一节 “Plan-validate-execute” 讲的是先把计划写成结构化文件（例如 `field_values.json`），用脚本对照“事实来源”校验，失败就修改后重验，并强调**错误信息要具体到智能体能自我纠正**。
2. **assets/ 和 references/ 的分工**：同一页 “Templates for output format” 建议较长或只在部分情况下需要的模板放进 `assets/`，从 SKILL.md 引用，按需加载；`references/` 放给模型读的说明文档，关键是写清 *when* 读取（例如 “Read `references/api-errors.md` if the API returns a non-200 status code”）。今天 schema 是给**脚本**用的，模型不必读它；字段说明是给**模型**用的。
3. **jsonschema（Python）**：PyPI 最新版 4.26.0（要求 Python ≥ 3.10）。几个要点：
   - 用 `Draft202012Validator.check_schema(schema)` 先确认 schema 本身合法，再 `iter_errors(instance)` 拿到全部错误，而不是只拿第一个；每个错误有 `json_path`/`absolute_path`（出错位置）、`validator`（触发的关键字，如 `required`、`enum`、`minContains`）和 `message`。
   - Draft 2020-12 的 `contains` + `minContains` 可以表达“数组里至少有 N 个满足条件的元素”，`if`/`then` 可以表达条件必填。
   - **坑**：`"format": "date"` 默认只是注解，不会被校验；必须传 `format_checker=Draft202012Validator.FORMAT_CHECKER` 才会检查。
   - Schema 做不到“按 `id` 字段去重”（`uniqueItems` 比较的是整个元素），这类规则要在脚本里另写。
4. **今天的领域**：为一个 skill 生成**触发评估集**（下一阶段会用到）。格式是本练习自定的，参考了 skill-creator 一类工具常用的 `{"query", "should_trigger"}` 写法，不是官方标准。

**今天的格式约定（schema 必须表达的规则）**
| 位置 | 规则 |
|---|---|
| 顶层 | 只允许 `skill`、`created`、`cases` 三个字段（`additionalProperties: false`），全部必填 |
| `skill` | 符合 Agent Skills 的 name 规则（小写字母数字和单个连字符，1-64 字符） |
| `created` | `format: date`（例如 `2026-11-27`），并且脚本要真的校验它 |
| `cases[]` | 每项必填 `id`、`prompt`、`category`、`should_trigger`；`id` 匹配 `^[a-z0-9]+(-[a-z0-9]+)*$`；`prompt` 10-500 字符 |
| `category` | 只能是 `positive`、`negative`、`near-miss` |
| 条件规则 | `positive` → `should_trigger` 必须为 `true`；`negative`、`near-miss` → 必须为 `false`；`near-miss` 还必须有非空的 `confusable_with`（说明它容易和什么任务混淆） |
| 数量 | 用 `contains` + `minContains`：每个 category 至少 3 条 |

**脚本额外的语义检查（schema 表达不了）**：`id` 重复（error）；`prompt` 去掉首尾空白、忽略大小写后重复（error）；`prompt` 里直接出现了 skill 名（warning：等于把答案告诉了模型）。

**任务步骤**
1. 建 `day-13/eval-set-builder/`。先写 `assets/eval-set.schema.json`（Draft 2020-12，`$schema` 写明），实现上表全部规则。
2. **先建夹具并单独提交一次，早于脚本**：`tests/fixtures/` 下至少 9 个 JSON 文件，每个对应一种情况，并写 `tests/fixtures/README.md` 列出每个文件的期望退出码和期望的 `rule`。必须包含：合法；缺必填字段；`category` 非法；`near-miss` 缺 `confusable_with`；`positive` 却 `should_trigger: false`；某个 category 只有 2 条（`minContains`）；`created` 写成 `2026-13-45`（验证 format 真的被检查）；`id` 重复；不是合法 JSON（例如末尾多一个逗号）。
3. 写 `scripts/validate_evals.py`：
   - PEP 723 块固定 `jsonschema==4.26.0`；依赖缺失时退出码 4，stderr 给出确切的 `uv run ...` 命令（复用 day-12 的做法）。
   - 用法：`uv run scripts/validate_evals.py FILE [--schema PATH]`，默认 schema 路径按脚本自身位置解析（`assets/eval-set.schema.json`），不依赖当前工作目录。
   - stdout 只输出一个 JSON 对象：`{"file", "valid", "errors": [...], "warnings": [...], "summary": {...}}`。每条 finding 有 `path`（JSON Pointer，如 `/cases/4/confusable_with`）、`rule`（schema 关键字或语义规则名，如 `required`、`minContains`、`duplicate-id`）、`message`（哪里错、期望什么）和 `fix`（具体改法，尽量用实际值，例如 `Add "confusable_with": "<the task this prompt could be mistaken for>" to /cases/4`，而不是 “Fix the field”）。
   - 退出码：0 通过（可有 warning）、1 有 error、2 参数错误或文件不存在、3 文件不是合法 JSON（`message` 含行号和列号）、4 依赖缺失。`--help` 写清所有字段、退出码和运行方式。
4. 写 `scripts/test_validate_evals.py`（`unittest`）：每个夹具至少一个用例，断言退出码和 `rule`；另加一个用例证明 `format` 被检查（去掉 format checker 时该用例应失败，可在注释里说明）；一个 `python3 -I -S` 的依赖缺失用例。
5. 写 `references/field-guide.md`（给模型看的）：每个字段的含义；怎样写好 positive / negative / near-miss（各给 1 个英文好例子和 1 个坏例子）；`confusable_with` 应该写什么。
6. 写 `SKILL.md`：
   - description 单行：做什么（为一个 skill 生成或修复触发评估集 JSON）、何时用（“write trigger tests for my skill / make an eval set / fix my evals.json”）、至少两条排除边界（例如：运行评估、改写 skill 的 description、评审输出质量）。
   - 正文 ≤ 60 行，写成一个明确的循环：读目标 skill 的 frontmatter → **何时**读 `references/field-guide.md`（例如“写 near-miss 之前”或“校验器报出你不理解的规则时”）→ 把草稿写到文件 → 运行校验命令 → 只改报错的 `path` → 重跑；**最多 3 轮**，仍不通过就停下来，把剩余错误原样告诉用户，不要交付未通过的文件，也不要为了通过去修改 schema。
   - 写明：模型不需要读 `assets/eval-set.schema.json`（脚本会读），也不需要读脚本源码；warning 怎么处理。
7. 行为测试（全新会话、普通提示词），**先写并提交 `tests/CHECKLIST.md`（早于任何 output）**：
   - skill-1：为仓库里的 `day-11/semver-next` 生成评估集。
   - skill-2：修复 `tests/fixtures/` 外另放的一个**至少含 3 个错误**的 `tests/broken-evals.json`（文件名中性，不要叫 “3-errors”）。
   - skill-3：一个 near-miss 提示词，例如 “Can you run the trigger tests in evals.json and tell me the pass rate?”，期望 skill **不**被激活（或激活后明确拒绝）。
   - baseline-1 / baseline-2：与 skill-1 / skill-2 相同的提示词，不装 skill，**但提示词里告诉它 schema 文件的路径**。运行结束后你自己用 `validate_evals.py` 校验基线产出的文件，把结果写进 RESULTS.md。
   - 每次运行 2-3 条可判断检查项，至少包括：最终文件通过校验；报告给用户的问题都来自校验输出、没有编造；skill-2 的日志里校验器至少运行了 2 次（证明真的循环了）。
   - 输出原样保存为 `output-skill-N.md`、`output-baseline-N.md`，产出的 JSON 保存为 `output-skill-N.json` 等；用脚本从 harness 日志提取证据：运行了几次 `validate_evals.py`、是否读了脚本源码或 schema、是否读了 field-guide.md 以及在第几步读的。
8. 写 `tests/RESULTS.md`（≤ 35 行）：validate（skills-ref）输出、单测结果和运行方式、夹具表、5 次运行逐条检查结果和日志证据、基线产出的校验结果，以及一段“区分度”分析：有 skill 和无 skill 的差别具体出现在哪些规则上（例如 `minContains`、条件必填、`format`），field-guide.md 有没有在预期的时机被读取。

**交付物**
- `day-13/eval-set-builder/SKILL.md`
- `day-13/eval-set-builder/assets/eval-set.schema.json`
- `day-13/eval-set-builder/references/field-guide.md`
- `day-13/eval-set-builder/scripts/validate_evals.py`
- `day-13/eval-set-builder/scripts/test_validate_evals.py`
- `day-13/eval-set-builder/tests/fixtures/`（≥ 9 个 JSON + `README.md`）
- `day-13/eval-set-builder/tests/broken-evals.json`
- `day-13/eval-set-builder/tests/CHECKLIST.md`
- `day-13/eval-set-builder/tests/output-skill-1..3.md`、`output-baseline-1..2.md`，以及对应产出的 JSON
- `tests/` 下的 harness 日志证据和提取脚本
- `day-13/eval-set-builder/tests/RESULTS.md`
- （可选）`day-13/NOTES.md`

**完成标准**
1. `name` 为 `eval-set-builder`，与目录同名；description 为单行纯字符串，写明做什么、何时用、至少两条排除边界；有 `compatibility` 字段；validate 通过，输出记在 RESULTS.md。
2. schema 是 Draft 2020-12 且能通过 `check_schema`；表中每条规则都在 schema 里实现（条件规则用 `if`/`then` 或等价写法，数量用 `contains` + `minContains`）。
3. 夹具和 `tests/fixtures/README.md` 的提交早于 `validate_evals.py` 的第一次提交（git log 可见），覆盖步骤 2 列出的全部 9 种情况。
4. 脚本有 PEP 723 块并固定 `jsonschema==4.26.0`；无交互；默认 schema 路径不依赖当前工作目录；`--help` 写明参数、输出字段、退出码 0-4 和运行方式。
5. stdout 只输出 JSON（退出码 2、4 时为空）；每条 finding 有 `path`、`rule`、`message`、`fix`；`format: date` 确实被校验；语义检查（重复 id、重复 prompt、prompt 含 skill 名）都实现且有用例。
6. 单测可直接运行并全部通过（运行方式写进 RESULTS.md）；每个夹具至少一个用例；有 `python3 -I -S` 的依赖缺失用例。
7. 正文 ≤ 60 行，包含：确切命令、何时读 field-guide.md、写文件 → 校验 → 只改报错位置 → 重跑的循环、最多 3 轮后的停止规则、不改 schema、不读 schema 和脚本源码、warning 的处理。
8. CHECKLIST.md 早于任何 output 提交；5 次运行全新会话、普通提示词，输出原样保存；检查项含“最终文件通过校验”“没有编造问题”和 skill-2 的“至少 2 次校验”。
9. 日志证据由脚本提取：skill-1、skill-2 执行了校验脚本且没读源码，skill-2 至少运行 2 次；skill-3 未激活（或激活后拒绝）；基线没有加载 skill，基线产出已用你的脚本校验。
10. RESULTS.md ≤ 35 行，含上述各项和区分度分析；skill 内容、脚本（注释、`--help`、错误信息）、schema 和 tests/ 文档使用英文（NOTES.md 可以用中文）。

**预计用时**：约 40 分钟（schema 和夹具约 12 分钟，脚本和单测约 15 分钟，正文和字段说明约 5 分钟，5 次运行约 8 分钟，可并行开会话）

**可选加分**
- day-12 遗留：`allowed-tools-not-string` 的 `fix` 用序列里的实际项生成，例如 `["Read", "Bash"]` → `allowed-tools: "Read Bash"`，加一个单测。
- 加 `--max-errors N`，避免一个结构性错误引出几十条连锁错误；在正文说明智能体应先修最上层的错误。
- 用 jsonschema 的 `best_match` 给出“最可能的根因”，放在输出的 `summary.primary` 里，并比较它和全部错误列表哪种更利于模型一次修好。
- 把同一份 schema 用另一个实现（例如 Node 的 `ajv`，或 `check-jsonschema` CLI）再跑一遍全部夹具，记录有没有不一致。

**参考链接**
- [Agent Skills: Best practices](https://agentskills.io/skill-creation/best-practices)（Validation loops、Plan-validate-execute、Templates for output format、progressive disclosure）
- [Agent Skills: Using scripts](https://agentskills.io/skill-creation/using-scripts)（结构化输出、错误信息、退出码、PEP 723）
- [Agent Skills specification](https://agentskills.io/specification)（`assets/` 与 `references/`、文件引用保持一层深）
- [jsonschema on PyPI](https://pypi.org/project/jsonschema/) 和 [jsonschema 文档](https://python-jsonschema.readthedocs.io/)（`iter_errors`、`json_path`、`FORMAT_CHECKER`、`best_match`）
- [JSON Schema: conditional subschemas](https://json-schema.org/understanding-json-schema/reference/conditionals)（`if`/`then`）和 [contains / minContains](https://json-schema.org/understanding-json-schema/reference/array#contains)
