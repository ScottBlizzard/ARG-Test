# ARG-Test Final Upgrade Report

版本：`v1`

日期：`2026-05-07`

适用仓库：`D:\软件测试\Final\ARG-Test`

对应课程作业：`Assignment 2: Final Project`

截止时间：`2026-05-29 17:00`

---

## 1. 执行摘要

本报告的目标不是说明“如何把作业做完”，而是说明“如何把 `ARG-Test` 从已有的中期项目基础升级为一份高质量、可答辩、可复现、可展示的 final 项目”。

当前仓库已经具备很强的基础：

- requirement-driven AI black-box testing 主流程已经存在
- `Analysis -> Pattern -> Steps -> Verification -> FinalAnswer` 五段式输出已经成型
- parser / checker / rerank / repair / exporter / evaluation 已存在
- baselines、ablation、generalization、图表素材、submission package 都已有中期基础
- final 文档骨架、详细执行模块基线、white-box 测试脚手架也已经补入仓库

因此，final 阶段不应该重写，也不应该分散精力搞很多“看起来高级”的附加功能。最佳策略是：

1. 以现有仓库为唯一主仓库继续推进。
2. 把已有成果从“脚手架 + 中期结果”提升为“正式证据 + 完整交付物”。
3. 优先补最影响 final 质量的升级项，而不是再横向扩很多新需求。

本报告给出的最终判断是：

- **代码层面要继续提升，但不需要重构架构。**
- **实验层面应采用 `best-of-3 candidates + 3 independent reruns`，不要随意声称是 3 seed。**
- **数据量目前足够，不应继续扩数据优先级；应优先统一正式结果口径。**
- **详细测试设计与执行必须以一个主模块形成黑盒 + 白盒闭环。**
- **风险分析、测试计划、详细执行文档、结果源管理必须全部成型。**

---

## 2. 当前基线状态

### 2.1 仓库结构状态

当前主仓库已经统一到：

- `D:\软件测试\Final\ARG-Test`

final 工作资料区已经建立：

- `final_docs/`

中期冻结材料已经隔离：

- `frozen_middle/`

这意味着现在已经具备继续在同一仓库上完成 final 的结构前提。

### 2.2 已有系统能力

当前 `ARG-Test` 已有的系统能力包括：

- requirement ingestion
- structured testing trace generation
- parser for five-section output
- EP / BVA / Decision Table / State Transition checker
- reranking and local repair
- final artifact export to JSON / CSV / Markdown
- baseline comparison
- ablation and generalization scripts
- summary table export

关键代码入口包括：

- `src/main.py`
- `src/pipeline.py`
- `src/llm_client.py`
- `src/parser.py`
- `src/checker/`
- `src/reranker.py`
- `src/repair.py`
- `src/exporter.py`
- `src/evaluation/metrics.py`

### 2.3 现有数据规模

根据 `data/requirements/manifest.json` 当前统计结果：

- `dev = 50`
- `test = 16`

`test` 集类别分布：

- `business_rules = 7`
- `input_validation = 4`
- `workflow_state = 5`

这个规模对于课程 final 是足够的，而且三类 requirement 都有覆盖。

### 2.4 当前正式结果状态

当前一个最重要的问题是：

- `manifest` 中 `test = 16`
- 但 `outputs/reports/test/run_main_summary.json` 当前只有 `10` 条 requirement 的正式结果

这意味着：

- 现有数据资产数量与现有正式结果数量不一致
- 如果直接写 final 报告，极易在答辩中被追问
- 当前最优先的问题不是“加更多数据”，而是“统一评估口径”

### 2.5 当前详细执行模块状态

已经为 `coupon_discount_engine` 补了可执行的 detailed module 基线：

- `reference_impl/coupon_discount_engine.py`
- `tests/test_coupon_discount_engine_blackbox.py`
- `tests/test_coupon_discount_engine_whitebox.py`

当前执行证据：

- `15 passed`
- `reference_impl/coupon_discount_engine.py` statement coverage = `100%`

证据文件位于：

- `final_docs/execution_evidence/coupon_discount_engine_execution_summary.md`
- `final_docs/execution_evidence/coupon_discount_engine_coverage.xml`

这为 final 的 Detailed Test Design and Execution Document 提供了一个已经可运行的起点。

---

## 3. 最佳版本 Final 的目标定义

final 项目不应仅仅达到“满足老师要求”，而应达到如下四个层级的高标准。

### 3.1 工具层目标

`ARG-Test` 应该表现为一个：

- 能从自然语言需求生成可审计测试设计
- 能给出结构化 trace
- 能用 technique-specific checker 自动发现遗漏
- 能输出可写入报告和测试管理材料的标准化结果
- 至少在一个重点模块上形成可执行测试闭环

### 3.2 实验层目标

实验不应只展示单次跑出的数字，而应至少体现：

- baseline 对比
- ablation
- generalization
- stability / rerun sanity
- 详细案例分析

### 3.3 文档层目标

文档不应只像项目 proposal 或课程模板，而应具备：

- 风险分析报告
- 正式测试计划
- 详细测试设计与执行文档
- 完整 final report
- 能和仓库中的证据一一对应

### 3.4 展示层目标

演示和答辩应做到：

- 15 分钟能讲清方法、结果、局限、价值
- 所有主结论都有仓库证据路径
- 面对“为什么这么设计”和“为什么数字可信”时能直接回答

---

## 4. 与作业要求的差距分析

### 4.1 AI-driven AutoTestDesign Tool

当前已具备：

- 核心工具流程
- prompts
- setup 说明
- artifacts / outputs / experiments

当前差距：

- 缺 final 版风险优先级输出能力
- 缺更正式的运行元数据记录
- 缺 final demo 视频与演示路径设计

### 4.2 Risk Analysis Report

当前已具备：

- failure analysis 素材
- 限制与风险讨论素材

当前差距：

- 缺独立成型的 risk report
- 缺统一的风险评分与优先级表达

### 4.3 Test Plan

当前已具备：

- 大量系统模块和实验脚本
- 角色分工与中期 runbook 思路

当前差距：

- 缺 final 版正式测试计划
- 缺清晰的 test level、framework rationale、cost estimation、schedule

### 4.4 Detailed Test Design and Execution Document

当前已具备：

- 结构化测试输出
- gold specs
- 多个合适的候选 requirement
- `coupon_discount_engine` executable baseline

当前差距：

- detailed 文档尚未写成正式成品
- 仍需把黑盒设计和 white-box 证据明确串起来
- 仍可进一步补 defect usefulness 证明

### 4.5 Presentation / Demo

当前已具备：

- proposal / outline / figures / scripts 基础

当前差距：

- final 版 PPT 尚未成稿
- demo 脚本与视频尚未完成

---

## 5. 核心判断与决策

### 5.1 是否要重构代码

结论：

- **不要重构架构。**
- **要做针对性增强。**

理由：

1. 现有架构已经完整，重构收益低、风险高。
2. final 的主要短板不是“没有系统”，而是“缺成型证据与正式口径”。
3. 更高价值的投入应放在风险评分、结果去模板化、正式 rerun、详细执行与文档化。

### 5.2 是否需要更多数据

结论：

- **当前数据量够。**
- **不建议把扩数据作为优先项。**

理由：

1. `dev=50`, `test=16` 对课程 final 已经足够。
2. 真正的问题在于 test 结果未覆盖完整 16 条。
3. 继续扩数据只会增加跑数和写报告负担，不直接提升 final 质量。

### 5.3 最佳实验配置是什么

结论：

- **单次正式实验：best-of-3 candidates**
- **稳定性分析：3 independent reruns**

注意：

- 当前代码并没有显式 seed 控制
- 因此 final 报告中不要轻率写成 “3 seeds”
- 更准确表述应为：
  - `best-of-3 candidate generation`
  - `3 independent reruns for stability sanity`

### 5.4 详细执行主模块选哪个

结论：

- **主模块固定为 `coupon_discount_engine`**

理由：

1. 同时适合 EP、BVA、Decision Table
2. 业务规则清晰
3. 已经补上 reference implementation 和 pytest 基线
4. 适合再扩成 white-box 和 defect usefulness 展示

辅助案例建议：

- `order_approval_state_machine`
- `payment_3ds_authentication_flow`

这些更适合作为 workflow/state 类能力和局限的 case study。

---

## 6. 程序层升级方案

本节只保留真正能提升 final 质量的程序级升级，不列低价值装饰项。

### U1. 引入 Risk Score 与 Test Priority 输出

#### 目标

补齐 final 要求中的：

- requirement risk analysis
- prioritization

#### 当前状态

虽然 test case 表中已有 `Priority` 字段，但当前更多是静态填值，不是系统化 risk analysis 结果。

#### 升级内容

1. 在 requirement analysis 阶段提取风险特征。
2. 基于规则或轻量评分模型生成：
   - `risk_score`
   - `risk_level`
   - `test_priority`
3. 将该结果导出到：
   - parsed trace
   - final test suite summary
   - reports

#### 推荐风险因子

- rule complexity
- number of conditions
- presence of workflow/state transitions
- financial/business criticality keywords
- negative/exception behavior count
- ambiguity markers

#### 代码建议修改点

- `src/schemas.py`
- `src/parser.py`
- `src/pipeline.py`
- `src/exporter.py`
- `src/evaluation/metrics.py`

#### 交付价值

- 直接补齐 final 要求
- 让 test suite optimization / prioritization 更像真正产品功能
- 让报告中的 risk analysis 与工具功能统一

### U2. 统一记录运行元数据

#### 目标

让 final 结果更可复现、更可答辩。

#### 升级内容

在正式结果输出时记录：

- provider
- model
- candidates
- rerun tag
- timestamp
- output root
- split

#### 建议位置

- `outputs/reports/<split>/run_manifest.json`
- 或在每个 summary 中补 metadata

#### 价值

- 防止后续文档写作时混淆不同 run
- 方便对比正式结果和 rerun 结果

### U3. 去模板化关键展示结果

#### 目标

消除 final 展示样例中的占位式文本。

#### 当前问题

现有一些输出还带有：

- `representative valid input`
- `rule trigger combination`
- `rule-specific outcome`

这类内容对演示和答辩非常不利。

#### 升级方式

1. 为最终展示的 2 到 3 个 requirement 做 targeted rerun。
2. 强化 prompt，要求：
   - 输入值必须具体
   - expected output 必须具体
   - covered item 必须与 gold spec 对齐
3. 若仍不足，则对展示样例允许有限人工校订，并明确标注为 final curated case study。

#### 优先 requirement

- `coupon_discount_engine`
- `bank_transfer_rule_checker`
- `order_approval_state_machine` 或 `payment_3ds_authentication_flow`

### U4. 强化 workflow/state 类结果质量

#### 当前问题

workflow/state 类需求的 `overall_coverage` 与表现明显弱于一些 business rules 类 requirement。

#### 目标

至少让 final 报告中 workflow 类案例既能展示能力，也能展示真实局限，而不是一味回避。

#### 升级方式

1. 对 workflow 类 prompt 加强结构约束：
   - state list
   - event list
   - legal transition
   - illegal transition
   - expected next state
2. 针对 state trace 做更具体的 repair 条件。
3. 在 checker 层降低不相关契约误报，避免 business rule requirement 被 state checker 干扰解释。

#### 建议修改点

- `prompts/`
- `src/repair.py`
- `src/checker/state_checker.py`
- `src/evaluation/metrics.py`

### U5. 主模块 executable evidence 继续增强

#### 当前状态

`coupon_discount_engine` 已有：

- reference implementation
- pytest black-box tests
- pytest white-box tests
- 100% statement coverage

#### 下一步增强

1. 增加 branch coverage 说明
2. 增加 decision table 与 test mapping
3. 如时间允许，增加 defect-seeded usefulness demonstration

#### 价值

这会让 Detailed Test Design and Execution 部分从“有例子”升级为“有完整闭环”。

---

## 7. 实验层升级方案

### E1. 将正式 test 集统一到 16 条

#### 当前问题

- `manifest test = 16`
- `run_main_summary = 10`

#### 目标

把 final 报告中的正式 test 评估集统一为完整 16 条。

#### 原因

1. 统一口径
2. 避免答辩被问
3. 让 generalization 和 average 指标更可信

#### 建议动作

1. 先校验 16 条 test requirement 和 gold spec 是否齐全。
2. 用同一配置正式跑完 16 条。
3. 重新生成：
   - `run_main_summary.json`
   - `main_summary_table.*`
   - `baseline_summary.json`
   - `ablation_summary.json`
   - `generalization_by_category.json`

### E2. 保留 best-of-3 candidates

#### 判断

当前仓库已经默认支持：

- `--candidates 3`

这应该保留，不建议改成 1。

#### 理由

1. 它是当前方法优于 plain LLM 的重要组成部分。
2. `rerank + repair` 的意义要建立在有多候选基础上。
3. final 图表和方法叙事也已经围绕这一点展开。

### E3. 增加 3 independent reruns

#### 目标

对 final 结果补稳定性支持。

#### 注意

这里不要写成 3 seeds，除非后续真正加 seed 参数控制。

#### 建议设计

方案 A，强版本：

- 全量 `test=16` 跑 3 次独立正式 rerun
- 统计平均值、方差、绝对差

方案 B，课程性价比最高版本：

- 正式主结果跑 1 次
- 代表性子集用 `run_stability_sanity.py` 跑 3 次独立 rerun
- 在报告中作为 stability sanity check 呈现

#### 推荐结论

若 API 成本可承受，选方案 A。

若成本有限，选方案 B。

### E4. Baseline 与 Ablation 重新对齐

#### 目标

避免不同结果文件基于不同 test 子集或不同配置。

#### 建议

确保 baseline / ablation / main comparison 都基于：

- 相同 test set
- 相同正式输出口径
- 相同结果源目录规则

### E5. 报告中明确分离三类指标

final 不应只呈现一个总分。

建议显式分开：

#### Outcome metrics

- overall coverage
- valid partition coverage
- invalid partition coverage
- boundary coverage
- decision rule coverage
- state / illegal transition coverage
- duplicate count

#### Process metrics

- checker score
- schema validity
- repair triggered or not
- rerank selection quality

#### Stability metrics

- rerun score delta
- rerun coverage delta
- stable case count

这样可以直接回应“checker score 高但 coverage 低”这类问题。

---

## 8. 数据层升级方案

### 8.1 是否继续扩 requirement

结论：

- **不建议继续扩新 requirement 作为优先项。**

### 8.2 数据层当前最值得做的事情

1. 核查 16 条 test requirement 的 gold spec 完整性。
2. 核查 manifest、requirements、gold specs 的一致性。
3. 确保 final 报告中的 category 统计与仓库一致。

### 8.3 可以做但非优先

如果后续时间很充裕，可以考虑：

- 给 workflow/state 类补 1 条更易展示的 requirement

但这不应挤占正式跑数和最终成稿时间。

---

## 9. 文档与交付物升级方案

### D1. Risk Analysis Report 成型

需要从草稿升级为正式文档，内容应至少包含：

- 风险评分模型
- ranked risk table
- 高风险项缓解动作
- 方法技术风险与交付风险区分

### D2. Test Plan 成型

需要正式写出：

- scope
- test items
- architecture
- suite design
- test levels
- framework rationale
- schedule
- cost estimation

### D3. Detailed Test Design and Execution 成型

以 `coupon_discount_engine` 为中心，正式文档需要包含：

- requirement summary
- EP 设计
- BVA 设计
- decision table
- white-box branch discussion
- pytest result
- coverage result
- result analysis

### D4. Final Report 成型

final report 应以现有 `report_outline` 为基础，但必须升级为：

- 讲清楚方法贡献
- 数字与图表全部来自正式结果路径
- limitations 和 threats to validity 写得真实而具体

### D5. PPT 与 Demo 成型

建议结构：

1. problem
2. why plain LLM is not enough
3. ARG-Test method
4. architecture
5. checker logic
6. main experiment
7. baseline / ablation
8. detailed module execution
9. limitations
10. conclusion

demo 要控制在 3 到 5 分钟内，展示：

- input requirement
- structured trace
- checker diagnostics
- final tests
- one summary table / figure
- executable module evidence

---

## 10. 建议的结果源管理规范

### 10.1 正式结果来源

仅允许引用：

- `outputs/reports/dev/run_main_summary.json`
- `outputs/reports/test/run_main_summary.json`
- `outputs/reports/test/baseline_summary.json`
- `outputs/reports/test/ablation_summary.json`
- `outputs/reports/test/generalization_by_category.json`

以及案例分析原始来源：

- `artifacts/raw_generations/<split>/`
- `artifacts/parsed_traces/<split>/`
- `artifacts/checker_logs/<split>/`
- `outputs/final_tests/<split>/`

### 10.2 不允许直接引用

- 临时终端输出
- mock dry-run 结果
- 未固化的手工数字
- 不可复现的截图数字

### 10.3 应新增的正式元数据

建议新增：

- `run_manifest.json`
- `rerun_manifest.json`

至少记录：

- model
- provider
- candidates
- run type
- split
- execution timestamp

---

## 11. 推荐的升级优先级

### P0：必须完成

1. 统一正式 test 集到 16 条
2. 补 risk scoring / prioritization 输出
3. 去模板化最终展示样例
4. 完成 final 文档四件套
5. 固化详细执行模块闭环

### P1：强烈建议

1. 做 3 次 independent rerun 或 stability sanity check
2. 优化 workflow/state 类 prompt / checker / repair
3. 补正式运行元数据

### P2：若时间允许

1. 加 defect-seeded usefulness demonstration
2. 更细的 branch coverage 说明
3. 更完整的 visual assets 导出

### 不建议优先投入

1. 继续横向扩大量 requirement
2. 重做仓库结构
3. 做复杂 UI 包装
4. 加很多和 final 结论无关的附加功能

---

## 12. 建议的执行顺序

### Phase 1：口径统一

目标：

- 统一 test 集规模和正式结果规模
- 确认最终实验配置

动作：

1. 检查 16 条 test 的 requirements / gold specs
2. 确认正式 run 配置
3. 规划 rerun 策略

### Phase 2：程序补强

目标：

- 把 final 缺口补到系统中

动作：

1. 加 risk score / priority
2. 增加 run metadata
3. 强化 workflow/state 处理
4. 去模板化展示案例

### Phase 3：正式跑数

目标：

- 得到 final 可写入文档的正式结果

动作：

1. main run
2. baseline run
3. ablation
4. generalization
5. rerun / stability

### Phase 4：详细执行成型

目标：

- 把 `coupon_discount_engine` 写成完整章节

动作：

1. 整理 black-box tables
2. 整理 white-box evidence
3. 补 coverage / result analysis

### Phase 5：文档与展示定稿

目标：

- 收束全部 final 交付物

动作：

1. 完成 report
2. 完成 PPT
3. 完成 demo script / video
4. 完成 submission package

---

## 13. 预期最终成果形态

如果按本报告推进，最终仓库应呈现为：

### 工具层

- 能生成结构化测试设计
- 能给出风险优先级
- 能导出标准化测试结果
- 至少一个模块可执行验证

### 实验层

- main / baseline / ablation / generalization / stability 全部齐全
- test 集规模和结果规模一致
- 所有主结论有正式结果支持

### 文档层

- risk analysis report
- test plan
- detailed test design and execution document
- final report
- PPT / demo assets

### 答辩层

- 讲得清楚
- 证据可追踪
- 局限说得真实

---

## 14. 最终退出标准

只有同时满足下面条件，才算进入真正的 final 可交状态：

1. `test = 16` 的正式结果已经统一生成并可引用。
2. risk score / priority 已经进入系统输出。
3. `coupon_discount_engine` 的 detailed execution 形成黑盒 + 白盒闭环。
4. final 报告中的所有主数字都能映射到仓库正式结果路径。
5. PPT 与报告使用的是同一版本结果。
6. demo 有固定流程，不依赖临场 improvisation。

---

## 15. 结论

`ARG-Test` 当前最大的优势不是“还有很多东西没做”，而是“已经有非常强的底座”。因此 final 最优策略不是推翻重做，而是把已经存在的系统和证据收束成一个高质量成品。

最关键的三个升级点是：

1. **把正式结果口径统一到完整 16 条 test 集。**
2. **把系统从 black-box generator 升级为带 risk prioritization 的 AutoTestDesign 工具。**
3. **把 `coupon_discount_engine` 打造成可执行、可展示、可写进详细章节的 final 主模块。**

如果这三件事做好，再加上稳定性 rerun、正式文档和展示打磨，这个 final 项目不只是“完成作业”，而是会非常像一套结构完整、逻辑清楚、答辩友好的课程项目成品。
