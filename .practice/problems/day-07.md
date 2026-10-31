# day-07：Load Only Your Domain — an ecosystem-aware dependency-fix skill

- 出题日期：2026-10-31
- 阶段：第二阶段 · 渐进式披露（第 2 题：按领域拆分参考文件）

**学习目标**
- 掌握“按领域拆分”的渐进式披露：同一个 skill 覆盖多个领域，每次只加载相关的那一个领域文件。
- 写出基于客观信号（清单文件、锁文件）的路由规则，而不是靠猜。
- 测试两种最容易出错的情况：仓库里有多个领域但只该加载一个（过读），以及没有匹配领域、一个都不该加载。

**背景知识**
day-06 按“条件”拆分：时区、RCA 方法、敏感信息这些内容只在某类事故里才需要。今天练另一种常见结构，按“领域”拆分。Anthropic 最佳实践里把它叫做 domain-specific organization：一个 skill 覆盖多个领域（例子是 finance / sales / product），每个领域一个参考文件，用户问销售数据时只读 sales 文件，其他文件不占上下文。

依赖漏洞修复很适合这种结构。流程在各生态之间是一样的：确认受影响的包和版本，判断它是直接依赖还是传递依赖，选最小的修复，最后验证。但具体做法差别很大：
- **npm**：`npm ls <pkg>` 查依赖树；用 package.json 的 `overrides` 强制传递依赖版本（pnpm 用 `pnpm.overrides`，Yarn 用 `resolutions`）。
- **Python**：pip 用 constraints 文件（`-c`）；uv 在 `[tool.uv]` 下有 `constraint-dependencies` 和 `override-dependencies`，两者语义不同；漏洞扫描可用 `pip-audit`。
- **JVM**：Maven 用 `mvn dependency:tree` 和 `<dependencyManagement>`，默认按“最近者优先”调解版本；Gradle 用 dependency constraints。

共用的流程、输出模板、自检放在正文；生态特有的命令和坑放进各自的领域文件。正文里需要一张路由表，告诉智能体根据哪个文件判断生态、该读哪个参考文件。

**任务步骤**
1. 新建 `day-07/dependency-fix-plan/`，写 SKILL.md：description（单行），以及 ≤ 60 行的正文，包含共用修复流程、输出模板（如：Package / Current → Target / Direct or transitive / Fix / Verification / Risk）、返回前自检和路由表。
2. 写清楚路由规则：只加载拥有漏洞包的那个生态的文件。例如：
   `Read only the reference for the ecosystem that owns the vulnerable package. A repo that also contains other manifests does not need their references.`
   再写一条降级规则：遇到 go.mod、Cargo.toml 等没有领域文件的生态时，不读任何参考文件，按通用流程给出方案，并在输出里说明没有该生态的专门指导。
3. 写三个领域文件，各 40-120 行，使用相同的小节骨架，每个至少写 1 条该生态特有的坑。领域文件里不要重复正文的共用规则，也不要互相引用。
4. 自己写 5 个测试输入（每个 8-20 行，描述仓库文件和扫描结果即可，不需要真实项目）：N、P、J、M、G，要求见完成标准第 5 条。
5. 每个输入开一个全新会话运行，提示词用普通请求（如 “Our scanner flagged this, what should we change?”）。用脚本从 harness 会话日志中提取实际读取的文件，可以复用或改写 day-06 的 collect-harness.py。
6. 写 LOADING.md。如果 M 多读了 npm.md，或 G 读了任何参考文件，修改路由措辞后重跑。
7. 处理 day-06 遗留：用最终版 incident-postmortem 重跑 input-d，确认行动项每行都有 5 个单元格。

**交付物**
- `day-07/dependency-fix-plan/SKILL.md`
- `day-07/dependency-fix-plan/references/npm.md`、`python.md`、`jvm.md`
- `day-07/dependency-fix-plan/tests/input-n.md`、`input-p.md`、`input-j.md`、`input-m.md`、`input-g.md`
- `day-07/dependency-fix-plan/tests/LOADING.md`
- `tests/` 下的读取证据（从日志提取的结果）和提取脚本
- day-06 input-d 重跑结果（追加到 `day-06/incident-postmortem/tests/LOADING.md` 或写进 `day-07/NOTES.md`）
- （可选）`day-07/NOTES.md`

**完成标准**
1. 目录为 `day-07/dependency-fix-plan/`；`name` 与目录同名；description 单行纯字符串，写明做什么、何时用、至少一条排除边界（如普通的版本升级/新功能升级、写 commit message）；`agentskills validate` 通过。
2. SKILL.md 正文 ≤ 60 行，只放所有生态共用的内容：修复流程（确认受影响包和版本 → 判断直接/传递依赖 → 按“升级直接依赖 > 覆盖传递依赖 > 记录理由后暂缓”的顺序选最小修复 → 验证）、输出模板、返回前自检；外加一张路由表：判断依据（清单文件/锁文件名）→ 对应参考文件。
3. 路由规则明确：只加载拥有漏洞包的生态对应的文件，而不是仓库里出现的所有生态；没有匹配生态（如 go.mod、Cargo.toml）时不加载任何参考文件，正文给出通用降级做法，并说明没有该生态的专门指导。
4. 三个领域文件各 40-120 行，使用相同的小节骨架（如 Detect / Inspect the tree / Fix a direct dependency / Override a transitive dependency / Verify / Pitfalls），超过 100 行的开头有目录；每个文件至少 1 条该生态特有的坑（如 npm overrides 只在根 package.json 生效、pip 的 constraints 文件本身不安装任何包、Maven 的“最近者优先”依赖调解）；领域文件之间不互相引用，也不重复正文的共用规则。
5. tests/ 下 5 个自己编写的输入（每个 8-20 行）：N 只有 npm；P 是 Python（uv 或 pip）；J 是 Maven 或 Gradle；M 是同时含 package.json 和 pyproject.toml 的 monorepo，但漏洞只在 Python 侧（预期只加载 python.md）；G 是 Go 或 Rust 项目（预期不加载任何参考文件）。参考文件里的例子不能与这些输入使用同一个包或同一情形。
6. 每个输入在全新会话中运行，加载磁盘上的原始 skill 文件夹；提示词是普通请求，不提“测试/加载”；读取证据由脚本从 harness 会话日志中提取，模型自述不作为证据。
7. LOADING.md ≤ 30 行：表格列出输入、预期加载、实际加载（来自日志）、是否通过；各层大小（description 字符数、正文行数和约 tokens、每个领域文件约 tokens，按字符数 ÷ 4 估算）；每次运行实际加载的总 tokens 与“全部内容塞进一个 SKILL.md”的 tokens 对比；至少一段分析过读或漏读（尤其是 M 和 G），以及对路由措辞的修改。
8. day-06 遗留：用 day-06 最终版 skill 在全新会话中重跑 input-d，记录行动项每行是否都有 5 个单元格（附日志依据）。
9. skill 内容和 tests/ 下的文档使用英文。

**预计用时**：约 35-40 分钟（5 个输入都很短；提取脚本可复用 day-06 的）

**可选加分**
- 在 npm.md 内部区分 npm / pnpm / Yarn（按锁文件判断），不新增文件，验证 pnpm 输入不会去读别的文件。
- 在第二个平台（如 Claude Code 和 Codex 各一次）跑 M，比较两者的读取行为。
- 修正 day-04 的 Edge cases 措辞：`hold for owner review; do not recommend deletion.`

**参考链接**
- [Agent Skills specification](https://agentskills.io/specification)（Progressive disclosure、File references）
- [Skill authoring best practices（Anthropic）](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)（Pattern: Domain-specific organization）
- [npm package.json: overrides](https://docs.npmjs.com/cli/v10/configuring-npm/package-json#overrides)
- [uv: Resolution（constraints 与 overrides）](https://docs.astral.sh/uv/concepts/resolution/)
- [pip-audit](https://pypi.org/project/pip-audit/)
- [Maven: Introduction to the Dependency Mechanism](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)
- [Gradle: Dependency constraints](https://docs.gradle.org/current/userguide/dependency_constraints.html)
