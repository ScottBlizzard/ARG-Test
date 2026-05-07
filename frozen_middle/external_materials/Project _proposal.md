我综合看了你上传的论文和静态分析工具列表后，结论很明确：**你们最合适的项目，不是走 static analysis，也不是走 white-box coverage，而是做一个“基于需求说明的、可审计的 AI 黑盒测试用例生成工具”**。原因很简单：你论文的核心已经不是“单纯让 LLM 出答案”，而是把推理过程变成**五段式、可解析、可验证、可重排/修复**的结构化轨迹；这和“从 requirement 生成 test cases”几乎是天然匹配的。论文前半部分明确给出了五段式 schema（Analysis / Pattern / Steps / Verification / FinalAnswer）和 checker + rerank/refine 的整体框架，后半部分又强调评估时要把 **accuracy、structure quality、token cost** 分开看，而不是混成一个分数。

相反，静态分析那条路线虽然作业允许，但你上传的工具列表本身就已经列出了一大批成熟工具，如 CodeQL、SonarQube、Semgrep、Infer、Coverity、Clang、Frama-C 等；这意味着如果你们选 static analysis，很容易做成“套现成工具+做一点 AI 包装”，反而不容易凸显你论文里的结构化 reasoning 创新。

下面我直接给你一版**最适合拿分、最贴合作业、也最能复用论文**的完整方案。你可以把它当成你们项目的正式蓝图。

---

# 一、最终推荐定版

## 项目题目

**ARG-Test: Auditable Requirement-Driven Black-Box Test Generation with Structured LLM Reasoning and Contract Verification**

中文可以写成：

**ARG-Test：一种基于结构化大语言模型推理与合同验证的可审计需求驱动黑盒测试用例生成工具**

## 一句话定义

输入自然语言需求说明，工具先生成**结构化测试设计轨迹**，再用**testing contract checker**检查其是否完整覆盖等价类、边界值、规则组合、非法场景等，最后输出**高质量测试用例集、覆盖报告和诊断信息**。

## 为什么这是最优解

第一，它和作业要求完全对齐。作业允许黑盒测试，且输入可以是 requirement，输出必须是 test cases，还要求实验分析、对比传统方法、分析 AI 局限。

第二，它和你论文的核心完全对齐。你论文最强的不是某个具体 benchmark，而是这套“**结构化推理 → checker 验证 → 诊断修复 → rerank/refine**”的方法学。

第三，它实现风险最低但展示效果最好。white-box 需要插桩、覆盖率计算、程序分析；static analysis 需要语法树/CFG/数据流或现成工具整合。黑盒 requirement-driven 路线更容易在短时间内做出一个**能跑、能展示、能做实验、能解释创新点**的作品。

---

# 二、最合适的大纲

这是你们报告和项目都应该采用的**最终大纲**。

## 1. Introduction

说明三件事：

1. 传统黑盒测试设计依赖人工阅读需求，效率低，容易漏掉边界和异常情况。
2. 直接让 LLM 生成测试用例虽然方便，但容易出现遗漏、重复、预期结果胡编、技术选择混乱的问题。
3. 你们提出 ARG-Test，用**结构化测试推理 + 合同验证 + 诊断修复**来提升测试质量与可审计性。

## 2. Problem Definition

定义输入、输出、目标。

输入：

* 自然语言需求说明
* 可选的字段约束、接口说明、业务规则

输出：

* 测试用例集
* 每条用例对应的测试技术标签
* 测试设计轨迹
* 验证/诊断结果
* 覆盖分析报告

目标：

* 提高 test case correctness
* 提高 requirement coverage
* 提高 boundary / invalid / rule coverage
* 降低 redundancy 和 hallucination

## 3. Proposed Method

这是最核心的一章。

### 3.1 整体框架

**Requirement → Prompt Builder → LLM Structured Trace → Parser → Contract Checker → Rerank/Repair → Final Test Cases**

### 3.2 Testing-ARG 五段式结构

把论文的五段式迁移到 testing：

* **Analysis**：抽取输入字段、约束、异常、状态、规则
* **Pattern**：选择黑盒测试技术（EP / BVA / Decision Table / State Transition）
* **Steps**：分步推导分区、边界、规则、状态转移场景
* **Verification**：自检是否覆盖正常/异常/边界/非法场景
* **FinalAnswer**：输出最终测试用例表

### 3.3 Testing Contracts

给每种技术定义 checker contract：

* EP：必须有 valid class / invalid class / representative tests
* BVA：必须有 lower / upper / below / on / above
* Decision Table：必须有 conditions / actions / rules / rule-to-test mapping
* State Transition：必须有 states / events / legal transitions / illegal transitions

### 3.4 ARG-Test 与 ARG-Test-Pro

* **ARG-Test**：单次结构化生成 + checker 验证
* **ARG-Test-Pro**：多候选生成 + checker-aware reranking + targeted repair

这正是你论文里 ARG 与 ARG-Pro 的 testing 版迁移。

## 4. Implementation

讲清楚怎么做：

* Python 实现
* LLM API 调用
* JSON/Markdown 结构化输出
* Python checker 或 clingo ASP checker
* CSV/JSON/pytest 输出
* CLI 或简单 Web demo

## 5. Baselines

至少 3 个：

* **Traditional non-AI baseline**：人工规则/模板法
* **Plain LLM baseline**：直接 prompt 生成 test cases
* **Structured w/o verification**：有结构，但无 checker
* **Full ARG-Test**：完整方法

## 6. Experimental Design

* requirement 数据集设计
* gold coverage checklist
* 指标设计
* generalizability 设置
* ablation 设置

## 7. Results and Analysis

* 主结果
* case study
* ablation
* generalizability
* 成本分析

## 8. Comparison with Traditional Technique

比较手工/规则法与 AI 方法的优缺点。

## 9. Limitations and Improvements

分析 AI 失败模式，以及你们如何修复。

## 10. Conclusion

强调你们的价值不是“让 LLM 随便生成测试”，而是构建了一个**可审计、可验证、可修复**的 testing tool。

---

# 三、完整 project proposal（可直接当你们 proposal 的母版）

下面这部分，我按“可直接拿来写文档”的方式给你。

## 1. Project Title

**ARG-Test: Auditable Requirement-Driven Black-Box Test Generation with Structured LLM Reasoning and Contract Verification**

## 2. Abstract

**Abstract**
This project proposes ARG-Test, an AI-based black-box testing tool that generates auditable test cases from natural-language software requirements. Instead of directly prompting a large language model to output test cases in free form, ARG-Test constrains the model to produce a structured testing trace consisting of Analysis, Pattern, Steps, Verification, and FinalAnswer. The generated trace is then checked against technique-specific testing contracts covering Equivalence Partitioning, Boundary Value Analysis, Decision Table Testing, and optionally State Transition Testing. Based on checker feedback, the system can rerank multiple candidates and repair incomplete or inconsistent outputs. The final output includes test cases, testing rationale, coverage tags, and diagnostic reports. We evaluate the tool in terms of correctness, coverage, executability, redundancy, and generalizability, and compare it with traditional non-AI rule-based testing and plain LLM prompting. The project aims to demonstrate that structured reasoning and contract verification can improve the quality, explainability, and reliability of AI-generated test design.

## 3. Background and Motivation

传统黑盒测试理论很成熟，但人工设计测试用例仍然有三个问题：

* 阅读需求耗时长
* 复杂规则和边界条件容易漏
* 不同测试人员产出不稳定

直接使用 LLM 虽然能降低工作量，但 free-form 输出存在明显缺点：

* 不可审计
* 很难检查是否真的覆盖了关键 partition / boundary / rule
* 容易输出冗余或不一致的 expected result

你论文的思想正好提供了解法：**把推理结构化，并把“faithfulness”操作化成 trace–contract consistency**，也就是不去假装证明模型内部“真实思考”，而是检查它输出的测试设计轨迹是否满足它声称采用的测试逻辑。这个思路非常适合软件测试课程项目。

## 4. Problem Statement

本项目要解决的问题是：

> 如何从自然语言需求说明中，自动生成高质量、覆盖充分、可验证、可审计的黑盒测试用例？

### 输入

* 一段软件需求说明
* 可选补充信息：字段限制、业务规则、异常规则、状态描述

### 输出

* 一组测试用例
* 每条用例的 technique label
* structured reasoning trace
* contract verification result
* coverage summary / diagnostics

### 核心挑战

* 需求描述可能模糊
* 测试技术选择可能错误
* LLM 容易漏 invalid cases 和 edge cases
* expected output 可能不一致
* 生成结果可能重复、不完整

## 5. Research Questions

### RQ1

与 plain LLM 相比，结构化测试推理能否提高测试用例质量和覆盖率？

### RQ2

引入 contract checker 后，能否显著减少遗漏边界、缺少 invalid class、规则不完整等问题？

### RQ3

多候选 reranking 和 targeted repair 能否进一步提高最终 test suite 的有效性？

### RQ4

该方法能否在不同类型需求上保持稳定表现？

## 6. Proposed Method

## 6.1 System Overview

建议你们在 proposal 里画这张图：

**Requirement Input**
→ Requirement Preprocessor
→ Prompt Builder
→ LLM Structured Testing Trace Generator
→ Section Parser
→ Technique Contract Checker
→ Candidate Reranker / Repair Module
→ Final Test Case Exporter
→ Evaluation Module

这个结构就是论文 Figure 1 的 testing 迁移版：上层负责生成，下层负责验证和控制。

## 6.2 Structured Testing Trace Schema

你们工具强制 LLM 输出以下五部分：

### Analysis

提取：

* 输入变量
* 合法/非法条件
* 数值范围
* 状态
* 规则依赖
* 异常行为

### Pattern

选择技术，并说明原因：

* EP
* BVA
* Decision Table
* State Transition

### Steps

分步推导：

* 如何划分等价类
* 如何找边界点
* 如何列 decision rules
* 如何列状态转移

### Verification

检查：

* 是否有 normal cases
* 是否有 invalid cases
* 是否有 boundary cases
* 是否有 exception cases
* 是否有 illegal transition
* 是否有冗余或冲突

### FinalAnswer

导出标准化测试表。

## 6.3 Contract Checker Design

这一块是你们项目的创新心脏。

### EP contract

必须检查：

* 是否识别出至少一个 valid partition
* 是否识别出至少一个 invalid partition
* 每个 partition 是否至少有一个 representative test
* 是否说明 partition 对应的 expected behavior

### BVA contract

必须检查：

* 是否识别出 lower bound / upper bound
* 是否覆盖 below / on / above
* 对于长度、数量、次数等离散边界，是否转换成整数测试点

### Decision Table contract

必须检查：

* 是否列出 conditions
* 是否列出 actions
* 是否形成完整或声明性的 rule combinations
* 是否每个 rule 至少映射一个 test case

### State Transition contract

必须检查：

* 是否列出 states
* 是否列出 events/triggers
* 是否区分 legal / illegal transitions
* 是否覆盖初始状态及关键异常转移

### 通用 contract

还要检查：

* 结构完整性
* 字段不为空
* Verification 是否引用前面的推导结果
* FinalAnswer 是否能解析成标准表格
* 用例是否重复
* expected output 是否自相矛盾

## 6.4 ARG-Test-Pro: Reranking and Repair

论文里 ARG-Pro 用 checker-aware reranking 与 refinement 提高结果质量。你们可以直接迁移。

具体做法：

1. 对同一需求生成 N 个候选 test suite
2. 对每个候选计算分数

   * structure completeness
   * contract pass rate
   * reference integrity
   * redundancy penalty
   * optional oracle consistency
3. 选出分数最高者
4. 如果低于阈值，触发 repair prompt
5. repair 只修改有问题的部分，而不是整段重写

这会让你们的方法明显强于“只生成一次”的 plain LLM。

---

# 四、最稳妥的实现范围

这里我给你一个**必须做 / 加分做 / 可选做**的分层版本。

## A. 必须做（最低风险也足够高分）

* 输入：requirements only
* 技术：EP + BVA + Decision Table
* 结构化输出：五段式
* checker：Python rule checker
* baseline：rule-based + plain LLM + structured-no-checker
* 数据集：8–10 个 requirement
* 指标：coverage / correctness / redundancy / cost
* 报告 + PPT + demo

## B. 加分做

* State Transition Testing
* best-of-3 candidate reranking
* repair prompt
* structured JSON export
* 自动生成 pytest

## C. 可选做（时间够再上）

* clingo/ASP checker
* 第二个模型的 generalizability 实验
* bug-seeded reference implementations 的 mutation/fault detection
* 简单 Web UI

**最现实建议**：
你们把 A 全做稳，再做 B；C 作为 bonus。

---

# 五、具体执行方案：把老师要求一项一项落地

下面这部分最重要。我把老师要求的每个 submission item，直接变成“你们该做什么”。

## 1. Input: requirement / project code base

### 你们怎么做

本项目主输入选择 **requirements**。

### 具体执行

准备 8–10 份 requirement 文档，每份 0.5–1 页，类型覆盖：

* 输入校验类
* 业务规则类
* 状态流转类

### 推荐需求集

1. User registration validation
2. Password policy checker
3. Shipping fee calculator
4. Coupon/discount engine
5. Bank transfer rule checker
6. Login lockout workflow
7. Ticket booking/refund rule
8. Order approval state machine
9. Vending machine state flow（可选）
10. Elevator controller（可选）

### 产物

`data/requirements/*.txt`

---

## 2. Tool artifact: prompts used, model used, model-generated code

### 你们怎么做

必须把 prompts、模型、生成代码完整保存。

### 具体执行

在项目里建立：

* `prompts/system_prompt.txt`
* `prompts/generation_prompt.txt`
* `prompts/repair_prompt.txt`
* `prompts/baseline_plain_llm.txt`

再在报告中写明：

* 使用模型名称
* temperature
* max tokens
* sampling 次数
* rerank 规则

### 还要保存

* 模型输出原文
* 解析后的 JSON / CSV
* checker log
* repair 前后对比

### 产物

`artifacts/raw_generations/`
`artifacts/parsed_traces/`
`artifacts/checker_logs/`

---

## 3. Generated output: test cases / alarms

### 你们怎么做

你们输出的是 **test cases**，不是 static alarms。

### 统一输出格式

每条用例至少包含：

* Test ID
* Technique
* Requirement target
* Preconditions
* Input
* Expected Output
* Covered item
* Priority
* Checker status

### 建议格式

同时导出：

* CSV：便于统计
* JSON：便于程序处理
* Markdown 表：便于报告展示

### 产物

`outputs/final_tests/*.csv`
`outputs/final_tests/*.json`
`outputs/final_tests/*.md`

---

## 4. Experimental Analysis (Accuracy, Coverage, Generalizability, etc)

### 你们怎么做

不要只做一个“老师看起来很多数字”的表，而要分成 3 层：

### Outcome metrics

* Test correctness
* Expected-output consistency
* Executability（如果转 pytest）
* Fault detection / mutation score（加分）

### Process metrics

* Structure completeness
* Well-formedness
* Reference integrity
* Contract pass rate
* Repair success rate

### Cost metrics

* Tokens
* Latency
* Manual post-edit time

这和你论文的评估哲学是一致的：不要把 accuracy、structure、cost 混在一起。

---

## 5. Project report

### 你们怎么做

报告结构建议固定为：

1. Cover page
2. Abstract
3. Introduction
4. Background
5. Problem Definition
6. Method
7. Implementation
8. Experimental Setup
9. Results
10. Comparison with Traditional Method
11. Limitations and Improvements
12. Conclusion
13. References
14. Appendix

### Cover page 一定要有

* Team ID
* Full names
* Student IDs

---

## 6. Comparison to traditional non-AI-based technique

### 你们怎么做

这一项不能只写几句“传统方法慢、AI 快”，太虚。

### 最好的做法

设两个比较对象：

#### 传统方法 1：Rule-based template generator

手工写规则：

* 看关键词识别数值范围
* 自动生成 BVA
* 对包含 “if/when” 的规则生成 decision table 草案

#### 传统方法 2：Manual textbook design

让组员按课上方法手动设计 2–3 个 requirement 的 test suite，记录时间与覆盖。

### 比较维度

* 生成时间
* requirement coverage
* boundary coverage
* invalid-case coverage
* redundancy
* fault detection（若能跑）
* explainability

这样你们的“comparison”会很扎实。

---

## 7. Analytical report: limitations of AI and improvement process

### 你们怎么做

这部分单独成章，不要混在 discussion 里一句带过。

### 你们应记录的 AI 失败模式

* 漏 invalid partition
* 漏 just-below / just-above
* Decision table rule 不完整
* 把 requirement 理解错
* expected output 自相矛盾
* 输出冗余测试
* 把 EP 和 BVA 混在一起
* 状态转移不区分合法/非法

### 对应改进动作

* 增加 structured schema
* 加 technique contract checker
* 加 few-shot example
* 做 best-of-N reranking
* 用 diagnostics 触发 local repair
* 对 FinalAnswer 采用严格表格约束
* 添加去重逻辑

这正好能和论文里的 failure mode、diagnostic repair 和 contract boundary 对应起来。

---

## 8. Summary

### 你们怎么做

最后总结不要泛泛而谈，要回答这四件事：

1. 你们做了什么
2. 为什么比 plain LLM 更好
3. 相比传统方法优缺点是什么
4. 未来还能怎么扩展

---

# 六、最关键的实验设计

这是拿高分的关键。我建议你们用下面这个方案。

## 1. 数据集设计

### Development set

4 个 requirement
用于调 prompt、调 checker、调 repair

### Test set

6 个 requirement
最终只在这个集合上报告主结果

这样能避免“调到测试集上”的质疑。

## 2. requirement 类型分布

### 类型 A：输入验证

适合 EP + BVA
如 age、password、username length

### 类型 B：业务规则

适合 Decision Table
如 coupon、shipping、discount、refund

### 类型 C：流程/状态

适合 State Transition
如 login lockout、order approval

## 3. Gold reference 的准备方式

你们必须手工准备一个**gold checklist**，否则“coverage”很难说服老师。

每个 requirement 配一个 `gold_spec.json`：

* valid partitions
* invalid partitions
* boundaries
* decision rules
* legal transitions
* illegal transitions
* exception cases

然后看每个方法生成的测试用例覆盖了多少 gold 项。

## 4. 评价指标

### 4.1 Coverage metrics

* Partition Coverage
* Boundary Coverage
* Rule Coverage
* Transition Coverage
* Exception Coverage

### 4.2 Quality metrics

* Test Validity
* Expected Output Correctness
* Non-redundancy
* Requirement Relevance

### 4.3 Process metrics

* Structure Completeness
* Contract Pass Rate
* Repair Success Rate
* Diagnostic Accuracy

### 4.4 Efficiency metrics

* Avg tokens
* Avg latency
* Avg manual fix time

## 5. 强烈建议加入的加分实验：Fault Detection

这是我最建议你们做的额外增强，因为它会大幅提高“effectiveness/usefulness”这一项。

### 做法

对 4–6 个 requirement，各写一个很小的 reference implementation（Python 就行），再人为插入 2–3 个 bug/mutant。

然后把生成的 test cases 自动转成 pytest：

* 在正确版本上运行，看 test 是否合理
* 在 bug 版本上运行，看能杀死多少 mutant

### 指标

* Executable test rate
* Pass rate on correct version
* Mutation kill rate

这样你们的实验就不只是“看起来覆盖多”，而是能证明“真的更会发现错误”。

### 为什么这一步特别好

因为它把你论文里“executable validity signal”的思想迁移到了 testing 项目里。论文里用 executable checks 作为强信号；你们这里则用 test execution / mutation detection 作为强信号，非常顺。

---

# 七、baseline 设计的最终版本

我建议你们固定这四组。

## Baseline 1: Traditional Rule-Based

输入 requirement，用手工规则/模板生成测试用例。

## Baseline 2: Plain LLM

Prompt：
“Generate black-box test cases from this requirement.”

## Baseline 3: Structured LLM without Verification

五段式输出，但不经过 checker，不做 repair。

## Baseline 4: Full ARG-Test

五段式 + checker + rerank + repair

### 可选 Baseline 5

Full ARG-Test-Pro（best-of-3）

如果时间不够，至少做前四个。

---

# 八、你们的 prompts 应该怎么写

## 1. System Prompt（核心）

```text
You are a software testing expert. Given a natural-language requirement,
produce a structured black-box testing trace with exactly five sections:
Analysis, Pattern, Steps, Verification, FinalAnswer.

Rules:
1. Use only black-box testing techniques.
2. Explicitly choose from Equivalence Partitioning, Boundary Value Analysis,
   Decision Table Testing, and State Transition Testing.
3. Verification must check coverage of valid, invalid, boundary, and exception scenarios.
4. FinalAnswer must be a machine-readable table of test cases.
5. Do not omit expected outputs.
```

## 2. Generation Prompt（主方法）

```text
Requirement:
[REQUIREMENT TEXT]

Task:
Generate black-box test cases using a structured testing trace.

Output format:
Analysis:
...
Pattern:
...
Steps:
...
Verification:
...
FinalAnswer:
| Test ID | Technique | Preconditions | Input | Expected Output | Covered Item |
```

## 3. Plain LLM Baseline Prompt

```text
Read the requirement and generate a set of black-box test cases.
Return them as a table with inputs and expected outputs.
```

## 4. Repair Prompt

```text
The previous testing trace failed the checker.

Diagnostics:
- missing invalid partition for field "password"
- missing just-above boundary for "age"
- duplicated test cases T04 and T07

Please revise only the necessary parts and regenerate the final test suite.
Keep the five-section structure unchanged.
```

---

# 九、checker 具体怎么实现

## 最稳妥方案：Python rule checker

实现文件：

* `checker/schema_checker.py`
* `checker/ep_checker.py`
* `checker/bva_checker.py`
* `checker/decision_checker.py`
* `checker/state_checker.py`

### Schema checker 检查

* 五个 section 是否齐全
* 顺序是否正确
* 内容是否为空
* Verification 是否引用前面的步骤或 coverage item
* FinalAnswer 是否可解析为表格

### EP checker 检查

* 是否有 valid / invalid class
* 每个 class 是否有代表 case
* 是否至少包含一个正常路径和一个异常路径

### BVA checker 检查

* 是否识别边界
* 是否覆盖下界前/下界/下界后
* 是否覆盖上界前/上界/上界后

### Decision checker 检查

* 是否有 condition/action/rule
* 是否至少一条用例对应一条 rule
* 是否存在互斥冲突

### State checker 检查

* 是否定义状态和事件
* 是否覆盖关键合法转移
* 是否覆盖至少一个非法转移

## ASP 版本

如果你们时间够，进一步把这些规则写成 clingo facts/rules。
但从交付稳妥性来说，**Python checker 先做出来更重要**。

---

# 十、代码结构建议

```text
ARG-Test/
├── data/
│   ├── requirements/
│   ├── gold_specs/
│   └── mutants/
├── prompts/
│   ├── system_prompt.txt
│   ├── generation_prompt.txt
│   ├── repair_prompt.txt
│   └── baseline_plain_llm.txt
├── src/
│   ├── main.py
│   ├── llm_client.py
│   ├── parser.py
│   ├── reranker.py
│   ├── repair.py
│   ├── exporter.py
│   ├── checker/
│   ├── baselines/
│   └── evaluation/
├── outputs/
│   ├── raw_generations/
│   ├── parsed_traces/
│   ├── final_tests/
│   └── reports/
├── experiments/
│   ├── run_main.py
│   ├── run_baselines.py
│   └── run_ablation.py
├── README.md
├── requirements.txt
└── report_assets/
```

---

# 十一、报告怎么写，才能对准评分点

## 1. Understanding of concepts（10%）

这一项不要靠空话，要在 Background 里明确解释：

* 什么是 EP
* 什么是 BVA
* 什么是 Decision Table
* 什么是 State Transition
* 为什么这些是黑盒技术
* 你们的 tool 如何对应这些理论

## 2. Coherence of design and implementation（20%）

靠三点拿分：

* 整体架构图清楚
* 从 prompt 到 checker 到 final output 的流程闭环清楚
* implementation 和 method 一一对应

## 3. Coverage and usefulness（40%）

这是大头。一定要做：

* requirement coverage
* invalid/boundary/rule/transition coverage
* redundancy
* fault detection / executable validity（强烈建议）

## 4. In-depth analysis（20%）

一定要做：

* ablation
* case study
* failure mode analysis
* generalizability（不同 requirement 类型，最好再加一个第二模型小实验）

## 5. Presentation（10%）

做到：

* 结构清晰
* demo 能跑
* 一张流程图 + 一张案例图 + 两张结果表

---

# 十二、你们最终报告的推荐目录

你可以直接照这个目录写：

## Cover Page

Team ID / Names / Student IDs

## Abstract

## 1. Introduction

## 2. Background and Related Concepts

2.1 Black-box testing techniques
2.2 AI-assisted test generation
2.3 Limitation of plain LLM prompting

## 3. Problem Definition

3.1 Input and output
3.2 Objectives
3.3 Challenges

## 4. Method

4.1 ARG-Test overview
4.2 Structured testing trace
4.3 Technique-specific contracts
4.4 Reranking and repair

## 5. Implementation

5.1 System modules
5.2 Prompt design
5.3 Output format
5.4 Checker implementation

## 6. Experimental Setup

6.1 Requirement dataset
6.2 Baselines
6.3 Metrics
6.4 Threats to validity

## 7. Results

7.1 Main comparison
7.2 Case study
7.3 Ablation
7.4 Generalizability
7.5 Cost analysis

## 8. Comparison with Traditional Non-AI Technique

## 9. Limitations and Improvements

## 10. Conclusion

## References

## Appendix

* prompts
* extra examples
* additional tables

---

# 十三、PPT 最佳结构（15 分钟）

## Slide 1

Title + Team ID + Names + Student IDs

## Slide 2

Background and problem

## Slide 3

Why plain LLM is not enough

## Slide 4

Project goal and research questions

## Slide 5

ARG-Test framework

## Slide 6

Structured testing trace schema

## Slide 7

Contract checker design

## Slide 8

Example: one requirement → generated tests

## Slide 9

Experimental setup and baselines

## Slide 10

Main results

## Slide 11

Case study / ablation

## Slide 12

Comparison with traditional testing

## Slide 13

Limitations and future improvements

## Slide 14

Conclusion

### 时间建议

* 背景与问题：2 分钟
* 方法：5 分钟
* demo：2 分钟
* 实验：4 分钟
* 结论：2 分钟

---

# 十四、Q&A 最容易被问的问题

## 1. 你们的项目到底属于哪种 testing？

答：Requirement-driven black-box testing，主要覆盖 EP、BVA、Decision Table，部分扩展到 State Transition。

## 2. 你们的方法和 plain LLM 的区别是什么？

答：不是直接生成 test cases，而是先生成结构化测试设计轨迹，再用 contract checker 验证，再做 rerank/repair。

## 3. checker 能保证 test case 一定正确吗？

答：不能保证完整语义正确，但能显著减少结构遗漏、不完整覆盖和明显冲突；它验证的是 contract consistency，不是全能证明。

## 4. 为什么不选 static analysis？

答：因为本项目核心创新来自 requirement-to-test 的结构化 reasoning，更适合复用我们的方法学；static analysis 还依赖语言、AST 和大量现成工具，短期内不利于突出项目原创性。这个判断也能从你上传的静态分析工具列表看出来：现成生态太成熟。

## 5. 你们如何比较传统方法？

答：用 rule-based template generator 作为 automated non-AI baseline，并用小规模 manual textbook design 作为人工对照。

## 6. generalizability 怎么体现？

答：跨 requirement 类型；如果时间允许，再加一个第二模型的小规模复现实验。

---

# 十五、建议你们最终采用的“最稳版本”

我给你的最后定版如下：

## 项目最终题目

**ARG-Test: Auditable Requirement-Driven Black-Box Test Generation with Structured LLM Reasoning and Contract Verification**

## 输入

requirements only

## 核心支持技术

* Equivalence Partitioning
* Boundary Value Analysis
* Decision Table Testing

## 扩展技术

* State Transition Testing

## Baselines

* Rule-based template
* Plain LLM
* Structured LLM without checker
* Full ARG-Test
* 可选 ARG-Test-Pro

## 最关键结果指标

* Requirement coverage
* Boundary/invalid/rule coverage
* Test correctness
* Redundancy
* Contract pass rate
* Token/latency
* 可选 mutation kill rate

## 最关键创新点

* 结构化 testing trace
* technique-specific contract checker
* diagnostic-driven repair
* auditable output

---

# 十六、最后的执行清单

你们接下来就按这个顺序做：

## 第一步

把 8–10 个 requirements 定稿，并为每个 requirement 写 gold checklist。

## 第二步

实现最小系统：

* plain LLM baseline
* structured output
* parser
* Python checker
* final table exporter

## 第三步

做 full ARG-Test：

* checker 评分
* rerank/repair

## 第四步

补 baseline 与实验：

* rule-based baseline
* structured-no-checker baseline
* main comparison

## 第五步

做结果分析：

* main table
* case study
* ablation
* limitations

## 第六步

整理提交物：

* Report PDF
* PPT PDF
* code.zip
* README
* prompts
* raw outputs
* final test scripts

---

**一句话总结这个方案的优势：**
你们这个项目最好的定位，不是“LLM 生成测试用例”，而是**“用论文里的 ARG 思想，把测试设计过程结构化、可验证、可修复，再导出高质量黑盒测试用例”**。这会让你们的方法、实验、分析、展示都非常完整，而且和课程作业要求是强对齐的。

下一步我可以直接把这份内容继续展开成两样东西：
**1）可直接提交的英文 project proposal 正文；2）可直接讲的英文 PPT 逐页文案。**
