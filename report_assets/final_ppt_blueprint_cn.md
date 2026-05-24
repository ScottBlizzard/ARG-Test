# Final PPT Blueprint

## 1. 使用目的

这份文档不是最终 PPT，而是给制作 PPT 的同学使用的完整制作蓝图。目标是让对方明确：

- 整个答辩应该讲什么故事
- 每一页应该放什么
- 哪些图可以直接复用
- 哪些案例必须人工挑选和人工裁剪
- 哪些说法必须讲清楚，避免重复中期答辩时老师提出的疑问

推荐时长：

- `15` 分钟主讲
- `13` 到 `16` 页主幻灯片
- `3` 到 `5` 页 backup slides

推荐总叙事：

1. 任务是什么，为什么 plain LLM 不够
2. 我们的方法是什么，为什么不是“只会 prompt 一下”
3. 我们做了哪些 final 级升级
4. 实验结果是否成立，是否比 baseline 强
5. 这个项目是否有真正可执行、可复现、可 defend 的证据

一句话主结论建议固定为：

`ARG-Test is an auditable and risk-aware requirement-driven testing pipeline that turns plain LLM prompting into structured, checked, and reproducible black-box test design.`

---

## 2. 先给做 PPT 的人看的结论

### 2.1 最终应该优先展示什么

最优先展示的强项只有四个：

- 我们不是直接让 LLM 胡乱出测试，而是有 `structured trace + parser + checker + rerank/repair`
- 主结果明显强于 `rule-based`、`plain LLM`、`structured-no-checker`
- 我们不仅有设计级结果，还有 `coupon_discount_engine` 的可执行证据
- 我们现在有稳定 Web demo，正式样例走冻结 formal replay，页面数字和报告数字一致
- 我们对 reproducibility / stability 讲得严谨，没有乱吹

### 2.2 不要在 PPT 里花太多时间的内容

- 不要把所有仓库模块都逐个念一遍
- 不要把所有 16 个 requirement 都展示
- 不要把所有中间文件路径塞满一页
- 不要把 live nondeterminism 讲得像失败点
- 不要把 final report 逐页压缩成 PPT

### 2.3 这套 PPT 最该避免的误区

- 不要说“我们训练了模型”或“我们 fine-tune 了模型”
- 不要说“rule-based baseline 来自某篇论文”或“直接引用了某现成系统”
- 不要说“我们已经做到了严格 live 3-seed fully deterministic”
- 不要把 `checker_score` 说成“最终正确率”
- 不要把 `gold spec` 说成训练数据

---

## 3. 数字口径锁定

PPT 里涉及实验数字时，优先以 final report 当前正式口径为准。建议 PPT 制作者不要自己重新抄数字，而是直接从这里拿。

### 3.1 数据集与评估设置

- `dev = 50`
- `test = 16`
- 三类 requirement：
- `business_rules`
- `input_validation`
- `workflow_state`

### 3.2 主结果

- Full pipeline:
- `avg checker score = 0.959`
- `avg overall coverage = 0.615`
- `avg test count = 7.312`

### 3.3 Baselines

- Rule-based:
- `0.753 / 0.147 / 4.125`
- Plain LLM:
- `0.844 / 0.030 / 7.250`
- Structured No Checker:
- `0.841 / 0.538 / 6.312`

### 3.4 Category-level generalization

- Business Rules:
- `score = 0.957`
- `coverage = 0.577`
- Input Validation:
- `score = 0.950`
- `coverage = 0.579`
- Workflow State:
- `score = 0.970`
- `coverage = 0.697`

### 3.5 Detailed module evidence

- `15 module tests passed`
- `38 repo tests passed`
- `100% statement coverage`
- `100% branch coverage`
- `4 / 4 mutants killed`

### 3.6 Reproducibility / stability

- Mock `3-run` repeatability:
- `16 / 16 stable`
- Live multi-seed sample:
- `1 / 5 stable`
- Live same-seed sample:
- `0 / 3 stable`
- 正确说法：
- `seed-controlled pipeline + archive-grade replay reproducibility`

---

## 4. 主幻灯片完整大纲

下面按“推荐页码 - 标题 - 核心信息 - 页面内容 - 所需图片 - 人工处理要求 - 建议讲法”给出完整大纲。

### Slide 1. Title

目标：

- 一页讲清楚项目名、课程、组别、成员、最终定位

页面内容：

- 标题：`ARG-Test`
- 副标题：`Auditable and Risk-Aware Requirement-Driven Black-Box Test Generation`
- `Software Testing 42036101 Final Project`
- `Group 7`
- 成员姓名和学号

图片：

- 可不放图
- 或右下角放一张很淡的架构图缩略图

人工处理要求：

- 标题不要太长，占两到三行即可
- 成员信息以 final report 首页为准

讲法：

- 一句话说清楚：这是一个从自然语言 requirement 自动生成可审计黑盒测试的 AI-enhanced testing pipeline

建议时长：

- `0.5 min`

### Slide 2. Problem and Final Scope

目标：

- 讲清楚我们选的是 requirement-driven branch
- 讲清楚问题是什么，不是做 code generation，也不是做 static analysis

页面内容：

- 左侧：
- `Input: natural-language requirements`
- `Output: auditable black-box test suites`
- 右侧：
- 为什么难：
- 需要 valid / invalid partitions
- 需要 boundaries
- 需要 rule combinations
- 需要 legal / illegal transitions

图片：

- 不强制
- 可以用一个 very light 的 `Requirement -> Test Suite` 箭头示意

人工处理要求：

- 这一页不要堆公式，不要放实验图

讲法：

- 强调我们选了作业允许的 `system-requirement input` 分支，并把它做完整了

建议时长：

- `0.8 min`

### Slide 3. Why Plain LLM Is Not Enough

目标：

- 建立问题张力
- 让后面的 checker / repair / structured trace 显得必要

页面内容：

- Plain LLM 的问题：
- 输出 fluent，但不一定可审计
- 容易漏 invalid cases
- 容易漏 boundary neighbors
- 容易说用了某 technique，但其实没有覆盖其 obligations

图片：

- 最好人工做一个左右对比框
- 左：`plain answer`
- 右：`auditable structured trace`

可选素材：

- 从 `plain_llm` 的任意一条输出里截一小段
- 或直接手工画一个两栏对比框，避免塞原始长文本

人工处理要求：

- 这一页不要贴太长原始输出
- 只要 2 到 4 行对比即可

讲法：

- 核心句：`The problem is not only correctness. The deeper issue is auditability.`

建议时长：

- `0.9 min`

### Slide 4. Final System Overview

目标：

- 把“我们不是一个 prompt”讲清楚

页面内容：

- 一页只做一件事：讲 pipeline

主图：

- 架构图

推荐图片：

- 直接用你手画的架构图
- 优先使用：
- [arg_test_architecture_editable.pptx  -  已修复.pptx](/D:/软件测试/Final/ARG-Test/report_assets/figures/arg_test_architecture_editable.pptx%20%20-%20%20已修复.pptx)
- 或其最终导出版本

人工处理要求：

- 这张图已经够好了，不要重画
- 只需保证 PPT 中清晰度够高

讲法：

- 强调五个关键控制点：
- structured generation
- parser/schema gate
- technique-aware checker
- rerank/repair
- export/evaluation

建议时长：

- `1.1 min`

### Slide 5. Structured Trace and Contract Checking

目标：

- 讲清楚技术核心

页面内容：

- 上半部分：
- `Analysis`
- `Pattern`
- `Steps`
- `Verification`
- `FinalAnswer`
- 下半部分：
- EP checker
- BVA checker
- Decision checker
- State checker

图片：

- 这一页建议直接在 PPT 内手工画，不必额外找图片
- 因为做成流程框比截图更清楚

人工处理要求：

- 不要直接粘 LaTeX / Markdown
- 用 5 个盒子 + 4 个 checker 小标签即可

讲法：

- 强调“LLM reasoning is turned into a typed artifact”

建议时长：

- `1.2 min`

### Slide 6. What Was Upgraded for the Final

目标：

- 让老师看出 final 不是 middle 原样提交

页面内容：

- Middle -> Final 的升级清单
- 新增：
- risk-aware prioritization
- state-model extraction
- CSV/direct input
- detailed executable evidence
- NFR validation
- mutation usefulness demo
- seeded repeatability and replay
- Web demo formal catalog and frozen-result replay

图片：

- 不需要外部图
- 可以用一个 `Before / After` 双栏排版

人工处理要求：

- 这一页不要讲数字，只讲 final 升级闭环

讲法：

- 用“we closed the strict final-project gaps”这个逻辑

建议时长：

- `0.9 min`

### Slide 7. Experimental Setup and Evaluation Protocol

目标：

- 这一页要一次解决中期答辩老师问过的两个大疑问

必须明确写在页面上的内容：

- `dev = 50, test = 16`
- `dev is used for prompt/checker/repair tuning`
- `test is frozen for final evaluation`
- `No model training or fine-tuning`
- `Coverage is measured against manually authored gold specs`

推荐页面布局：

- 左栏：dataset split
- 右栏：evaluation dimensions

页面内容：

- gold spec covers:
- valid partitions
- invalid partitions
- boundaries
- decision rules
- states
- illegal transitions
- exception cases

图片：

- 不需要外部图
- 直接在 PPT 内做 mini table 即可

人工处理要求：

- 这页一定要清楚，不能让人误以为你们在训练模型

讲法：

- 明确说：
- `The dev/test split was used for tuning and final evaluation, not for model training.`
- `The gold spec is an evaluation rubric derived from each requirement, not training data.`

建议时长：

- `1.2 min`

### Slide 8. Baselines and Fair Comparison

目标：

- 回答“rule-based baseline 到底是什么”

页面内容：

- 四个方法：
- Rule-based
- Plain LLM
- Structured No Checker
- Full ARG-Test

页面上必须写清楚：

- `Rule-based baseline = our own deterministic heuristic non-AI baseline`
- `Inspired by classical black-box testing ideas`
- `Not a trained model`
- `Not directly taken from a paper or OSS project`

图片：

- 不强制
- 可做一个 4 行比较表

人工处理要求：

- 这页的 rule-based baseline 描述一定要准确

讲法：

- 可以直接沿用中期老师问题的澄清逻辑

建议时长：

- `0.9 min`

### Slide 9. Main Result Scorecard

目标：

- 用最紧凑的方式先把总体成绩打出来

推荐图片：

- [final_result_scorecard.png](/D:/软件测试/Final/ARG-Test/report_assets/figures/final_result_scorecard.png)

页面要点：

- `16 test requirements`
- `avg checker score = 0.959`
- `avg overall coverage = 0.615`
- `0 duplicate cases`

人工处理要求：

- 如果这一页已经有 scorecard 图，文字不要再重复太多

讲法：

- 先给结论，再给解释

建议时长：

- `0.8 min`

### Slide 10. Main Comparison Against Baselines

目标：

- 这是实验最关键的一页

推荐图片：

- [main_vs_baselines.png](/D:/软件测试/Final/ARG-Test/report_assets/figures/main_vs_baselines.png)

页面要点：

- Full pipeline beats:
- `rule-based`
- `plain LLM`
- `structured-no-checker`

必须讲清楚：

- 对 `rule-based`：显著更强
- 对 `plain LLM`：说明光 prompt 不够
- 对 `structured-no-checker`：说明 checker / repair 有实际价值

人工处理要求：

- 这页最好再配 1 句人工总结，不要只扔图

讲法：

- 核心句：
- `The gain is not only against a weak traditional baseline, but also against a stronger structured AI variant.`

建议时长：

- `1.2 min`

### Slide 11. Generalization and Ablation

目标：

- 同时回答“能不能跨类别泛化”和“提升来自哪里”

推荐图片：

- [generalization_by_category.png](/D:/软件测试/Final/ARG-Test/report_assets/figures/generalization_by_category.png)
- [ablation_gain.png](/D:/软件测试/Final/ARG-Test/report_assets/figures/ablation_gain.png)

推荐布局：

- 左：generalization
- 右：ablation

页面要点：

- `workflow_state` 不是空壳，category-level score 很强
- ablation 说明 checker-guided control 不是装饰

必须确保的数字口径：

- Structured No Checker:
- `0.841 / 0.538 / 6.312`
- Full Pipeline:
- `0.959 / 0.615 / 7.312`

人工处理要求：

- 不要再插单独的 ablation 表，图加一句总结就够

讲法：

- `The full pipeline improves both checker-aligned quality and practical obligation coverage.`

建议时长：

- `1.2 min`

### Slide 12. Representative Cases

目标：

- 这页是最需要人工挑选的
- 不应该直接贴 3 张完整 markdown 表

推荐做法：

- 只展示 `3` 个案例
- 每个案例只展示：
- requirement 核心规则 2 到 3 条
- 采用的 testing techniques
- 2 到 4 个代表性测试
- 如果是 workflow，用状态/转移摘要替代表格

推荐案例池：

- Business-rule 主案例：
- `coupon_discount_engine`
- Input-validation 主案例：
- `pickup_station_contact_validation`
- Workflow-state 主案例：
- `warehouse_pickup_order_workflow`

备选案例池：

- `order_split_shipment_state_machine`
- `payment_3ds_authentication_flow`
- `payment_card_expiry_and_cvv_validation`

不建议优先上屏的案例：

- `address_international_format_validation`
- 原因：coverage 偏低

说明：

- `order_approval_state_machine` 可以作为 backup 使用，但不要因为 illegal transition 数量为 `0` 就说它失败；这个 requirement 本身没有显式非法迁移规则。
- `return_exchange_approval_workflow` 现在可以用于 state-model 备选展示，但主 PPT 仍建议优先用 `warehouse_pickup_order_workflow`，因为它的合法/非法迁移更直观。

可直接取材的文件：

- [coupon_discount_engine.md](/D:/软件测试/Final/ARG-Test/.local_runs/formal_qwen_novpn/outputs/final_tests/test/coupon_discount_engine.md)
- [pickup_station_contact_validation.md](/D:/软件测试/Final/ARG-Test/.local_runs/formal_qwen_novpn/outputs/final_tests/test/pickup_station_contact_validation.md)
- [warehouse_pickup_order_workflow.md](/D:/软件测试/Final/ARG-Test/.local_runs/formal_qwen_novpn/outputs/final_tests/test/warehouse_pickup_order_workflow.md)
- [warehouse_pickup_order_workflow state model](/D:/软件测试/Final/ARG-Test/.local_runs/formal_qwen_novpn/outputs/state_models/test/warehouse_pickup_order_workflow.md)

人工处理要求：

- 这页必须人工裁剪
- 不要原样贴完整输出
- 去掉 `pending / Pending`
- 不要把 `repaired boundary input` 这种修补行原样放上去
- 表述可以在 PPT 上改得更自然，但数值和含义不能改

讲法：

- 核心句：
- `The method works across different requirement structures, not just on one hand-picked example.`

建议时长：

- `1.4 min`

### Slide 13. Detailed Executable Evidence

目标：

- 证明项目不只是“生成测试文档”

推荐图片：

- [coupon_module_evidence_scorecard.png](/D:/软件测试/Final/ARG-Test/final_docs/detailed_test_design_execution/figures/coupon_module_evidence_scorecard.png)

页面要点：

- `coupon_discount_engine`
- `15 module tests passed`
- `100% statement`
- `100% branch`
- `4 / 4 mutants killed`

可选补充：

- 放一小行说明：black-box + white-box + mutation

人工处理要求：

- 这页尽量简洁，别再放大表

讲法：

- `This gives us executable evidence, not only design-level metrics.`

建议时长：

- `1.0 min`

### Slide 14. Reproducibility and Practical Validation

目标：

- 这页要讲得诚实，但不能讲成自爆

推荐图片：

- [reproducibility_stability_overview.png](/D:/软件测试/Final/ARG-Test/report_assets/figures/reproducibility_stability_overview.png)
- 可选补一张前端正式结果页截图：[web_demo_formal_evidence_dashboard.png](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/frontend_focus/screenshots/web_demo_formal_evidence_dashboard.png)

建议页面结构：

- 左侧放 reproducibility 图
- 右侧放 3 条总结

右侧建议文案：

- repository-level deterministic chain under seeded mock control
- seeded live experiments supported, but provider variance remains
- frozen generations + replay guarantee submission-level reproducibility
- Web demo uses frozen replay for formal examples, not ad hoc live coverage claims

可选补充：

- 右下角再用 2 条 bullet 写 NFR：
- direct text / CSV supported
- no secret leak found, regression suite passes

人工处理要求：

- 这页不能说“strict live deterministic”
- 也不要把 `0/3` 说成项目失败

讲法：

- 正确讲法：
- `We separate pipeline-level reproducibility from provider-level nondeterminism.`

建议时长：

- `1.0 min`

### Slide 15. Limitations and Honest Boundaries

目标：

- 这页是加分页，不是减分页

页面内容：

- requirement-driven branch only
- test split is course-scale, not benchmark-scale
- coverage depends on authored gold specs
- live provider still has residual nondeterminism

人工处理要求：

- 别写太长
- 只放 3 到 4 条

讲法：

- 强调这些是 scope limitation，不是 method collapse

建议时长：

- `0.7 min`

### Slide 16. Conclusion

目标：

- 干净收尾

推荐内容：

- 一句结论
- 三条 takeaways

推荐三条：

- auditable structured generation
- clear gains over non-AI and weaker AI baselines
- executable and reproducible evidence beyond a minimal course project

图片：

- 可不放图
- 或小号放 scorecard 缩略图

建议时长：

- `0.6 min`

---

## 5. Backup Slides 建议

Backup slides 非常重要，因为老师中期问过的问题基本都可以预先做成备份页。

### Backup 1. Clarification on Dev/Test Split

必须写清楚：

- no training
- no fine-tuning
- dev for prompt/checker/repair tuning
- test frozen for final evaluation

### Backup 2. Clarification on Rule-Based Baseline

必须写清楚：

- self-implemented deterministic heuristic baseline
- theoretical inspiration from classical black-box testing
- not a trained model
- not directly copied from a paper or OSS system

### Backup 3. Clarification on Coverage Computation

必须写清楚：

- coverage is computed against manually authored gold specs
- gold spec lists applicable obligations
- overall coverage is averaged over applicable dimensions

### Backup 4. Detailed Module Evidence

可放：

- black-box / white-box mapping
- coverage summary
- mutation table

### Backup 5. Workflow State-Model Example

推荐用：

- `warehouse_pickup_order_workflow`

素材：

- [warehouse_pickup_order_workflow state model](/D:/软件测试/Final/ARG-Test/.local_runs/formal_qwen_novpn/outputs/state_models/test/warehouse_pickup_order_workflow.md)

---

## 6. 图片与素材清单

下面列的是 PPT 制作时最值得直接复用的现有图表。

### 6.1 必用图

- 架构图：
- [arg_test_architecture_editable.pptx  -  已修复.pptx](/D:/软件测试/Final/ARG-Test/report_assets/figures/arg_test_architecture_editable.pptx%20%20-%20%20已修复.pptx)
- 总体结果：
- [final_result_scorecard.png](/D:/软件测试/Final/ARG-Test/report_assets/figures/final_result_scorecard.png)
- baseline 比较：
- [main_vs_baselines.png](/D:/软件测试/Final/ARG-Test/report_assets/figures/main_vs_baselines.png)
- generalization：
- [generalization_by_category.png](/D:/软件测试/Final/ARG-Test/report_assets/figures/generalization_by_category.png)
- ablation：
- [ablation_gain.png](/D:/软件测试/Final/ARG-Test/report_assets/figures/ablation_gain.png)
- reproducibility：
- [reproducibility_stability_overview.png](/D:/软件测试/Final/ARG-Test/report_assets/figures/reproducibility_stability_overview.png)
- 详细执行证据：
- [coupon_module_evidence_scorecard.png](/D:/软件测试/Final/ARG-Test/final_docs/detailed_test_design_execution/figures/coupon_module_evidence_scorecard.png)
- 前端 Direct 冻结回放截图：
- [web_demo_direct_frozen_replay.png](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/frontend_focus/screenshots/web_demo_direct_frozen_replay.png)
- 前端 State Model 截图：
- [web_demo_state_model_extraction.png](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/frontend_focus/screenshots/web_demo_state_model_extraction.png)
- 前端 Formal Evidence 截图：
- [web_demo_formal_evidence_dashboard.png](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/frontend_focus/screenshots/web_demo_formal_evidence_dashboard.png)

### 6.2 可选图

- 风险热力图：
- [risk_priority_heatmap.png](/D:/软件测试/Final/ARG-Test/final_docs/risk_analysis_report/figures/risk_priority_heatmap.png)
- case study 拼图：
- [case_study_snapshots.png](/D:/软件测试/Final/ARG-Test/report_assets/figures/case_study_snapshots.png)

### 6.3 不建议直接搬上主 PPT 的图

- `stability_sanity_check.png`
- 原因：信息价值不如 `reproducibility_stability_overview.png`

### 6.4 前端截图怎么用

这三张前端截图已经按最终 demo 页面重新截好，做 PPT 的同学不需要自己重新跑页面才能开始排版。

- `web_demo_direct_frozen_replay.png`：用于证明 Direct Input 不是随便 mock 出一个数字，而是对正式样例返回 `Frozen formal replay`，覆盖率显示 `71.3%`，并且有 `No live API call` 标签。
- `web_demo_formal_evidence_dashboard.png`：用于证明最终正式数字来自 Formal Evidence Dashboard，尤其是 `Avg Overall Coverage = 61.5%`。
- `web_demo_state_model_extraction.png`：用于证明 `FR 4.0` 不是空口说法，页面能显示 states、legal transitions、illegal transitions 和 coverage plans。

使用建议：

- 主 PPT 只放 `formal dashboard` 或 `direct replay` 其中一张即可，避免 UI 截图过多。
- demo 视频里可以完整走 Direct -> State Model -> Formal Evidence 三步。
- 如果老师问“为什么有些数是 0”，回答时只说：没有显式非法迁移规则的 requirement 不应强行产生 illegal transition；我们检查的是合法迁移是否非空、是否与规则一致。

---

## 7. 人工必须完成的挑选与裁剪工作

这部分一定要让做 PPT 的人知道，因为这不是自动生成图就能解决的。

### 7.1 必须人工挑的案例

至少人工确定这三类案例各一个：

- `business_rules`
- `input_validation`
- `workflow_state`

推荐首选：

- `coupon_discount_engine`
- `pickup_station_contact_validation`
- `warehouse_pickup_order_workflow`

### 7.2 必须人工检查的地方

- 输出里是否还有 `pending / Pending`
- 是否还有明显模板残留
- expected output 是否自然
- requirement 规则太长时，是否已经裁剪成 2 到 3 条核心规则
- workflow 页是否更适合用 state-model 摘要而不是测试表

### 7.3 建议怎么裁剪案例

Business-rule 页：

- 左边放 requirement 核心规则
- 右边放 3 到 4 个代表性测试

Input-validation 页：

- 左边放字段与边界
- 右边放 valid / invalid / boundary 代表项

Workflow-state 页：

- 左边放 states + legal / illegal transitions
- 右边放 one sequence plan 或 3 个关键状态迁移

### 7.4 最不建议的做法

- 直接截图整张 markdown 表
- 直接把 raw output 原样贴上去
- 一页塞三个完整案例
- 在 slide 上保留 `Checker Status = pending`

---

## 8. 对老师中期问题的防御性处理

老师中期问到的点，这次应该主动讲清楚，而不是等问到再解释。

### 8.1 关于为什么 split 成 dev 和 test

PPT 正确口径：

- `We did not train the LLM.`
- `The dev split was used for prompt refinement, checker adjustment, repair tuning, and pipeline debugging.`
- `The test split was frozen for final evaluation and report writing.`

### 8.2 关于 rule-based baseline 是什么

PPT 正确口径：

- `The rule-based baseline is our own deterministic heuristic non-AI baseline.`
- `It is inspired by classical black-box testing ideas such as EP, BVA, decision tables, and state-transition thinking.`
- `It is not a trained model, and it is not directly adopted from a paper or existing project.`

### 8.3 关于 final coverage 怎么算

PPT 正确口径：

- `Coverage is computed against a manually authored gold specification for each requirement.`
- `The gold spec is an evaluation rubric, not training data.`
- `We measure coverage on applicable dimensions and then average them into final overall coverage.`

---

## 9. 不该说的话

下面这些说法会给自己找麻烦，PPT 和答辩都要避免：

- `We trained the model on our dataset.`
- `The rule-based baseline is from a paper.`
- `Our live provider is fully deterministic under 3 seeds.`
- `Checker score directly equals real-world correctness.`
- `Gold specs are labels used to teach the model.`

---

## 10. 做 PPT 时的优先级

如果时间紧，按这个顺序做：

1. 先把 Slide 1 到 Slide 10 做完
2. 再做 Slide 13 `Detailed Executable Evidence`
3. 再做 Slide 14 `Reproducibility and Practical Validation`
4. 最后做 Slide 12 `Representative Cases`

原因：

- 实验主结果和 detailed evidence 是最硬的
- case-study 页面最花人工，但也是最容易做丑的，所以应该最后精修

---

## 11. 给 PPT 制作者的最后建议

这套 PPT 不应该做成“把报告内容浓缩一遍”，而应该做成“带着老师快速看到 strongest evidence 的 defense deck”。

最重要的执行原则只有四条：

- 一页一个消息
- 主结果图不要超过两张同屏
- 案例页必须人工裁剪
- 主动回答中期老师问过的问题

如果这四条做到了，这套 PPT 的完成度会明显高于中期。
