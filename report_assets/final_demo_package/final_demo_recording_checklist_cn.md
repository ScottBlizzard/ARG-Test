# Final Demo Recording Checklist

这份清单给负责录制 demo 视频的同学使用。最终视频建议以 Web UI 为主，不再按旧命令行脚本逐条录。

## 1. 录制前准备

- 打开仓库根目录：`D:\软件测试\Final\ARG-Test`
- 打开 PowerShell，工作目录切到仓库根目录。
- 运行 Web demo：

```powershell
python -m uvicorn demo_web.app:app --host 127.0.0.1 --port 8000
```

- 浏览器打开：`http://127.0.0.1:8000/`
- 准备好示例 CSV：`final_docs/execution_evidence/sample_requirement_batch.csv`
- 可以提前打开截图目录：`report_assets/final_demo_package/frontend_focus/screenshots/`

## 2. 推荐录制顺序

1. 先说明：本视频用 `mock` 保证交互稳定，用 `frozen formal replay` 支撑正式质量数字。
2. 打开 `Formal Evidence` tab，展示 `16` 个 test requirements、`Avg Overall Coverage = 61.5%`、baseline 和 category generalization。
3. 切到 `Direct Input`，选择 `pickup_station_contact_validation`，点击 `Generate Test Suite`。
4. 指出页面显示 `Replay`、`Frozen formal replay`、`Matches Formal Evidence coverage`、`No live API call`。
5. 向下滚动到 case editor，修改一条 case，再新增一条负例，点击 `Export Revised Suite`。
6. 强调这一步说明设计者可以在生成后直接修改测试用例并重新导出。
7. 切到 `CSV Batch`，上传 sample CSV，展示匹配正式样例的行显示 `Frozen replay`。
8. 切到 `State Model`，选择 `warehouse_pickup_order_workflow`，点击 `Build State Model`。
9. 展示 `States = 5`、`Legal Transitions = 4`、`Illegal Transitions = 2`、`Coverage Plans = 2`。
10. 最后回到 `Formal Evidence`，强调正式结论来自冻结结果，不来自临时 ad hoc mock。

## 3. 必须讲清楚的话

- `mock` 只用于稳定交互，不是 final benchmark 本身。
- 正式样例的 Direct/CSV 结果会 replay frozen formal output，所以 coverage 与 Formal Evidence 一致。
- Direct Input 现在支持生成后编辑测试用例并重新导出 reviewed suite。
- 如果手动改 requirement 文本，页面会走本地 mock 生成，这种结果不能引用为正式实验质量。
- `checker_score` 不是正确率；它是结构化契约检查分数。
- `overall_coverage` 来自人工 gold spec 的 obligation 覆盖，不是模型训练标签。

## 4. 不要做的事

- 不要选择 `openai` 或其他 live provider；当前正式 demo 只保留 `mock`。
- 不要现场修改代码。
- 不要展示 API key、`.env`、长 JSON 或无关目录。
- 不要把 coverage 为 `N/A` 或 ad hoc mock 的结果说成正式结果。
- 不要说 live provider 完全 deterministic。

## 5. 时间控制

- 最佳长度：`4` 分钟左右。
- 最长不建议超过 `5` 分钟。
- 如果时间不够，优先保留 Formal Evidence、Direct replay、State Model 三段。
