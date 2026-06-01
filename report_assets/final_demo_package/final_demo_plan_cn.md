# Final Demo Plan

这份 plan 给录制 demo 和制作 PPT 的同学使用。最终展示以 Web UI 为主，旧命令行流程只作为 backup。

## 1. Demo 目标

Demo 只需要证明四件事：

- 工具可以稳定运行，支持 Direct Input、CSV Batch、State Model、Formal Evidence。
- 默认正式样例走 frozen formal replay，页面数字与正式结果一致。
- 系统输出不是普通文本，而是包含 checker、coverage、risk、test cases、state model 的结构化结果。
- 设计者可以在生成前调整 review focus，并在生成后直接修改测试用例再导出 revised suite。
- 项目还有 executable evidence：`coupon_discount_engine` 的 `15` 个 module tests、`100%` statement/branch coverage、`4 / 4` mutants killed。

## 2. 推荐视频结构

| 时间 | 页面 | 重点 |
| --- | --- | --- |
| `0:00-0:20` | Title / opening | 说明 mock 用于稳定交互，formal replay 用于正式结论。 |
| `0:20-1:10` | Formal Evidence | 展示 `16` requirements、`0.959` structural、`61.5%` coverage、baselines。 |
| `1:10-2:10` | Direct Input | 选择 `pickup_station_contact_validation`，生成后指出 `Frozen formal replay`，再演示 case editor 和 revised-suite export。 |
| `2:10-2:45` | CSV Batch | 上传 sample CSV，展示匹配正式样例的行显示 `Frozen replay`。 |
| `2:45-3:25` | State Model | 选择 `warehouse_pickup_order_workflow`，展示 states / legal / illegal transitions。 |
| `3:25-4:10` | Evidence / PPT figure | 展示 detailed executable evidence scorecard。 |
| `4:10-4:30` | Closing | 总结 structured、checked、reviewable、reproducible、executable evidence。 |

## 3. 推荐展示样例

- Direct Input：`pickup_station_contact_validation`，coverage `71.3%`，适合展示输入验证和 frozen replay。
- Direct Input 的 case editor：适合演示“修改一条 expected output + 新增一条负例 + 导出 revised suite”。
- CSV Batch：使用 `final_docs/execution_evidence/sample_requirement_batch.csv`。
- State Model：`warehouse_pickup_order_workflow`，`5` states、`4` legal transitions、`2` illegal transitions，最直观。
- Formal Evidence：必须展示 `Avg Overall Coverage = 61.5%`。

## 4. 可直接用的截图

- `frontend_focus/screenshots/web_demo_direct_frozen_replay.png`
- `frontend_focus/screenshots/web_demo_state_model_extraction.png`
- `frontend_focus/screenshots/web_demo_formal_evidence_dashboard.png`

这些截图已经来自当前 Web demo，可直接放进 PPT 或作为录屏前的视觉参考。

## 5. 必须避免的说法

- 不要说我们训练了模型或 fine-tune 了 LLM。
- 不要说 rule-based baseline 来自某篇论文或开源项目。
- 不要说 live provider 完全 deterministic。
- 不要把 checker score 说成 correctness。
- 不要把 ad hoc mock output 当成 final benchmark。
