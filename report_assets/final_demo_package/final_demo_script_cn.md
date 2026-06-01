# Final Demo Full Recording Script (Chinese)

这份讲稿给负责录制 demo 视频的同学使用。当前版本按 `3.5` 到 `4` 分钟展示压缩，录制时以浏览器里的 Web UI 为主，不需要展示太多命令行和文件目录。

## 0. 录制前准备

在仓库根目录运行：

```powershell
python -m uvicorn demo_web.app:app --host 127.0.0.1 --port 8000
```

然后浏览器打开：

```text
http://127.0.0.1:8000/
```

提前准备好 CSV 文件：

```text
final_docs/execution_evidence/sample_requirement_batch.csv
```

录制时只使用页面里的 `mock` provider。这里的 `mock` 是为了保证演示稳定；正式实验质量来自 frozen formal results 和 replay，不来自临时 ad hoc mock。

## 1. 三分钟录制流程

### 0:00 - 0:08 开场

操作：浏览器停留在 Web UI 首页。

口播一句话：

大家好，这里用三分钟展示 ARG-Test 如何把自然语言 requirement 转换成结构化、可审计、可 replay 的测试设计结果。

### 0:08 - 1:10 Output Preview / Direct Input / Manual Revision

操作：

1. 点击 `Direct Input`。
2. Requirement Case 选择 `pickup_station_contact_validation`。
3. 保持 provider 为 `mock`，不要改 requirement 文本。
4. 点击 `Generate Test Suite`。
5. 结果出现后，看右侧 `Output Preview / Generated Suite and Diagnostics`。
6. 向下滚动到生成后的 test-case editor。
7. 修改一条已有 case 的 `Expected Output` 或 `Priority`，再点击 `Add Test Case` 新增一条负例。
8. 填一行 `Revision Notes`，点击 `Export Revised Suite`。

发言稿：

第一步看 Output Preview。这里我选择一个正式 test split 中的 input validation requirement，然后点击生成。页面右侧可以看到 `Structural Checker = 0.950`，`Overall Coverage = 71.3%`，并且 `Run Mode` 是 `Replay`。

重点是 `Result Source` 这里标注了 `Frozen formal replay`、`Matches Formal Evidence coverage` 和 `No live API call`。也就是说，这个正式样例不是现场随机 mock 出来的，而是回放冻结的 formal result，因此页面数字和最终报告中的正式结果是一致的。

下面还能看到 risk assessment、recommended focus 和 generated test cases。它不是普通 prompt 文本，而是包含测试数据、expected output、技术类型和诊断信息的结构化输出。

更重要的是，页面现在支持 designer-in-the-loop review。我们可以先用左侧 review controls 指定 coverage focus，再在生成后直接修改单条 test case，新增负例，然后导出 revised suite。这样覆盖项、策略和测试用例三层都能被人工审查和修订。

### 1:10 - 1:45 CSV Batch

操作：

1. 点击 `CSV Batch`。
2. 上传 `final_docs/execution_evidence/sample_requirement_batch.csv`。
3. 点击 `Run Batch Analysis`。
4. 结果出现后看 `Batch Output / Requirement-Level Summary`。

发言稿：

第二步展示 CSV Batch。这个入口说明系统不仅能处理单条 requirement，也能批量导入 CSV。

运行后，结果区域会显示 batch size 和每条 requirement 的 compact result card，包括 category、structural score、coverage、risk 和 source。匹配正式 requirement 的行会显示 `Frozen replay`，表示它同样来自冻结正式结果；如果是临时改写的 ad hoc CSV，则只能作为功能演示，不能当成正式 benchmark。

### 1:45 - 2:30 State Model

操作：

1. 点击 `State Model`。
2. Workflow Case 选择 `warehouse_pickup_order_workflow`。
3. 不改文本内容。
4. 点击 `Build State Model`。
5. 结果出现后看 states、legal transitions、illegal transitions 和 coverage plans。

发言稿：

第三步展示 State Model，这对应 final requirement 里的 `FR 4.0`。我们选择 `warehouse_pickup_order_workflow`，点击构建状态模型。

页面显示这个 workflow 被抽取出了 `5` 个 states、`4` 条 legal transitions、`2` 条 illegal transitions 和 `2` 个 coverage plans。下面的表格展示了合法迁移和非法迁移，例如订单可以从 `READY_FOR_PICKUP` 到 `PICKED_UP`，但 `PICKED_UP` 回到 `READY_FOR_PICKUP` 会被识别为 illegal transition。

这里要注意，如果某个 requirement 没有显式非法迁移规则，illegal transitions 为 `0` 是合理的，不代表功能失败。

### 2:30 - 3:15 Formal Evidence

操作：

1. 点击 `Formal Evidence`。
2. 看顶部指标卡：`Official Test Requirements`、`Avg Structural Checker`、`Avg Overall Coverage`、`Avg Test Count`。
3. 快速扫一下 Baselines、Category Generalization、Reproducibility Snapshot。

发言稿：

最后看 Formal Evidence，这是最终报告、PPT 和答辩中最安全的正式数字来源。

这里显示 held-out test split 一共有 `16` 个 requirements，平均 `Structural Checker = 0.959`，平均 `Overall Coverage = 61.5%`，平均 test count 是 `7.312`。下面还有 baseline comparison、category generalization 和 reproducibility snapshot。

所以前面的 Direct、CSV 和 State Model 证明工具可以交互运行，而这里的 Formal Evidence 证明最终质量数字来自 frozen formal snapshot，不依赖现场 live API。

### 3:15 - 3:30 结束

操作：停在 `Formal Evidence` 页面即可。

口播一句话：

总的来说，ARG-Test 不只是一个 prompt demo，而是一个有结构化输出、人工可审查可修改、风险与状态建模、冻结结果 replay 和正式实验支撑的 AutoTestDesign 工具。

## 2. 录制时不要说错的边界

下面这些不是口播正文，但录制时必须注意：

- 不要说我们训练或微调了 LLM。
- 不要说 rule-based baseline 来自某篇论文或开源系统；它是我们自己实现的 deterministic heuristic baseline。
- 不要说 live provider 完全 deterministic。
- 不要把 `checker_score` 说成 correctness；它是 structural contract consistency。
- 不要把临时修改 requirement 后生成的 ad hoc mock 结果说成正式 benchmark。
- 不要展示 `.env`、API key、长 JSON 或无关本地目录。
