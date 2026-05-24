# Final Demo Full Recording Script (Chinese)

这份讲稿给负责录制 demo 视频的同学使用。建议视频长度控制在 `4.5` 到 `5.5` 分钟。录制时以浏览器里的 Web UI 为主，不需要展示太多命令行和文件目录。

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

## 1. 开场：说明 demo 的目的

操作：打开 Web UI 首页，先不要急着点击。

口播：

大家好，这里展示的是我们软件测试 final project 的工具本身，也就是 `ARG-Test`。它是一个 requirement-driven 的 AI-enhanced AutoTestDesign 工具，目标是把自然语言 requirement 转换成结构化、可审计的黑盒测试设计结果。

这个 demo 主要证明三件事。第一，工具可以稳定运行，并支持 Direct Input、CSV Batch、State Model 和 Formal Evidence 这些核心入口。第二，输出不是普通的 prompt 文本，而是包含 test cases、checker diagnostics、risk assessment、state model 和 coverage information 的结构化结果。第三，最终实验数字来自已经冻结的 formal result bundle，并通过 replay 保证展示时可复现。

需要提前说明的是，本视频中的交互使用 `mock` provider，是为了保证录屏稳定、快速、可重复。我们不会把临时 ad hoc mock 输出当成 final benchmark；正式质量数字以后面 Formal Evidence Dashboard 和 frozen formal replay 为准。

## 2. Formal Evidence：先展示正式数字来源

操作：

1. 点击顶部导航栏的 `Formal Evidence`。
2. 停留在上方指标卡区域。
3. 依次指一下 `Official Test Requirements`、`Avg Structural Checker`、`Avg Overall Coverage`、`Avg Test Count`。

口播：

我们先看 `Formal Evidence` 页面，因为这里是最终报告、PPT 和答辩中最安全的正式数字来源。

这里显示我们的 held-out test split 一共有 `16` 个正式 test requirements。平均 `Structural Checker` 是 `0.959`，平均 `Overall Coverage` 是 `61.5%`，平均 test count 是 `7.312`。

这些数字不是现场临时生成的，而是来自冻结的 formal result snapshot。这样做的原因是，大模型 provider 可能存在网络波动和输出随机性，所以正式结果必须以 frozen artifacts 为准，而不是依赖录屏时现场调用 live API。

操作：

1. 向下看 Baselines 和 Category Generalization 区域。
2. 不需要滚很远，只要能看到 baseline 表即可。

口播：

下面的 baseline comparison 用来说明 ARG-Test 相比普通方法的价值。我们比较了 rule-based baseline、plain LLM baseline、structured no-checker ablation 和 full pipeline。Full pipeline 的 coverage 和 structural quality 都明显更强，说明我们的 checker、rerank 和 repair 并不是装饰，而是真正提升了输出质量。

Category generalization 部分说明这个方法不只适用于单一案例，而是在 business rules、input validation 和 workflow state 三类 requirement 上都有稳定表现。

## 3. Direct Input：展示正式样例的 frozen replay

操作：

1. 点击顶部导航栏的 `Direct Input`。
2. Requirement 下拉框选择 `pickup_station_contact_validation`。
3. 不要改文本框内容。
4. 点击 `Generate Test Suite`。
5. 等待页面显示 Completed。

口播：

接下来展示 Direct Requirement Input。这里可以从下拉框选择正式 test split 中的 requirement。我们选择 `pickup_station_contact_validation`，它是一个 input validation 类型的 requirement。

注意这里不要手动改 requirement 文本。因为当前文本和正式 requirement 完全匹配，所以点击生成后，系统会返回 frozen formal replay，而不是重新随机生成一个临时结果。

操作：

1. 指向 `Structural Checker = 0.950`。
2. 指向 `Overall Coverage = 71.3%`。
3. 指向 `Run Mode = Replay`。
4. 指向 `Result Source` 中的三个标签。

口播：

这里可以看到，`Structural Checker` 是 `0.950`，`Overall Coverage` 是 `71.3%`。更关键的是，页面显示 `Run Mode` 为 `Replay`，并且在 `Result Source` 中标注了 `Frozen formal replay`、`Matches Formal Evidence coverage` 和 `No live API call`。

这说明这个正式样例的结果来自已经冻结的 formal output，coverage 与 Formal Evidence Dashboard 中的正式结果一致，不是录屏时临时 mock 出来的数字。

操作：

1. 稍微向下看 `Risk Assessment`、`Recommended Focus`、`Generated Test Cases`。
2. 不需要逐条读完整表格。

口播：

继续往下可以看到 risk assessment、recommended testing focus 和 generated test cases。这个页面展示的不是简单的自然语言答案，而是结构化测试设计结果。测试用例中包含 test data、expected output、technique information 和 diagnostic information，方便后续审查、导出和复现。

## 4. CSV Batch：展示批量导入

操作：

1. 点击顶部导航栏的 `CSV Batch`。
2. 选择或上传 `final_docs/execution_evidence/sample_requirement_batch.csv`。
3. 点击运行按钮。
4. 等待结果表格出现。

口播：

接下来展示 CSV Batch。这个入口说明系统不只支持单条 requirement，也支持批量导入多个 requirement。

我们上传准备好的 sample CSV。这个 CSV 中的样例和正式 test requirement 匹配，因此系统会对匹配行使用 frozen replay。这样录屏时既能展示批量处理能力，又不会把临时 ad hoc mock 输出误当成正式实验结果。

操作：

1. 指向 batch size。
2. 指向每行里的 `Structural`、`Coverage`、`Risk`、`Source`。
3. 特别指出 `Frozen replay`。

口播：

结果表里可以看到每条 requirement 的 category、structural score、coverage、risk level 和 source。这里的 `Frozen replay` 表示对应行命中了正式 result snapshot，所以结果可以和 Formal Evidence 中的数字对应起来。

如果用户上传的是自己临时写的 CSV，系统仍然可以用 mock path 生成结果，但那种 ad hoc 结果只能说明工具能运行，不能作为 final benchmark 的正式质量数字。

## 5. State Model：展示 FR 4.0 状态建模

操作：

1. 点击顶部导航栏的 `State Model`。
2. Workflow Case 选择 `warehouse_pickup_order_workflow`。
3. 不要改文本框内容。
4. 点击 `Build State Model`。
5. 等待页面显示 Completed。

口播：

接下来展示 State-Model Extraction。这个部分对应 assignment 和 requirement specification 中的 `FR 4.0`，也就是从 workflow requirement 中建模系统行为，并生成覆盖状态和迁移的测试计划。

我们选择 `warehouse_pickup_order_workflow`，这是一个典型的 workflow-state requirement。

操作：

1. 指向顶部四个指标卡。
2. 读出 `States = 5`、`Legal Transitions = 4`、`Illegal Transitions = 2`、`Coverage Plans = 2`。

口播：

页面上方显示这个 requirement 被抽取出了 `5` 个 states、`4` 条 legal transitions、`2` 条 illegal transitions，以及 `2` 个 coverage plans。这里的 coverage plans 对应 all-states 和 all-transitions 这类状态覆盖目标。

操作：

1. 指向 Legal Transitions 表。
2. 指向 Illegal Transitions 表。
3. 如果页面够高，展示下方 coverage plan；不够就不用滚太多。

口播：

下面的表格展示了从 requirement 规则中抽取出的合法迁移和非法迁移。例如订单可以从 `READY_FOR_PICKUP` 到 `PICKED_UP`，也可以因为过期进入 `EXPIRED`；同时，像 `PICKED_UP` 回到 `READY_FOR_PICKUP` 这种路径会被识别为 illegal transition。

这里需要注意，如果某个 workflow requirement 本身没有显式非法迁移规则，那么 illegal transition 数量为 `0` 是合理的，不代表功能失败。我们检查的重点是状态和合法迁移是否能被结构化抽取，是否能形成可审计的 coverage plan。

## 6. 回到 Formal Evidence：连接实验结论

操作：

1. 回到 `Formal Evidence`。
2. 停留在指标卡和 baseline 区域。

口播：

现在再回到 Formal Evidence，把刚才的 live interaction 和正式实验结论连接起来。

Direct Input、CSV Batch 和 State Model 证明工具界面和核心功能可以稳定操作；Formal Evidence 则说明最终质量数字来自 frozen formal result bundle。这样我们既能展示一个可操作的工具，也能保证答辩时引用的实验数字是稳定、可复现、可追踪的。

## 7. Executable Evidence：补充详细执行证据

操作：

1. 如果时间允许，打开或展示 `coupon_module_evidence_scorecard.png`。
2. 路径：`final_docs/detailed_test_design_execution/figures/coupon_module_evidence_scorecard.png`
3. 如果不方便打开图片，也可以只口头说明。

口播：

除了 requirement-level 的测试设计，我们还准备了一个详细可执行模块作为证据，也就是 `coupon_discount_engine`。

这个模块完成了 `15` 个 module-focused tests，包括 black-box 和 white-box tests。执行结果达到 `100%` statement coverage、`100%` branch coverage，并且 `4 / 4` seeded mutants 全部被杀死。

这说明 final project 不只是生成测试文档，也有真实的 test execution evidence，能够证明测试设计对实际缺陷是有检测能力的。

## 8. 结束总结

操作：回到 Web UI 任意页面，最好停在 `Formal Evidence` 或 `Direct Input`。

口播：

总结一下，这个 demo 展示了 ARG-Test 的完整 final 状态。

第一，它支持 Direct Input、CSV Batch、State Model 和 Formal Evidence，说明工具不是单一脚本，而是一个可以交互使用的 AutoTestDesign prototype。

第二，它的输出是结构化和可审计的，包括 checker score、coverage、risk assessment、test cases、state transitions 和 export artifacts，而不是简单地让 LLM 输出一段文本。

第三，正式实验结果通过 frozen formal replay 和 Formal Evidence Dashboard 保证稳定可复现；同时，详细模块还提供了 black-box、white-box、coverage 和 mutation evidence。

因此，这个项目不仅完成了 assignment 对 AI-driven AutoTestDesign tool 的要求，也在结果可信度、可复现性和可执行证据方面做了额外加强。

## 9. 录制时不要说错的边界

下面这些不是口播正文，但录制时必须注意：

- 不要说我们训练或微调了 LLM。
- 不要说 rule-based baseline 来自某篇论文或开源系统；它是我们自己实现的 deterministic heuristic baseline。
- 不要说 live provider 完全 deterministic。
- 不要把 `checker_score` 说成 correctness；它是 structural contract consistency。
- 不要把临时修改 requirement 后生成的 ad hoc mock 结果说成正式 benchmark。
- 不要展示 `.env`、API key、长 JSON 或无关本地目录。

## 10. 如果时间不够的压缩版

如果视频必须控制在 3 分钟左右，只保留这四段：

1. Formal Evidence：展示 `16`、`0.959`、`61.5%`、`7.312`。
2. Direct Input：展示 `pickup_station_contact_validation` 的 `Frozen formal replay`。
3. State Model：展示 `warehouse_pickup_order_workflow` 的 states 和 transitions。
4. 结束总结：说明 frozen replay、structured output、executable evidence。
