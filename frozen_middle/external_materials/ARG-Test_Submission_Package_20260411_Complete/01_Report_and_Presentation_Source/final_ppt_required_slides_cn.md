# 最终答辩 PPT 终版清单（按五人英文讲稿对齐）

本文档用于指导最终答辩 PPT 的内容组织，并与英文讲稿文件完全对齐：

- `final_defense_script_5members_en.md`

本版本按老师要求控制为 `10` 页以内，并围绕以下重点展开：

- test requirements analysis
- test design
- team-AI interaction
- prompts
- analysis of generated test cases
- thinking and verification methods
- revision of the test plan to the final version

## 1. 先说明一个规则

老师原话是：第一大作业由每组 `one representative` 主讲。

所以正式上台时，最稳的默认方案仍然是：

- `Yi Xu` 作为主讲人
- 其他四位成员负责 Q&A 备战

但为了便于你们五个人都准备清楚，这份 PPT 结构和讲稿仍然按“五人分工版”组织。即使最后只有一个人讲，也可以直接把这 10 页顺着讲完。

## 2. PPT 最终提交时必须满足什么

- 提交给老师/TA 的最终文件是 `PPT 导出的 PDF`
- 汇报语言是 `English`
- 总页数不超过 `10`
- 第一页必须包含：
  - `Team ID`
  - 所有成员 `full names`
  - 所有成员 `student IDs`

## 3. 推荐的最终 10 页结构

### Slide 1. Cover

**建议主讲人：Yi Xu**

必须包含：

- project title
- team ID
- full names
- student IDs

推荐标题：

- `ARG-Test: Auditable Requirement-Driven Black-Box Test Generation with Structured LLM Reasoning and Contract Verification`

要点：

- 不讲技术细节
- 只讲项目是什么、你们要解决什么问题

### Slide 2. Problem and Scope

**建议主讲人：Yi Xu**

必须讲清楚：

- 你们做的是 `AI-enhanced black-box dynamic testing`
- 当前实现的是 `System Requirements -> Test Cases`
- 不是 codebase branch，而是 requirement-driven branch
- 核心目标是从自然语言需求中生成可审计的测试用例

一句话目标：

- `Given natural-language requirements, we generate auditable black-box test cases with structured reasoning and verification.`

### Slide 3. Requirement Analysis and Input

**建议主讲人：Member 3（数据与需求分析负责人）**

必须讲：

- requirement 输入长什么样
- 测试场景是什么
- 数据集规模和划分

建议展示：

- 1 个 requirement snippet
- 数据集统计：
  - `dev = 50`
  - `test = 16`

### Slide 4. Tool Artifact and Prompt Design

**建议主讲人：Member 3**

必须讲：

- 用了什么模型：`Qwen3.5-Flash`
- prompt family 有哪些：
  - `system_prompt`
  - `generation_prompt`
  - `repair_prompt`
  - `baseline_plain_llm`
- prompt 为什么不能只靠一句 plain prompt

这一页要开始体现老师要求的：

- `team-AI interaction`
- `prompts`

### Slide 5. Pipeline and Architecture

**建议主讲人：Member 4（Prompt / Pipeline 负责人）**

这一页放架构图：

- `latex_report/figures/arg_test_architecture_final.pdf`

必须讲：

- structured trace
- parser
- checker suite
- reranking
- repair
- final export

推荐口径：

- `The tool is a full pipeline rather than a single prompt call.`

### Slide 6. Generated Output Example

**建议主讲人：Member 4**

必须讲：

- 最终输出不是自由文本
- 而是结构化 test suite
- 包含 technique, input, expected output, and covered item

建议展示：

- 1 个代表性 requirement
- 2 到 4 条 representative test cases

这一页对应老师要求的：

- `analysis of generated test cases`

### Slide 7. Main Result and Baseline Comparison

**建议主讲人：Member 5（实验与验证负责人）**

建议使用图：

- `final_result_scorecard.pdf`
- `main_vs_baselines.pdf`

必须口头讲清楚的数字：

- `avg checker score = 0.959`
- `avg overall coverage = 0.615`
- `rule_based coverage = 0.147`
- `plain_llm coverage = 0.030`
- `structured_no_checker coverage = 0.538`
- `full_pipeline coverage = 0.615`

必须点明：

- full pipeline 明显优于传统非 AI baseline
- structured pipeline 明显优于 plain prompting

### Slide 8. Verification, Ablation, and Generalization

**建议主讲人：Member 5**

建议使用图：

- `ablation_gain.pdf`
- `generalization_by_category.pdf`

必须讲：

- checker / repair 明显提高 `checker score`
- coverage 与 no-checker 版本接近，但结果更一致、更可审计
- 三类 requirement 都能工作：
  - `business_rules = 0.577`
  - `input_validation = 0.579`
  - `workflow_state = 0.697`

这一页对应老师要求的：

- `thinking and verification methods`

### Slide 9. Team-AI Interaction and Revision to Final Version

**建议主讲人：Luowu Zhang**

这是老师要求里非常关键的一页。

必须讲：

- 初始 plain generation 的问题
- 为什么加入 structured trace
- 为什么加入 parser / checker
- 为什么加入 reranking / repair
- 怎么从 early plan 修到 final version

推荐版式：

- 左边：`Problem in early version`
- 右边：`What we changed`

这一页要直接对应老师原话里的：

- `team–AI interaction`
- `revision of the test plan to form the final version`

### Slide 10. Conclusion

**建议主讲人：Luowu Zhang**

必须讲：

- 项目做成了什么
- 为什么说它成功
- 相比传统方法的优势
- limitation 和 future work 一句带过

推荐结论句：

- `ARG-Test shows that structured LLM reasoning plus contract verification can produce more auditable and higher-coverage requirement-driven black-box tests than prompt-only or rule-based baselines.`

## 4. 五个人各自要准备什么

### Yi Xu

- 项目目标
- scope
- requirement-driven black-box testing 的定位
- 项目整体价值

### Member 3

- requirement analysis
- input design
- dataset split
- prompt family overview

### Member 4

- architecture
- parser / checker / repair
- generated output example

### Member 5

- result metrics
- baseline comparison
- ablation
- generalization

### Luowu Zhang

- team-AI interaction
- revision process
- final takeaway
- report/PPT 层面的收束表达

## 5. 建议使用的图

- `latex_report/figures/arg_test_architecture_final.pdf`
- `latex_report/figures/final_result_scorecard.pdf`
- `latex_report/figures/main_vs_baselines.pdf`
- `latex_report/figures/ablation_gain.pdf`
- `latex_report/figures/generalization_by_category.pdf`

稳定性图和 case study 图不是必须页，除非你们排练后还有时间。

## 6. 最终提交时，和 PPT 相关的正式文件

- `Final Presentation (PDF)`

如果你们自己想留底，可以另外保留：

- `.pptx` source file

但正式提交要求里，核心是 `PDF`。

## 7. 一句话结论

你们最后的 PPT 只要严格按这 `10` 页讲：

- 输入和需求分析
- prompt 和 team-AI interaction
- pipeline
- generated outputs
- 实验结果
- verification / ablation / generalization
- revision to final version
- conclusion

并且第一页放全成员信息，就已经完整覆盖老师要求。
