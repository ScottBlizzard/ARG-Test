# Demo Asset Map

## 1. 现场运行脚本

- [run_demo_commands.ps1](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/run_demo_commands.ps1)

## 2. Live demo 输出路径

演示输出根目录：

- [final_demo_mock](/D:/软件测试/Final/ARG-Test/.local_runs/final_demo_mock)

### 2.1 Direct text demo

- summary:
- [direct_text_demo_summary.json](/D:/软件测试/Final/ARG-Test/.local_runs/final_demo_mock/outputs/reports/adhoc/direct_text_demo_summary.json)
- final tests:
- [direct_text_demo.md](/D:/软件测试/Final/ARG-Test/.local_runs/final_demo_mock/outputs/final_tests/adhoc/direct_text_demo.md)
- state model:
- [direct_text_demo state model](/D:/软件测试/Final/ARG-Test/.local_runs/final_demo_mock/outputs/state_models/adhoc/direct_text_demo.md)

推荐展示重点：

- risk assessment
- candidate controls
- legal state transitions
- all-states / all-transitions coverage plan

### 2.2 CSV batch demo

- sample CSV input:
- [sample_requirement_batch.csv](/D:/软件测试/Final/ARG-Test/final_docs/execution_evidence/sample_requirement_batch.csv)
- cleaner workflow example:
- [csv_order_workflow.md](/D:/软件测试/Final/ARG-Test/.local_runs/final_demo_mock/outputs/final_tests/adhoc/csv_order_workflow.md)
- coupon example:
- [csv_coupon_rule.md](/D:/软件测试/Final/ARG-Test/.local_runs/final_demo_mock/outputs/final_tests/adhoc/csv_coupon_rule.md)

推荐展示重点：

- same tool, multiple imported requirements
- Markdown / JSON / CSV exports

### 2.3 State-model demo

- state model:
- [warehouse_pickup_order_workflow state model](/D:/软件测试/Final/ARG-Test/.local_runs/final_demo_mock/outputs/state_models/test/warehouse_pickup_order_workflow.md)
- generated test suite:
- [warehouse_pickup_order_workflow.md](/D:/软件测试/Final/ARG-Test/.local_runs/final_demo_mock/outputs/final_tests/test/warehouse_pickup_order_workflow.md)

推荐展示重点：

- states
- legal transitions
- illegal transition
- All States / All Transitions plan

## 3. 正式结果图

- [final_result_scorecard.png](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/figures/final_result_scorecard.png)
- [main_vs_baselines.png](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/figures/main_vs_baselines.png)
- [reproducibility_stability_overview.png](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/figures/reproducibility_stability_overview.png)
- [coupon_module_evidence_scorecard.png](/D:/软件测试/Final/ARG-Test/report_assets/final_demo_package/figures/coupon_module_evidence_scorecard.png)

## 4. 正式案例和证据入口

- formal business-rule case:
- [coupon_discount_engine.md](/D:/软件测试/Final/ARG-Test/.local_runs/formal_qwen_novpn/outputs/final_tests/test/coupon_discount_engine.md)
- formal workflow state model:
- [warehouse_pickup_order_workflow formal state model](/D:/软件测试/Final/ARG-Test/.local_runs/formal_qwen_novpn/outputs/state_models/test/warehouse_pickup_order_workflow.md)
- executable evidence:
- [coupon_discount_engine_execution_summary.md](/D:/软件测试/Final/ARG-Test/final_docs/execution_evidence/coupon_discount_engine_execution_summary.md)
- mutation evidence:
- [coupon_discount_engine_mutation_demo.md](/D:/软件测试/Final/ARG-Test/final_docs/execution_evidence/coupon_discount_engine_mutation_demo.md)

## 5. 如果只开最少文件

录制时最少只开这 7 个：

1. `run_demo_commands.ps1`
2. `direct_text_demo_summary.json`
3. `csv_order_workflow.md`
4. `warehouse_pickup_order_workflow.md`
5. `main_vs_baselines.png`
6. `reproducibility_stability_overview.png`
7. `coupon_module_evidence_scorecard.png`
