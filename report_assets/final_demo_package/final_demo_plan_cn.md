# Final Demo Plan

## 1. Demo 目标

这个 demo 不是要把整篇报告复述一遍，而是要在较短时间内让老师看到三件事：

- 这个工具真的能运行，而不是只有报告和图片
- 这个工具支持 final 作业要求里的关键功能，而不是只有最简单的黑盒测试生成
- 最终实验结果和可执行证据已经准备好，不是临时拼接

因此本 demo 采用 `hybrid demo` 结构：

- `live` 部分使用 `mock provider`，保证现场或录屏时稳定、快速、可重复
- `formal evidence` 部分使用已经冻结的正式结果和图表，展示项目真实最终质量

这样安排的好处是：

- 不依赖 API 网络状态
- 不需要担心 live provider 波动
- 仍然能真实展示工具的输入、运行、输出和证据链

## 2. 推荐时长

推荐时长：

- `4` 到 `5` 分钟

推荐拆分：

1. `0:00 - 0:20` 开场和 demo 范围
2. `0:20 - 1:10` live command demo
3. `1:10 - 2:40` live output inspection
4. `2:40 - 3:40` formal result figures
5. `3:40 - 4:20` executable evidence and close

## 3. Demo 结构

### Part A. 快速说明

要讲清楚：

- 我们的工具输入是 natural-language requirements
- 支持 `direct text`、`CSV batch`、`state-model extraction`
- live demo 用 `mock` 模式，只为了稳定展示功能链
- 最终项目质量看正式 frozen result

### Part B. 现场运行三段命令

要现场跑的三段：

1. `run-text`
2. `batch-csv`
3. `state-model`

目的分别是：

1. 证明支持 direct user input
2. 证明支持 batch CSV import 和 structured export
3. 证明支持 state-model extraction 和 sequence planning

### Part C. 展示生成后的输出

重点看：

- `direct_text_demo_summary.json`
- `csv_order_workflow.md`
- `warehouse_pickup_order_workflow.md`

这里不是要逐行念，而是让老师看到：

- 有 risk score
- 有 candidate control
- 有 final test export
- 有 state model 和 coverage plan

### Part D. 展示最终正式结果

重点图：

- `final_result_scorecard.png`
- `main_vs_baselines.png`
- `reproducibility_stability_overview.png`

这里的作用是把 live mock demo 和 final project quality 接起来。

### Part E. 展示详细可执行证据

重点图：

- `coupon_module_evidence_scorecard.png`

这里一页足够，强调：

- `15 module tests`
- `100% statement`
- `100% branch`
- `4/4 mutants killed`

## 4. 为什么不用 live provider 录视频

这不是回避，而是正确的工程决策。

原因：

- live provider 有残余 nondeterminism
- 录视频时最怕网络/API 超时或返回漂移
- assignment 需要的是可信的视频 demonstration，不是直播冒险

因此这次 demo 采用的正确口径是：

`We use mock mode for stable live interaction, and frozen formal outputs to represent the final experimental quality of the project.`

## 5. Demo 成功标准

这个 demo 只要做到下面五点，就已经是高质量：

- 录屏过程中命令真实执行成功
- 至少展示 `direct text / CSV / state-model` 三个功能入口
- 至少展示一份 final test export 和一份 state model export
- 至少展示主结果图和 detailed evidence 图
- 讲清楚 mock live demo 和 frozen formal result 的关系
