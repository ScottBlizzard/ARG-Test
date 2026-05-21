# Remaining Feature Closure Status

日期：`2026-05-07`

本文件专门回答一个问题：

> 在“最严格意义下还没做满的功能点”里，现在哪些已经补齐，哪些还需要重跑实验？

## 1. 已补齐的功能点

### 1.1 FR 1.0 Input / Parsing

现在已经明确支持三种输入形态：

- requirement file input
- direct text input
- CSV batch input

对应入口：

- [src/main.py](/D:/软件测试/Final/ARG-Test/src/main.py:1)
- [src/input_loader.py](/D:/软件测试/Final/ARG-Test/src/input_loader.py:1)

对应 CLI：

- `python -m src.main run`
- `python -m src.main run-text`
- `python -m src.main batch-csv`

smoke evidence：

- `.local_runs/input_mode_smokes/outputs/reports/adhoc/direct_text_state_demo_summary.json`
- `.local_runs/input_mode_smokes/outputs/reports/adhoc/csv_coupon_rule_summary.json`
- `.local_runs/input_mode_smokes/outputs/reports/adhoc/csv_order_workflow_summary.json`

### 1.2 FR 4.0 White-Box Test Modeling / State Modeling

现在已经新增 state-model capability：

- workflow requirement 的状态集合提取
- legal / illegal transition 抽取
- `All States` coverage plan
- `All Transitions` coverage plan
- exportable JSON / Markdown state-model artifact

对应实现：

- [src/state_model.py](/D:/软件测试/Final/ARG-Test/src/state_model.py:1)
- [src/schemas.py](/D:/软件测试/Final/ARG-Test/src/schemas.py:1)
- [src/pipeline.py](/D:/软件测试/Final/ARG-Test/src/pipeline.py:1)
- [src/exporter.py](/D:/软件测试/Final/ARG-Test/src/exporter.py:1)

CLI 入口：

- `python -m src.main state-model`

workflow formal evidence：

- `.local_runs/formal_qwen_novpn/outputs/state_models/test/order_approval_state_machine.md`
- `.local_runs/formal_qwen_novpn/outputs/state_models/test/payment_3ds_authentication_flow.md`
- `.local_runs/formal_qwen_novpn/outputs/state_models/test/warehouse_pickup_order_workflow.md`

### 1.3 Defect-Seeded Usefulness Demonstration

现在已经补入 coupon module 的 seeded mutants：

- multiple-coupon rule mutant
- SAVE10 boundary mutant
- SAVE20 sale-item mutant
- FREESHIP boundary mutant

对应实现：

- [coupon_discount_engine_mutants.py](/D:/软件测试/Final/ARG-Test/reference_impl/coupon_discount_engine_mutants.py:1)
- [run_mutation_demo.py](/D:/软件测试/Final/ARG-Test/experiments/run_mutation_demo.py:1)

自动验证：

- [test_mutation_demo.py](/D:/软件测试/Final/ARG-Test/tests/test_mutation_demo.py:1)

证据结果：

- [coupon_discount_engine_mutation_demo.md](/D:/软件测试/Final/ARG-Test/final_docs/execution_evidence/coupon_discount_engine_mutation_demo.md:1)
- `4/4 mutants killed`
- `kill rate = 1.0`

### 1.4 NFR Formalization

现在已经形成独立 NFR 文档与可运行验证：

- [09_nfr_validation_report_cn.md](/D:/软件测试/Final/ARG-Test/final_docs/09_nfr_validation_report_cn.md:1)
- [run_nfr_checks.py](/D:/软件测试/Final/ARG-Test/experiments/run_nfr_checks.py:1)
- [nfr_validation_summary.md](/D:/软件测试/Final/ARG-Test/final_docs/execution_evidence/nfr_validation_summary.md:1)

覆盖：

- performance
- usability
- security
- maintainability

## 2. 这批功能补齐后，实验要不要全量重跑

结论：

- **不需要把 main / baseline / ablation / generalization 全量重新跑一遍。**
- **只需要做针对性验证与必要的离线 enrichment。**

原因很明确：

1. `CSV/direct input` 是新入口，不改变原有 main experiment 的生成逻辑。
2. `state-model` 是新增 sidecar capability，不改变原有 coverage/evaluation 指标计算口径。
3. `mutation demo` 是 detailed module 的新增执行证据，不影响 main experiment 数字。
4. `NFR checks` 是新增验证资产，不影响 main/baseline/ablation/generalization 的统计结果。

## 3. 已经做过的必要验证

### 3.1 新功能 smoke

已完成：

- `run-text` smoke
- `batch-csv` smoke
- `state-model` smoke

### 3.2 正式 live 结果离线 enrichment

已完成：

- `.local_runs/formal_qwen_novpn` 已重新做 offline upgrade
- 新增 `state_models/`
- formal reports 已保留并补入新的 sidecar metadata

因此：

- 正式主结果源仍然可继续使用 `.local_runs/formal_qwen_novpn/outputs/reports/`
- 不需要因为这批新功能而重做全量 live rerun

## 4. 什么时候才需要重跑全量实验

只有在下面这些情况发生时，才值得重跑：

1. 改了 prompts，导致生成内容本身变化
2. 改了 reranker / checker / repair 的评分逻辑
3. 改了 evaluation metrics 定义
4. 想把 final report 的“主实验数字”全部切换到一份全新 runtime

当前这次补强没有触发以上 4 点。

## 5. 当前判断

对这批你点名的严格缺口，现在可以这样判断：

- `CSV/direct input`：已补齐
- `更完整的 FR 4.0`：已补齐到课程项目可 defend 的程度
- `NFR formalization`：已补齐
- `defect-seeded usefulness demonstration`：已补齐

所以现在不需要再为这些功能点停下来重做大规模实验。

下一阶段应该把重心切到：

1. final report 正文
2. final PPT
3. demo 视频
4. 最终 submission package
