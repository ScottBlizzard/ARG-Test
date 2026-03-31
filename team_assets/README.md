# Team Assets

本目录不是最终提交给老师的正式论文内容，而是给组员协作用的工作资料。

当前成员：

- 1 号：许奕，技术总控 / 最终集成
- 2 号：张洛梧，文档与 PPT
- 3 号：数据集与主实验
- 4 号：Baseline
- 5 号：评测、消融、错误分析

## 当前协作模式

当前采用“两阶段协作模式”：

- 第一阶段：3/4/5 号只负责完成各自 runbook 中的 mock/结构版准备工作，把脚本、数据、输出格式、分析框架搭好。
- 第二阶段：等 3/4/5 号完成并提交交接模板后，后续真实模型接入、正式实验重跑、最终结果定版、结果汇总，统一由许奕负责。
- 张洛梧最终只接收许奕整理好的正式结果包，不直接以 3/4/5 号的 mock 结果写最终文档。

也就是说：

- 3/4/5 号现在不负责最终正式实验结论。
- 3/4/5 号做完各自 runbook 并完成交接后，这个阶段就结束。
- 后续正式版本全部由许奕接管。

建议阅读顺序：

1. 先看 `report_assets/team_task_allocation_cn.md`
2. 再看自己对应的 runbook：
   - 3 号看 `03_member3_runbook_cn.md`
   - 4 号看 `04_member4_runbook_cn.md`
   - 5 号看 `05_member5_runbook_cn.md`
3. 需要交结果时，用 `templates/member_handoff_template_cn.md`
4. 遇到问题时，用 `templates/issue_report_template_cn.md`
5. 文档引用结果时，看 `official_result_sources_cn.md`

使用原则：

- 所有正式结果都以 `outputs/reports/` 下的 JSON/CSV/Markdown 为准。
- 所有成员只改自己的拥有目录。
- 核心 pipeline、prompt、checker 最后只由许奕统一修改。
