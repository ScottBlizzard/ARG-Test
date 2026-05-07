# Test Plan Draft

## 1. Project Scope

### 1.1 Background

`ARG-Test` is an AI-assisted AutoTestDesign system that converts natural-language requirements into auditable black-box test suites. The final project extends the middle-phase prototype into a more complete testing project with risk analysis, formal planning, detailed execution evidence, and presentation-ready artifacts.

### 1.2 Objectives

- generate structured black-box test cases from requirements
- improve auditability over plain LLM prompting
- validate generated traces with technique-specific contracts
- export reusable testing artifacts
- demonstrate one major module with black-box plus white-box evidence

## 2. Test Items

### 2.1 Major Functional Features

- requirement ingestion and parsing
- structured trace generation
- technique selection and reasoning trace output
- contract checking for EP / BVA / Decision Table / State Transition
- candidate reranking and repair
- final artifact export
- evaluation and summary generation

### 2.2 Major Non-Functional Features

- reproducibility
- usability of generated artifacts
- maintainability of project structure
- execution stability for batch experiments

### 2.3 System Architecture

Main components:

- `src/main.py`: entry point
- `src/pipeline.py`: orchestration
- `src/llm_client.py`: provider interface
- `src/parser.py`: structured trace parser
- `src/checker/`: contract checkers
- `src/reranker.py` and `src/repair.py`: candidate control
- `src/exporter.py`: artifact export
- `src/evaluation/metrics.py`: evaluation

## 3. High-Level Test Suite Design

### Suite A: Functional correctness of pipeline

- technique: script-based integration tests
- target: end-to-end trace generation, parsing, checking, export

### Suite B: Output quality validation

- technique: gold-spec based evaluation
- target: coverage, duplicates, diagnostics, final summaries

### Suite C: Baseline and ablation comparison

- technique: controlled experiment runs
- target: plain LLM vs rule-based vs structured-no-checker vs full pipeline

### Suite D: Detailed module execution

- technique: black-box + white-box
- target: selected module `coupon_discount_engine`

## 4. Test Levels and Objectives

| Level | Objective | Evidence |
| --- | --- | --- |
| Unit | validate parser/checker/export helper behavior | targeted scripts or pytest |
| Integration | verify full pipeline data flow | `experiments/run_main.py` and outputs |
| System | verify end-to-end generation/export/evaluation | `outputs/reports/` summaries |
| Acceptance | verify final deliverables support report/demo requirements | final_docs, figures, PPT, demo checklist |

## 5. Schedule / Checklist

### Phase 1

- finalize final_docs structure
- freeze middle baseline
- confirm official result source paths

### Phase 2

- choose detailed module
- add white-box execution support
- rerun key experiments if needed

### Phase 3

- finalize risk analysis, test plan, and detailed execution report
- export figures/tables
- build PPT and demo

### Phase 4

- final consistency check
- generate submission package
- record demo video

## 6. Organization Chart

建议保留现有按职责分工方式：

- role 1: integration / prompts / pipeline / final merge
- role 2: report / PPT / presentation assets
- role 3: dataset / main experiments
- role 4: baselines
- role 5: evaluation / ablation / failure analysis

## 7. Testing Framework and Rationale

### Primary framework

- `pytest` for executable white-box and module-level regression tests

理由：

- 与 Python 主仓库一致
- 容易保存执行日志
- 便于覆盖率工具接入

### Supporting framework

- repository scripts in `experiments/`
- JSON/CSV export validation
- markdown evidence generation

## 8. Cost Estimation

建议按人天估算而不是写空泛描述：

| Work Item | Estimated Effort |
| --- | --- |
| final doc structure and planning | 1 to 2 person-days |
| risk analysis and test plan writing | 1 to 2 person-days |
| detailed module implementation and execution | 2 to 3 person-days |
| experiment rerun and figure export | 2 to 3 person-days |
| PPT, demo, final packaging | 1 to 2 person-days |

总计建议预算：

- `7 to 12 person-days` depending on whether formal reruns and executable module support are added

## 9. Exit Criteria

- required final documents are complete
- all cited results come from approved evidence paths
- one detailed module has both black-box design and white-box execution evidence
- repository can explain the full pipeline in demo form
