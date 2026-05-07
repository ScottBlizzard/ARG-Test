# Final 高标准策略

## 目标定位

本项目不按“满足最低提交要求”推进，而按下面 5 个标准推进：

1. 作业完整度：4 类必交物全部齐全，且互相对应。
2. 技术可信度：报告中的结论必须能追溯到仓库内正式结果文件。
3. 可展示性：演示流程清晰，15 分钟内能讲明问题、方法、结果、局限。
4. 可答辩性：关键设计选择、指标、失败模式、传统方法对比都能自圆其说。
5. 可复现性：仓库结构、脚本入口、结果来源和文档引用路径统一。

## 最终项目的最佳叙事

最强叙事不是“我们用 LLM 生成了测试用例”，而是：

`ARG-Test` 将需求到测试设计的过程结构化、可检查、可修复、可导出，并在 final 阶段进一步补上风险分析、测试计划、详细执行和可演示证据。

建议最终叙事结构：

1. 问题：直接用 LLM 生测例，不可审计，覆盖不稳定。
2. 方法：五段式 trace + technique-specific checker + rerank/repair。
3. 结果：比 plain LLM 和 rule-based baseline 更完整、更可解释。
4. 提升：final 阶段增加风险优先级、正式测试计划、可执行模块、答辩材料。

## 当前基础

当前仓库已经具备这些强项：

- 需求驱动黑盒测试生成主流程
- EP / BVA / Decision Table / State Transition 的结构化支持
- parser / checker / rerank / repair
- baselines / ablation / generalization
- 导出 JSON / CSV / Markdown
- 现成的报告/PPT/图表资产

## 当前短板

当前离“高质量 final”还有 6 个短板：

1. 缺正式的 final 文档体系，尤其是风险分析和测试计划。
2. 缺一个聚焦模块的详细测试设计与执行证据。
3. 缺明确的 white-box 执行支撑。
4. 缺视频 demo 方案和答辩脚本。
5. 一些现有输出仍偏模板化，占位痕迹明显。
6. 需要把“中期基线”和“final 进行中内容”彻底分开。

## 推荐主模块

建议把 `coupon_discount_engine` 作为详细测试设计与执行的主模块，理由：

1. 它天然适合 EP、BVA、Decision Table 三种黑盒技术联用。
2. 它容易补一个小型 reference implementation，便于做 branch-level white-box 测试。
3. 它的业务逻辑清晰，适合做课堂展示和答辩。

建议把 `order_approval_state_machine` 或 `payment_3ds_authentication_flow` 作为辅助 case study，用来展示 workflow/state 类需求的能力和局限。

## 提高标准的具体做法

相比老师最低要求，建议额外做到：

1. 所有主结论都对应到仓库中的固定结果文件。
2. 至少一个模块做到“黑盒设计 + 白盒执行 + 结果分析”闭环。
3. 风险分析不只写文字，要形成可排序的风险表。
4. 测试计划不只列标题，要写出 test level、framework rationale、cost、schedule。
5. 演示中给出真实仓库路径、真实输出文件、真实案例。

## 近期优先级

### P0

- 完成 final 文档骨架
- 明确最终引用哪些正式结果文件
- 选定详细执行主模块

### P1

- 补风险评分与优先级表达
- 补 reference implementation 与 pytest/coverage
- 跑一轮可作为 final 的正式结果

### P2

- 打磨图表与 PPT
- 准备 demo 视频与答辩问答
