# 作业 2 要求逐项核对审计

日期：`2026-06-01`

说明：这份审计记录的是**整改前状态**。如果仓库后续已经新增目标应用定义并重写 `02 / 03 / 04` 三份文档，请以最新文档为准，不要把这份审计当作整改后的最终结论。

## 0. 审计结论先说

先说最重要的结论：

1. **你们的工具本体大体上做出来了，且核心 FR 基本都已实现。**
2. **你们当前最大的风险不是“代码没做完”，而是“交付物对象理解偏了”。**
3. **最严重的问题在三份文档的对象：风险分析报告和测试计划现在主要在写 `ARG-Test / AutoTestDesign AI App` 本身，而老师要求这两份文档针对的是“你们选择的独立目标应用”。**
4. **详细测试设计与执行文档相对更贴要求，因为它明确把 `coupon_discount_engine` 当作被测目标模块来写了，但它现在仍然更像“独立可执行模块”，还不像一个完整独立应用。**
5. **提交层面还有两个明显缺口：仓库里没有实际 demo 视频文件，也没有最终 PPT 的 PDF 文件。**

一句话概括就是：

> 你们的“工具实现”整体是成立的，但你们的“课程交付物叙事框架”目前仍然把“工具本身”和“被工具测试的目标应用”混在了一起，这和老师最后的澄清要求有明显冲突。

---

## 1. 本次审计看的是什么

本次核对主要基于以下文件：

- 作业原文：`final_docs/course_brief/assignment2_final_project.md`
- 工具实现：`src/`、`prompts/`、`demo_web/`、`tests/`
- 最终三份文档：
  - `final_docs/risk_analysis_report/02_risk_analysis_report_cn.md`
  - `final_docs/test_plan/03_test_plan_cn.md`
  - `final_docs/detailed_test_design_execution/04_detailed_test_design_execution_cn.md`
- 目标模块与执行证据：
  - `reference_impl/README.md`
  - `reference_impl/coupon_discount_engine.py`
  - `tests/test_coupon_discount_engine_blackbox.py`
  - `tests/test_coupon_discount_engine_whitebox.py`
- 提交物线索：
  - `README.md`
  - `final_docs/05_evidence_and_submission_checklist_cn.md`
  - `submission_artifacts/`
  - `07_PPT_Assets_For_Luowu/`

---

## 2. 最严重的问题

### 2.1 风险分析报告写错了对象

老师要求：

- 风险分析报告要针对 **application under test / target application**
  - 见 `final_docs/course_brief/assignment2_final_project.md:64-67`
- 后面的重要澄清又明确说：
  - 风险分析报告、测试计划、详细测试设计与执行文档都应当指向 **目标应用，而不是工具本身**

你们当前风险报告的写法：

- `final_docs/risk_analysis_report/02_risk_analysis_report_cn.md:5-18`
  - 明确写成：这是围绕最终 `ARG-Test` 提交物、`FR/NFR compliance`、答辩解释风险的报告
- `final_docs/risk_analysis_report/02_risk_analysis_report_cn.md:13-17`
  - 作用域明确覆盖：
    - `AutoTestDesign AI App` 本身
    - `final_docs/`
    - `demo_web/`
    - 展示/答辩解释风险

这意味着：

- **你们现在这份风险分析报告，本质上是在分析“工具交付风险”和“课程答辩解释风险”**
- **不是在分析“独立目标应用”的业务/功能/质量风险”**

这和老师要求**不一致**。

结论：

- **风险分析报告：当前为“对象理解错误”，不是简单补一页就能修好。**

---

### 2.2 测试计划也写错了对象

老师要求：

- 测试计划要覆盖：
  - 项目范围
  - 测试项
  - 系统架构
  - 主要组件
  - 高层测试套件设计
  - schedule/checklist
  - 组织结构
  - 测试框架与理由
  - 成本估算
  - 见 `final_docs/course_brief/assignment2_final_project.md:68-123`
- 但这些内容指向的是 **目标应用**

你们当前测试计划开头就明确写了：

- `final_docs/test_plan/03_test_plan_cn.md:7`
  - `the system under test in this test plan is explicitly the AutoTestDesign AI App`
- `final_docs/test_plan/03_test_plan_cn.md:19`
  - `coupon_discount_engine` 只是 detailed execution 的 executable anchor

这说明你们现在测试计划的对象是：

- **工具本体 `ARG-Test / AutoTestDesign AI App`**
- 不是老师要求的 **独立目标应用**

要公平地说，当前测试计划在“章节完整性”上其实做得不错：

- schedule/checklist：`03_test_plan_cn.md:133-145`
- 组织结构：`03_test_plan_cn.md:147-174`
- framework rationale：`03_test_plan_cn.md:176-191`
- cost estimation：`03_test_plan_cn.md:192-217`

也就是说：

- **测试计划的结构是齐的**
- **但计划的测试对象错了**

结论：

- **测试计划：结构上较完整，但对象理解错误，属于高风险不合规项。**

---

### 2.3 你们内部统一口径本身就在强化这个错误

这不是单篇文档偶然写偏了，而是内部交接口径就这么定的。

证据：

- `report_assets/final_role_handoff_checklist_cn.md:24-27`
  - 统一口径是：
  - `Our final project is implemented and validated against the provided Requirement Specification of the AutoTestDesign AI App.`
- `report_assets/final_role_handoff_checklist_cn.md:38-40`
  - 项目被描述成 requirement-driven `AutoTestDesign AI App`
- `report_assets/final_role_handoff_checklist_cn.md:136-149`
  - 风险报告被要求围绕 `FR/NFR compliance risk`、UI gap、performance claim、traceability、demo interpretation 去写

这说明：

- **你们团队当前的“最终交付叙事”是以工具本体为中心构建的**
- **而老师要求是“开发工具，再拿这个工具去测试一个独立目标应用”**

所以后续整改不能只改 PPT 文案，必须改：

- 风险报告对象
- 测试计划对象
- 对“被测应用”的正式定义
- 所有内部口径文件

---

## 3. 核心概念到底有没有理解错

### 3.1 工具是什么

你们开发的工具是：

- `ARG-Test`
- 一个 requirement-driven 的 AI AutoTestDesign 工具

它的核心实现证据很明确：

- CLI 支持多种输入：`src/main.py:24-57`
- 支持 direct text / CSV / file / state-model：`src/main.py:28-57`
- 结构化五段 trace：`prompts/system_prompt.txt:2-10`、`src/parser.py:9-24`
- 风险分析：`src/risk.py:74-157`
- 状态模型：`src/state_model.py:152-326`
- 导出：`src/exporter.py:14-93`
- rerank / repair：`src/reranker.py:7-20`、`src/repair.py:221-251`

所以：

- **工具本体没有理解错**
- **工具本身做得也基本对路**

### 3.2 被测应用是什么

老师要求很明确：

- 你们必须选择一个**独立目标应用**
- 然后用你们的工具去测试它

你们仓库里现在最接近这个角色的是：

- `coupon_discount_engine`

证据：

- `final_docs/detailed_test_design_execution/04_detailed_test_design_execution_cn.md:5`
  - 明确说它是 target e-commerce promotion application 的 selected major feature
- `reference_impl/README.md:3-13`
  - 明确说 `reference_impl/` 存的是 small executable modules，用于支持 detailed execution
- `reference_impl/coupon_discount_engine.py:56-118`
  - 确实有独立可执行逻辑
- `tests/test_coupon_discount_engine_blackbox.py:4-80`
- `tests/test_coupon_discount_engine_whitebox.py:6-38`

但严格说，它现在更像：

- **一个独立可执行模块**
- 而不是一个完整独立目标应用

结论：

- **宽松解释下：你们“有”目标对象，名称是 `coupon_discount_engine`。**
- **严格按老师澄清：你们还缺一个更明确、更完整的“独立目标应用定义”。**

---

## 4. 按功能要求 FR 逐项核对

### FR 1.0 输入/解析

老师要求：

- 从 CSV、纯文本、直接用户输入导入需求

实现证据：

- `src/main.py:28-57`
  - `run`
  - `run-text`
  - `batch-csv`
  - `state-model`
- `src/input_loader.py:17-49`
  - CSV 读取实现
- `demo_web/static/index.html:19-22`
  - Direct Input / CSV Batch / State Model / Formal Evidence

结论：

- **FR 1.0：已完成**

### FR 1.1 需求结构化

老师要求：

- 解析原始文本，识别输入字段、范围、条件、预期动作等

实现证据：

- `prompts/system_prompt.txt:2-10`
  - 强制五段结构输出
- `src/parser.py:12-24`
  - 切出 `Analysis / Pattern / Steps / Verification / FinalAnswer`
- `src/parser.py:36-68`
  - 解析最终表格为结构化测试用例
- `src/schemas.py:180-256`
  - `ParsedTrace`、`TestCase`

结论：

- **FR 1.1：已完成**

### FR 2.0 风险分析与优先级排序

老师要求：

- 给每条需求分配风险评分和优先级

实现证据：

- `src/risk.py:74-157`
  - requirement-level risk assessment
- `src/risk.py:171-208`
  - case priority promotion
- `src/pipeline.py:150-155`
  - annotate 阶段注入 risk

结论：

- **FR 2.0：已完成**

### FR 3.0 黑盒测试设计

老师要求：

- 至少三种 ISO 29119-4 核心黑盒技术

实现证据：

- `prompts/system_prompt.txt:6-10`
  - 明确要求 EP / BVA / Decision Table / State Transition
- `src/checker/composite.py:11-18`
  - 运行 schema / EP / BVA / decision / state checks
- `src/checker/ep_checker.py:11-31`
- `src/checker/bva_checker.py:7-24`
- `src/checker/decision_checker.py:10-25`
- `src/checker/state_checker.py:10-29`

结论：

- **FR 3.0：已完成，且实现强度较高**

### FR 4.0 白盒测试建模

老师要求：

- 对系统行为建模，例如状态转换图，并基于覆盖准则生成最优测试序列

实现证据：

- `src/state_model.py:152-326`
  - 抽取 legal transitions
- `src/state_model.py:329-420`
  - 抽取 illegal transitions
- `src/schemas.py:79-177`
  - `StateCoveragePlan` / `StateModel`
- `demo_web/static/index.html:161-227`
  - State-Model tab

但这里有边界：

- 你们的 **FR 4.0 主实现** 是“从 requirement 文本抽状态模型和覆盖计划”
- 它不是“对代码内部控制流做自动白盒建模”
- 详细执行文档里的白盒测试主要是对 `coupon_discount_engine` 做 `pytest + coverage`
  - `04_detailed_test_design_execution_cn.md:133-170`

结论：

- **FR 4.0：部分到大体完成**
- **可以作为加分项成立**
- **但不能夸成“通用自动白盒建模系统”**

### FR 5.0 测试预言生成

老师要求：

- 合成 expected result

实现证据：

- `prompts/system_prompt.txt:9-10`
  - 每个测试必须有 expected output
- `src/parser.py:56-66`
  - `expected_output` 是正式字段
- `src/schemas.py:13-18`
  - `TestCase.expected_output`
- `04_detailed_test_design_execution_cn.md:67-100`
  - 详细文档中 expected result 也落到了可执行断言

结论：

- **FR 5.0：已完成**

### FR 6.0 输出与导出

老师要求：

- 结构化标准格式，例如 JSON / Excel/CSV

实现证据：

- `src/exporter.py:14-93`
  - raw generations
  - parsed traces
  - checker logs
  - final test JSON / CSV / Markdown
  - summary JSON

结论：

- **FR 6.0：已完成**

### FR 7.0 测试套件优化

老师要求：

- 基于风险或覆盖效率进行优先级排序或最小化

实现证据：

- `src/pipeline.py:207-235`
  - 多 candidate 评估与 repair
- `src/reranker.py:7-20`
  - aggregate score + best selection
- `src/repair.py:221-251`
  - 本地补齐 coverage obligations
- `src/risk.py:204-208`
  - case priority promotion

边界：

- 你们确实有 **rerank / repair / prioritization**
- 但严格说这更像“质量导向的套件选择与修补”
- 不是一个形式化的 test suite minimization 算法

结论：

- **FR 7.0：已部分到大体完成**
- **可视为加分项成立，但表述宜克制**

---

## 5. 交互式审查能力是否满足

老师要求非常关键的一句是：

- 工具应允许设计者在覆盖项识别、策略、测试用例等过程中进行交互式审查、修订和更改

你们当前实现有：

- Web demo：
  - `demo_web/static/index.html:19-22`
  - Direct Input / CSV Batch / State Model / Formal Evidence
- 可以修改 requirement text 再重新运行：
  - `demo_web/static/index.html:75-95`
  - `demo_web/static/app.js:451-471`
- 可以查看生成结果、risk、cases、artifacts：
  - `demo_web/static/app.js:232-267`

但当前没有看到这些能力：

- 直接编辑“coverage items”
- 直接编辑“selected strategy / technique plan”
- 直接编辑已生成 test cases 并保存为新的正式版本
- 明确的人工 review -> revise -> commit 交互链路

也就是说，现在更像：

- **interactive input + rerun + inspect**

而不是：

- **interactive review and modification of coverage items, strategy, and test cases**

结论：

- **交互式审查能力：部分满足，不算完全符合老师这条强调要求**

这是一个重要但次于“文档对象写错”的问题。

---

## 6. 按非功能要求 NFR 核对

### Performance

证据：

- `03_test_plan_cn.md:44-45`
  - 本地/mock 路径 100 requirements `1.1331 s`
  - 单 requirement 最大 `0.0187 s`
- `02_risk_analysis_report_cn.md:75-76`
  - 也承认 live provider latency 仍是外部变量

结论：

- **NFR 性能：本地/mock 路径有证据，live 路径不能强宣称完全满足**

### Usability / UX/UI

证据：

- `demo_web/static/index.html:10-29`
- `tests/test_demo_web_api.py:15-35`

结论：

- **NFR 可用性：有课程项目级 demo，可演示，可回放**
- **但不是成熟产品前端**

### Security

证据：

- `README.md:189-205`
  - `.env.example` / `.env`
- `02_risk_analysis_report_cn.md:77-78`
  - secret-handling 和 artifact scan 口径

结论：

- **NFR 安全：有基本隔离与文档说明，课程项目层面基本成立**

### Maintainability and Technology

证据：

- `README.md:34-54`
  - 目录分层
- `src/` 结构化模块分工
- `tests/test_demo_web_api.py`
- `03_test_plan_cn.md:49-51`

结论：

- **NFR 可维护性/技术：成立**

---

## 7. 按交付物逐项核对

### 7.1 交付物 1：AI-driven AutoTestDesign Tool

老师要求：

- source code
- prompts
- README / setup instructions
- video demonstration

当前情况：

- source code：有
  - `src/`
  - `demo_web/`
  - `tests/`
- prompts：有
  - `prompts/system_prompt.txt`
  - `prompts/generation_prompt.txt`
- README：有
  - `README.md`
- video demonstration：**仓库中未找到实际视频文件**
  - 审计时未搜到 `.mp4/.mov/.avi/.mkv/.webm`
  - 只有 demo 脚本和录制说明，如 `report_assets/final_demo_package/`

结论：

- **工具交付物：大体完成，但“实际 demo 视频文件”目前缺失证据**

### 7.2 交付物 2：Risk Analysis Report

当前情况：

- 文件存在：`final_docs/risk_analysis_report/02_risk_analysis_report_cn.md`
- PDF 存在：`final_docs/risk_analysis_report/02_risk_analysis_report_cn.pdf`
- 但对象错误：
  - `02_risk_analysis_report_cn.md:5-18`

结论：

- **文件存在，但内容对象理解错误**

### 7.3 交付物 3：Test Plan

当前情况：

- 文件存在：`final_docs/test_plan/03_test_plan_cn.md`
- PDF 存在：`final_docs/test_plan/03_test_plan_cn.pdf`
- 各章节齐全：
  - scope：`03_test_plan_cn.md:3-21`
  - test items：`03_test_plan_cn.md:23-67`
  - suite design：`03_test_plan_cn.md:68-122`
  - levels/goals：`03_test_plan_cn.md:124-131`
  - schedule/checklist：`03_test_plan_cn.md:133-145`
  - org chart：`03_test_plan_cn.md:147-174`
  - framework rationale：`03_test_plan_cn.md:176-191`
  - cost estimation：`03_test_plan_cn.md:192-217`
- 但对象错误：
  - `03_test_plan_cn.md:7`

结论：

- **结构上完成，内容对象理解错误**

### 7.4 交付物 4：Detailed Test Design and Execution Document

当前情况：

- 文件存在：`final_docs/detailed_test_design_execution/04_detailed_test_design_execution_cn.md`
- PDF 存在：`final_docs/detailed_test_design_execution/04_detailed_test_design_execution_cn.pdf`
- 这份文档是三份里最贴要求的一份：
  - 选定 major feature/module：`04_detailed_test_design_execution_cn.md:3-15`
  - 黑盒设计：`04_detailed_test_design_execution_cn.md:65-132`
  - 白盒设计：`04_detailed_test_design_execution_cn.md:133-170`
  - 执行结果：`04_detailed_test_design_execution_cn.md:172-209`
  - mutation usefulness：`04_detailed_test_design_execution_cn.md:239-261`

边界：

- 它选的是 `coupon_discount_engine`
- 这是“目标电商应用的一个模块”
- 不是完整独立应用

结论：

- **这份文档基本合格**
- **但依赖于你们对“目标应用”的重新定义与补充说明**

---

## 8. 提交格式层面的核对

老师要求：

- report 和 PPT 交 PDF
- test scripts 交压缩包
- PPT 第一页要有 team ID、姓名、学号
- project artifact cover page 也要有 team ID、姓名、学号
  - 见 `final_docs/course_brief/assignment2_final_project.md:150-174`

当前仓库可见情况：

- 三份文档 PDF：
  - 有
- test scripts zip：
  - 有 `submission_artifacts/arg_test_final_test_scripts.zip`
- 最终 PPT：
  - 目前仓库里有 `07_PPT_Assets_For_Luowu/final_ppt.pptx`
  - **未找到 `final_ppt.pdf`**
- 实际 demo video：
  - **未找到视频文件**

关于“封面页/第一页是否包含 team ID、姓名、学号”：

- 当前这次审计以源文档和仓库文件为主
- **未对 PDF/PPT 二进制第一页进行最终格式核验**
- 这项需要在最终导出物上再做一次人工检查

结论：

- **提交格式层面目前仍有缺口**
  - 缺 PPT PDF
  - 缺视频文件证据

---

## 9. 最终总评

### 9.1 哪些是“已经完成”的

- 工具核心能力基本完成
- `FR 1.0 / 1.1 / 2.0 / 3.0 / 5.0 / 6.0` 可以认为已完成
- `FR 4.0 / 7.0` 可认为部分到大体完成
- NFR 有一套课程项目级证据
- detailed execution 证据很强

### 9.2 哪些是“理解错要求”的

- 风险分析报告对象
- 测试计划对象
- 团队内部统一叙事框架

### 9.3 哪些是“还没交齐”的

- 实际 demo 视频文件
- 最终 PPT 的 PDF
- 严格意义上“独立目标应用”的完整定义与文档化描述

---

## 10. 后续必须遵守的改进方向

后续如果要严格贴近老师要求，建议按这个顺序改：

1. **先冻结“目标应用”定义。**
   - 不要再模糊写成 `target module/application scenario`
   - 必须明确：
   - 你们的工具是 `ARG-Test`
   - 你们的目标应用是什么
   - `coupon_discount_engine` 在其中是什么角色

2. **重写风险分析报告对象。**
   - 从“工具交付/答辩风险”改成“目标应用测试风险”
   - 工具本体风险可保留少量作为边界说明，但不能再当主干

3. **重写测试计划对象。**
   - scope、architecture、test items、cost 都要围绕目标应用
   - `ARG-Test` 只能出现在“采用的测试工具/方法”位置

4. **保留详细执行文档主体，但补足目标应用背景。**
   - 这份文档可以继续以 `coupon_discount_engine` 为主模块
   - 但要明确它属于哪个目标应用、该应用还有哪些主要组件

5. **把交互式审查能力写实。**
   - 现在可以说有 direct input / rerun / inspect
   - 不能夸成完整的人机协同 design review workflow
   - 如果还来得及，可以补一个最小可行的人审修改入口

6. **补齐最终提交物。**
   - demo video
   - PPT PDF
   - 最终第一页/封面页信息核验

---

## 11. 一句话定性

如果现在就交：

- **代码和实验层面：整体是能站住的**
- **课程要求合规层面：还不能说完全贴要求**

最核心的不是“要不要重写系统”，而是：

> **要把“我们开发了什么工具”与“我们用这个工具测试了什么目标应用”这两件事彻底拆开，并让三份正式文档全部服从这个拆分。**
