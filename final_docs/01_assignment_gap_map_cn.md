# Assignment Gap Map

本文件用于把老师要求与当前仓库资产逐项对齐，并明确 final 阶段还差什么。

## 1. AI-driven AutoTestDesign Tool

当前已具备：

- `src/` 中的主流程、checker、baselines、exporter、evaluation
- `prompts/` 中的 prompts
- `README.md` 中的基本运行说明
- `experiments/` 中的实验脚本

当前缺口：

- final 版 README 表述仍偏“脚手架”，还不够“课程最终成品”
- 缺风险优先级表达的成型功能入口
- 缺 final demo 说明与视频材料

下一步：

- 将 README 调整为 final 交付导向
- 补 final demo checklist
- 视情况补 risk scoring / prioritization 输出

## 2. Risk Analysis Report

当前已具备：

- 有 failure analysis、limitations、风险讨论素材
- 有 `outputs/reports/test/failure_analysis_cn.md`

当前缺口：

- 没有独立成型的 risk analysis report
- 缺统一的风险评分口径和风险优先级表

下一步：

- 在 `final_docs/` 中形成独立风险分析文档
- 将系统风险、实验风险、交付风险区分开

## 3. Test Plan

当前已具备：

- 有报告大纲、实验结构、模块划分、团队角色
- 有主实验、baseline、ablation、generalization 输出

当前缺口：

- 缺正式的 test plan 文档
- 缺 schedule/checklist、cost estimation、framework rationale 的课程式写法

下一步：

- 输出完整 test plan 文档
- 把仓库模块、测试层级、框架选型、进度与成本写清楚

## 4. Detailed Test Design and Execution Document

当前已具备：

- 有多类 requirement、gold specs、final_tests、checker logs
- 有一批适合选作重点模块的需求案例

当前缺口：

- 缺“聚焦一个主模块”的详细设计文档
- 缺明确的 white-box 执行闭环
- 缺可直接截图放到报告/PPT 的执行证据

下一步：

- 选定 `coupon_discount_engine` 作为主模块
- 补 reference implementation
- 用 `pytest` + `coverage` 形成 detailed execution evidence

## 5. Presentation

当前已具备：

- `report_assets/` 中已有 proposal / outline / figures

当前缺口：

- final 版展示结构未定稿
- 缺 demo 路径、视频录制脚本、答辩问答准备

下一步：

- 补 final PPT 结构和 demo 流程
- 从 `outputs/`、`artifacts/` 中选定展示证据

## 6. 结论

结论不是“要不要重做”，而是：

1. 代码主仓库不需要重做。
2. final 文档和执行证据必须系统补齐。
3. 重点不是加更多散碎内容，而是把“工具、证据、文档、展示”收成一套闭环。
