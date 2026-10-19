# AI Skill 练习课程大纲（约 30 天）

每天一个约 30 分钟的练习，难度逐步上升。题号是练习序号，不是日历日；没完成的题不会跳过。
课程会根据评审中暴露的弱点动态调整（插入巩固题、调整顺序）。

## 第一阶段：格式基础（day-01 ~ day-05）
1. 第一个 SKILL.md：frontmatter（name / description）、正文结构、触发测试清单
2. 写好 description：同一个 skill 写 3 个版本的 description，用正例/反例提示词比较触发准确度
3. 正文指令的写法：步骤化、示例输入输出、边界情况；避免含糊和过度约束
4. 可选 frontmatter 字段：license、compatibility、metadata、allowed-tools（实验性）的用途与取舍
5. 阶段小结：用 skills-ref validate 校验前几天的 skill，修复问题

## 第二阶段：渐进式披露（day-06 ~ day-10）
6. 拆分长 SKILL.md：把详细资料移入 references/，正文只留何时读取哪个文件
7. 多领域 skill：按领域分 reference 文件（如 finance.md / legal.md），让智能体只加载需要的部分
8. assets/ 的使用：模板、schema、查找表
9. 上下文预算：估算各层 token（元数据 ~100、正文 <5000、资源按需），给一个臃肿 skill 瘦身
10. 阶段小结：重构一个"什么都塞进 SKILL.md"的 skill

## 第三阶段：配套脚本（day-11 ~ day-15）
11. 第一个 scripts/：把确定性步骤（解析、校验）交给脚本
12. 脚本的健壮性：清晰的错误信息、依赖说明、边界情况
13. 脚本 + 参考文件组合：校验输出格式（例如 JSON schema 校验）
14. 让模型"运行而不是阅读"脚本：在指令中写清调用方式和输出解读
15. 阶段小结：一个带脚本、参考文件和模板的完整 skill

## 第四阶段：测试与评估（day-16 ~ day-20）
16. 触发评估：设计正例/反例/近似反例提示词集
17. 输出评估：为 skill 写期望输出和评分标准（rubric）
18. 对比测试：有 skill vs 无 skill 的效果差异
19. 迭代 description：根据误触发/漏触发调整措辞
20. 阶段小结：为一个 skill 建立可重复运行的小型评估集

## 第五阶段：跨平台可移植（day-21 ~ day-25）
21. 各平台的 skill 发现路径（.agents/skills、.claude/skills、.codex/skills、.cursor/skills、Copilot 等）
22. 避免厂商专有假设：工具名、路径、模型特性
23. compatibility 字段与降级策略
24. 把一个 skill 在至少两个平台上实际安装并测试
25. 阶段小结：发布一个可移植的 skill 仓库结构（含 README 和安装说明）

## 第六阶段：组合与架构（day-26 ~ day-30）
26. skill vs MCP 工具：何时用哪个，以及 skill 如何指导智能体使用 MCP 工具
27. skill vs 系统提示词 / 自定义指令（AGENTS.md、CLAUDE.md、copilot-instructions.md）
28. 多个 skill 协作：职责划分、避免触发冲突
29. 安全性：脚本权限、不可信输入、allowed-tools
30. 毕业项目：设计并实现一个完整的 skill 套件，附评估和跨平台说明
