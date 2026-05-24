# Frontend Demo Focus Guide

如果你负责 `demo UI / 前端展示 / 录屏`，优先看这份文件。旧的命令行脚本和旧讲稿只作为备份材料；最终展示应以 `demo_web/` 前端页面为主。

## 1. 需要关注的文件

- 前端页面：`demo_web/static/index.html`
- 前端脚本：`demo_web/static/app.js`
- 前端样式：`demo_web/static/styles.css`
- 后端接口：`demo_web/app.py`
- 示例 CSV：`final_docs/execution_evidence/sample_requirement_batch.csv`
- 正式结果快照：`formal_results_snapshot/`
- 已截好的前端截图：`screenshots/`

## 2. 录制前怎么运行

在仓库根目录运行：

```powershell
python -m uvicorn demo_web.app:app --host 127.0.0.1 --port 8000
```

然后打开：

```text
http://127.0.0.1:8000/
```

只使用页面里的 `mock` provider。这里的 `mock` 是为了保证录屏稳定，不代表 final 质量来自临时 mock 输出。

## 3. 页面上必须讲清楚的数据

### Direct Input

- 先选择下拉框里的正式 requirement，例如 `pickup_station_contact_validation`。
- 点击 `Generate Test Suite` 后，重点看 `Structural Checker`、`Overall Coverage`、`Run Mode`、`Result Source`。
- 如果显示 `Frozen formal replay`，说明它读取的是冻结正式输出，coverage 应与 Formal Evidence Dashboard 一致。
- 如果你手动改了 requirement 文本，结果会走本地 mock 生成路径，这种结果不能当作正式实验结论。

### CSV Batch

- 使用 `Download Sample CSV` 或上传 `final_docs/execution_evidence/sample_requirement_batch.csv`。
- 关注每行的 `Structural`、`Coverage`、`Risk`、`Source`。
- 匹配正式 requirement 的行应该显示 `Frozen replay`。

### State Model

- 推荐展示 `warehouse_pickup_order_workflow`。
- 重点讲 `States`、`Legal Transitions`、`Illegal Transitions`、`Coverage Plans`。
- 如果某个 requirement 的 illegal transition 数量是 `0`，不要说这是失败；没有显式非法规则时，非法迁移为 0 是合理结果。

### Formal Evidence

- 这是正式数字的最高优先来源。
- 必须能看到 `Official Test Requirements = 16`、`Avg Structural Checker = 0.959`、`Avg Overall Coverage = 61.5%`、`Avg Test Count = 7.312`。
- PPT 和答辩中的正式实验数字都应以这里和 frozen formal snapshot 为准。

## 4. 已准备好的截图

- `screenshots/web_demo_direct_frozen_replay.png`
- `screenshots/web_demo_state_model_extraction.png`
- `screenshots/web_demo_formal_evidence_dashboard.png`

这些截图可以直接给 PPT 同学使用。录屏同学仍建议自己实际操作一遍，保证视频里能展示真实交互。

## 5. 正确讲法

- `We use mock mode for stable interaction, and frozen formal replay for official claims.`
- `The formal dashboard is the safest source for final numerical claims.`
- `Checker score measures structural contract consistency, not real-world correctness.`
- `Coverage is measured against manually authored gold specifications, not training labels.`

## 6. 不要这样说

- 不要说我们训练或微调了模型。
- 不要说 rule-based baseline 来自某篇论文或现成系统。
- 不要说 live provider 在 3 seed 下完全 deterministic。
- 不要把 ad hoc mock 结果当成 final benchmark。
