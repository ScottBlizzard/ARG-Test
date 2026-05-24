# Demo Handoff For Recorder

这份文件给负责录制 demo 的同学。当前推荐录制路径是 Web UI：`http://127.0.0.1:8000/`。旧命令行步骤只作为 fallback，不是主流程。

## 1. 你要录的不是 PPT

你要录的是“工具演示视频”，不是照着 PPT 念，也不是报告朗读。视频目标很明确：

`证明 ARG-Test 工具可以稳定运行，并且 final 项目的核心功能、正式结果和可执行证据都已经准备好。`

录制逻辑建议是：

- 先展示 Formal Evidence，锁定正式数字。
- 再展示 Direct / CSV / State Model 三个交互入口。
- 最后补充 executable evidence。

## 2. 你需要准备什么

- PowerShell 终端。
- 浏览器打开 `http://127.0.0.1:8000/`。
- 示例 CSV：`final_docs/execution_evidence/sample_requirement_batch.csv`。
- 录制清单：`final_demo_recording_checklist_cn.md`。
- 口播稿：`final_demo_script_cn.md` 或 `final_demo_script_en.md`。

不需要你现场改代码，不需要你自己重新设计讲法，也不要临时找文件路径。

## 3. 推荐操作顺序

1. 在仓库根目录运行：

```powershell
python -m uvicorn demo_web.app:app --host 127.0.0.1 --port 8000
```

2. 打开 Web UI：`http://127.0.0.1:8000/`。
3. 先看 `Formal Evidence`，展示 `Avg Overall Coverage = 61.5%`。
4. 再看 `Direct Input`，选择 `pickup_station_contact_validation`，运行后指出 `Frozen formal replay`。
5. 再看 `CSV Batch`，上传 sample CSV，展示 `Frozen replay`。
6. 再看 `State Model`，选择 `warehouse_pickup_order_workflow`，展示 states 和 transitions。
7. 结尾提到 `coupon_discount_engine` 的 executable evidence。

## 4. 最重要的几句话

- `For stable interaction, we use mock mode in the demo.`
- `Formal examples replay frozen formal results, so the displayed coverage matches the final evidence.`
- `Ad hoc edited inputs are only for interaction demonstration, not final benchmark claims.`
- `The system outputs not only test cases, but also risk metadata, state models, and structured exports.`
- `The selected module is backed by executable black-box, white-box, and mutation evidence.`

## 5. 不要做的事

- 不要切到 live provider。
- 不要展示 `.env`、API key 或无关本地目录。
- 不要长时间滚动 JSON 或 markdown 原文。
- 不要把 ad hoc mock 输出说成正式实验结果。
- 不要说 checker score 等于 correctness。
