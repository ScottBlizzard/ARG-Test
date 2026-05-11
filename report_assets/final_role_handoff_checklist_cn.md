# Final 角色交接清单

## 1. 这份清单是给谁的

这份文档是写给下面几类同学的：

- 风险分析报告负责人
- Test Plan 负责人
- Detailed Test Design and Execution Document 负责人
- demo 视频录制负责人
- PPT 制作负责人

目的不是讨论项目方向，而是把**现在必须统一的口径、不能说错的话、要补的点、以及各自最该注意的坑**一次说清楚。

---

## 2. 先统一一个前提

老师现在新发的 [Requirement_Specification.md](/D:/软件测试/Final/ARG-Test/Requirement_Specification.md:1) 应该被视为：

- 这次 final 项目的**正式需求规格说明**
- 后续三份文档、demo、PPT、答辩 Q&A 的**统一需求来源**

也就是说，后面不要再用“这是我们自己定义的系统功能”这种口径，而要用：

`Our final project is implemented and validated against the provided Requirement Specification of the AutoTestDesign AI App.`

---

## 3. 全组统一口径

下面这些是所有人都必须统一的，不允许各说各话。

### 3.1 项目是什么

我们的项目是：

- requirement-driven `AutoTestDesign AI App`
- 输入 natural-language requirements
- 输出 structured, auditable black-box testing artifacts

### 3.2 这次 final 选择的是哪条路线

我们实现的是：

- `system-requirement input` 分支

不是：

- codebase-driven branch
- static analysis tool
- model training project

### 3.3 统一需求来源

后续一切文档和答辩都要锚定到：

- [Requirement_Specification.md](/D:/软件测试/Final/ARG-Test/Requirement_Specification.md:1)

尤其是这些条目：

- `FR 1.0` Input / Parsing
- `FR 1.1` Requirement Structuring
- `FR 2.0` Risk Analysis & Prioritization
- `FR 3.0` Black-Box Test Design
- `FR 4.0` White-Box Test Modeling
- `FR 5.0` Test Oracle Generation
- `FR 6.0` Output & Export
- `FR 7.0` Test Suite Optimization

以及：

- `NFR 4.1` Performance
- `NFR 4.2` Usability / UX / UI
- `NFR 4.3` Security
- `NFR 4.4` Maintainability and Technology

### 3.4 统一实验数字

PPT、报告、demo 里涉及数字时，统一按 final report 当前正式口径：

- `dev = 50`
- `test = 16`
- Full pipeline:
- `avg checker score = 0.959`
- `avg overall coverage = 0.615`
- `avg test count = 7.312`

Baselines:

- Rule-based: `0.753 / 0.147 / 4.125`
- Plain LLM: `0.844 / 0.030 / 7.250`
- Structured No Checker: `0.841 / 0.538 / 6.312`

Detailed module evidence:

- `15 module tests passed`
- `27 repo tests passed`
- `100% statement coverage`
- `100% branch coverage`
- `4 / 4 mutants killed`

### 3.5 统一结果来源

正式结果统一引用：

- `.local_runs/formal_qwen_novpn`

不要混用：

- exploratory runs
- mock outputs
- 旧的 `outputs/reports/test` 历史残留

### 3.6 不准说错的话

下面这些口径全组统一禁止：

- `We trained the model on our dataset.`
- `The rule-based baseline comes from a paper or an existing project.`
- `The gold spec is training data.`
- `The checker score equals correctness.`
- `The live provider is fully deterministic under 3 seeds.`

---

## 4. 风险分析报告负责人要注意什么

对应文档：

- [02_risk_analysis_report_cn.md](/D:/软件测试/Final/ARG-Test/final_docs/risk_analysis_report/02_risk_analysis_report_cn.md:1)
- [02_risk_analysis_report_cn.pdf](/D:/软件测试/Final/ARG-Test/final_docs/risk_analysis_report/02_risk_analysis_report_cn.pdf)

### 4.1 这次最大的变化

风险来源不能再只写成“我们项目实现里有哪些风险”，而要写成：

- 基于 `Requirement_Specification` 的 FR/NFR compliance risk

### 4.2 必须显式覆盖的风险类别

你至少要确保风险报告里能覆盖这些方向：

- `FR coverage risk`
- `NFR compliance risk`
- `UI gap risk`
- `performance claim risk`
- `traceability/documentation risk`
- `demo/presentation interpretation risk`

### 4.3 最该补的几个点

这几项要特别小心：

1. `NFR 4.2.1 UI risk`
- 我们当前主体是 CLI + artifact-based workflow
- 不要假装已经有完整 web app
- 但要强调：工具可用性已经通过 CLI, direct text, CSV, state-model, structured export 体现

2. `NFR 4.1 performance risk`
- 不要轻易宣称完全满足 “100 requirements within 5 seconds”
- 更稳的写法是：
- mock/local processing is fast
- provider-bound live latency is an accepted boundary

3. `NFR 4.4.3 documentation risk`
- 要把 architecture, README, final docs, demo package 都作为 mitigation evidence 写进去

### 4.4 不要怎么写

- 不要把风险写成泛泛的项目管理废话
- 不要全是 “time is limited / members are busy”
- 不要脱离 Requirement Specification 自说自话

### 4.5 最好引用哪些证据

- `final_docs/`
- `report_assets/final_latex_report/main.pdf`
- `report_assets/final_demo_package/`
- `.local_runs/formal_qwen_novpn`

---

## 5. Test Plan 负责人要注意什么

对应文档：

- [03_test_plan_cn.md](/D:/软件测试/Final/ARG-Test/final_docs/test_plan/03_test_plan_cn.md:1)
- [03_test_plan_cn.pdf](/D:/软件测试/Final/ARG-Test/final_docs/test_plan/03_test_plan_cn.pdf)

### 5.1 这次最大的变化

Test Plan 里的 `system under test` 必须明确写成：

- `AutoTestDesign AI App`

不要写成模糊的：

- our project
- our framework
- our testing idea

### 5.2 Test items 必须映射到 Requirement Specification

这部分必须能对齐：

- `FR 1.0`: CSV / plain text / direct input
- `FR 1.1`: requirement structuring / parsing
- `FR 2.0`: risk scoring
- `FR 3.0`: EP / BVA / Decision Table / State Transition
- `FR 4.0`: state-model extraction / All States / All Transitions
- `FR 5.0`: expected-result synthesis
- `FR 6.0`: export to Markdown / JSON / CSV
- `FR 7.0`: rerank / repair / prioritization

### 5.3 NFR 部分一定要写得更像正式测试计划

尤其要明确这些：

- `Performance`: 我们如何测、如何解释边界
- `Usability`: 当前是 CLI-based prototype interface
- `Security`: no secret leak + basic safe artifact handling
- `Maintainability`: modular repo structure + scripts + docs

### 5.4 最敏感的问题

老师如果问：

`你们不是说它是一个 app 吗，UI 在哪里？`

Test Plan 里必须提前给口径：

- current final deliverable uses a CLI-centered prototype interface
- direct text, CSV batch, and state-model commands serve as the current usable interface
- this is a prototype-grade interface rather than a polished frontend product

### 5.5 不要怎么写

- 不要把 test plan 写成 final report 摘要
- 不要只列测试技术，不列被测 FR/NFR
- 不要用空泛 schedule，必须有实际 phase

### 5.6 最好引用哪些材料

- [Requirement_Specification.md](/D:/软件测试/Final/ARG-Test/Requirement_Specification.md:1)
- [arg_test_architecture_editable.pptx  -  已修复.pptx](/D:/软件测试/Final/ARG-Test/report_assets/figures/arg_test_architecture_editable.pptx%20%20-%20%20已修复.pptx)
- [README.md](/D:/软件测试/Final/ARG-Test/README.md:1)

---

## 6. Detailed Test Design and Execution 负责人要注意什么

对应文档：

- [04_detailed_test_design_execution_cn.md](/D:/软件测试/Final/ARG-Test/final_docs/detailed_test_design_execution/04_detailed_test_design_execution_cn.md:1)
- [04_detailed_test_design_execution_cn.pdf](/D:/软件测试/Final/ARG-Test/final_docs/detailed_test_design_execution/04_detailed_test_design_execution_cn.pdf)

### 6.1 这次你受影响最大

原因很简单：

- Requirement Specification 讲的是 `AutoTestDesign AI App`
- 你当前 detailed execution 的核心模块是 `coupon_discount_engine`

老师可能会问：

`你测的是你们做的 AutoTestDesign，还是外部 coupon engine？`

### 6.2 正确口径

你不能把 `coupon_discount_engine` 讲成系统本体。

最稳的说法是：

- `coupon_discount_engine` is the selected executable validation module
- it is used to demonstrate the usefulness and executability of the generated or curated test design
- it complements, rather than replaces, the validation of the AutoTestDesign app itself

### 6.3 你必须补清楚的两层对象

Detailed document 里最好显式区分两层：

1. `AutoTestDesign app feature under validation`
- requirement ingestion
- risk scoring
- state-model extraction
- structured export

2. `Executable usefulness anchor`
- coupon_discount_engine

### 6.4 你现有强项不要丢

这些是你最硬的证据，必须保住：

- `15 passed`
- `27 passed`
- `100% statement`
- `100% branch`
- `4/4 mutants killed`

### 6.5 你最需要避免的坑

- 不要让人觉得你在测一个和主项目无关的小程序
- 不要把 coupon module 当成整个 app 的唯一被测对象
- 不要忘记把它和 `FR 5 / FR 6 / usefulness demonstration` 挂钩

### 6.6 建议你在文档里补一句解释

建议显式出现类似表述：

`The selected executable module is not the whole AutoTestDesign application itself. It is the reference feature used to validate that the generated test design can be translated into concrete black-box and white-box execution evidence.`

---

## 7. Demo 视频录制负责人要注意什么

对应资料包：

- [final_demo_package](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package)

最重要的文件：

- [demo_handoff_cn.md](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/demo_handoff_cn.md:1)
- [final_demo_recording_checklist_cn.md](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/final_demo_recording_checklist_cn.md:1)
- [final_demo_script_cn.md](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/final_demo_script_cn.md:1)
- [prepare_demo_workspace.ps1](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/prepare_demo_workspace.ps1:1)

### 7.1 你这次最受影响

因为 `Requirement_Specification` 明确写了：

- `FR 1.0` input modes
- `FR 2.0` risk score
- `FR 4.0` state model
- `FR 6.0` export
- `NFR 4.2.1` interface

所以 demo 不能只录“生成几条测试”。

### 7.2 你必须在视频里展示什么

至少要展示这三段：

1. `run-text`
2. `batch-csv`
3. `state-model`

然后至少要打开：

- direct text summary
- 一个 CSV 结果
- 一个 state-model 输出
- baseline comparison 图
- detailed module evidence 图

### 7.3 正确口径

一定要说：

- live 部分使用 `mock` 是为了稳定和可重复
- final project 真实质量由 frozen formal result 表示

### 7.4 不要说错

- 不要说“这就是我们的最终 live 实验结果”
- 不要说“这证明 live provider 完全稳定”
- 不要把 mock demo 当成正式 benchmark

### 7.5 你真正的目标

demo 只要证明三件事就够：

- 工具真的能运行
- 输出真的结构化
- final 项目真的有正式结果和可执行证据

---

## 8. PPT 制作负责人要注意什么

对应资料：

- [final_ppt_blueprint_cn.md](/D:/软件测试/Final/ARG-Test/report_assets/final_ppt_blueprint_cn.md:1)
- [ppt_outline.md](/D:/软件测试/Final/ARG-Test/report_assets/ppt_outline.md:1)

### 8.1 这次必须新增的两页

至少要补这两页：

1. `Requirement Coverage`
2. `NFR / Boundaries`

### 8.2 Requirement Coverage 页必须讲什么

把 `FR 1.0 ~ FR 7.0` 和现有项目对应起来：

- input modes
- parser / structuring
- risk scoring
- black-box techniques
- state-model extraction
- oracle / expected result
- export
- optimization

### 8.3 NFR 页必须讲什么

一定要提：

- `Performance`: what we measured and what remains provider-bound
- `Usability`: current lightweight web UI plus stable backend demo shell
- `Security`: no secret leak found
- `Maintainability`: modular structure and documentation

### 8.4 最敏感的 PPT 问题

PPT 里最容易被老师追问的是：

- 你们是不是训练了模型
- rule-based baseline 是什么
- coverage 怎么算
- UI 到底在哪里

所以你必须在主讲或 backup 里提前覆盖：

- dev/test split clarification
- rule-based baseline clarification
- gold-spec coverage clarification
- why the final demo uses a lightweight web UI backed by the existing pipeline

### 8.5 案例页最容易做坏

这几件事必须人工处理：

- 去掉 `pending / Pending`
- 不要整张 markdown 截图
- workflow 页尽量用 state-model 摘要，不用长表

---

## 9. 你们五个人都必须知道的答辩敏感点

### 9.1 UI 问题

Requirement Specification 里写了 UI，这会被问。

统一回答：

- current final deliverable includes a lightweight web UI backed by FastAPI plus the original CLI workflow
- it already supports direct text input, CSV import, output viewing, and state-model generation
- the project prioritizes stable feature demonstration and evidence completeness over building a large standalone product frontend

### 9.2 Performance 问题

Requirement Specification 里写了很硬的性能指标，这也可能被问。

统一回答：

- mock/local path is fast enough for demonstration
- live runtime depends on provider latency
- our final evaluation focuses on functionality, coverage, usefulness, and evidence-backed validation

### 9.3 Rule-based baseline 问题

统一回答：

- it is our own deterministic heuristic non-AI baseline
- inspired by classical black-box testing ideas
- not trained
- not copied from a paper or OSS system

### 9.4 Gold spec 问题

统一回答：

- gold spec is an evaluation rubric
- manually derived from each requirement
- not training data

---

## 10. 各位最后交付前的自检

### 风险报告负责人

- 有没有显式引用 `Requirement_Specification`
- 有没有覆盖 FR/NFR 风险
- 有没有处理 UI/performance/documentation 风险

### Test Plan 负责人

- 有没有把被测对象写成 `AutoTestDesign AI App`
- 有没有把 FR/NFR 映射成 test items
- 有没有解释当前 interface 形态

### Detailed 负责人

- 有没有解释 `coupon_discount_engine` 和主系统的关系
- 有没有保住 executable evidence 这组硬证据
- 有没有避免“只测外部模块”的误解

### Demo 负责人

- 有没有跑 `run-text / batch-csv / state-model`
- 有没有展示 structured outputs
- 有没有展示 final figures

### PPT 负责人

- 有没有补 requirement coverage 页
- 有没有补 NFR 页
- 有没有准备老师中期问过的问题的 backup slides

---

## 11. 给你们的最后一句话

这次 Requirement Specification 的影响，不在于你们要重做项目，而在于：

`你们现在必须把现有成果统一解释成：这是一个按照老师给定 requirement specification 实现并验证的 AutoTestDesign AI App。`

只要这个口径统一了，影响就是可控的；如果每个人继续按自己的理解写，答辩时一定会出现冲突。
