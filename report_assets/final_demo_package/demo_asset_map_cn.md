# Demo Asset Map

这份文件列出录屏和 PPT 最应该打开或引用的资产。当前推荐路径是 Web UI；旧 `.local_runs/final_demo_mock` 命令行产物只作为 fallback。

## 1. Web Demo 入口

- 后端：`demo_web/app.py`
- 前端：`demo_web/static/index.html`
- 样式：`demo_web/static/styles.css`
- 前端逻辑：`demo_web/static/app.js`
- 运行命令：

```powershell
python -m uvicorn demo_web.app:app --host 127.0.0.1 --port 8000
```

- 浏览器地址：`http://127.0.0.1:8000/`

## 2. 录屏用输入

- CSV 示例：`final_docs/execution_evidence/sample_requirement_batch.csv`
- Direct 推荐案例：`pickup_station_contact_validation`
- State Model 推荐案例：`warehouse_pickup_order_workflow`
- Formal Evidence 页面：直接使用前端 tab，不需要手动打开 JSON。

## 3. 正式结果快照

- `frontend_focus/formal_results_snapshot/reports/test/run_main_summary.json`
- `frontend_focus/formal_results_snapshot/reports/test/baseline_summary.json`
- `frontend_focus/formal_results_snapshot/reports/test/generalization_by_category.json`
- `frontend_focus/formal_results_snapshot/reports/test/ablation_summary.json`
- `frontend_focus/formal_results_snapshot/final_tests/test/`
- `frontend_focus/formal_results_snapshot/state_models/test/`

这些路径是前端 replay 和 Formal Evidence Dashboard 的数据来源。

## 4. 已准备好的前端截图

- `frontend_focus/screenshots/web_demo_direct_frozen_replay.png`
- `frontend_focus/screenshots/web_demo_state_model_extraction.png`
- `frontend_focus/screenshots/web_demo_formal_evidence_dashboard.png`

PPT 可以直接复用这些截图。若录屏同学重新美化前端，建议重新截同名或新名截图。

## 5. PPT 推荐图

- `../figures/final_result_scorecard.png`
- `../figures/main_vs_baselines.png`
- `../figures/generalization_by_category.png`
- `../figures/ablation_gain.png`
- `../figures/reproducibility_stability_overview.png`
- `../../final_docs/detailed_test_design_execution/figures/coupon_module_evidence_scorecard.png`

## 6. 详细执行证据

- `final_docs/execution_evidence/coupon_discount_engine_execution_summary.md`
- `final_docs/execution_evidence/coupon_discount_engine_coverage.xml`
- `final_docs/execution_evidence/coupon_discount_engine_branch_coverage.xml`
- `final_docs/execution_evidence/coupon_discount_engine_mutation_demo.md`

## 7. 如果只来得及打开最少文件

优先打开：

1. Web UI：`http://127.0.0.1:8000/`
2. CSV 示例：`final_docs/execution_evidence/sample_requirement_batch.csv`
3. 前端截图目录：`report_assets/final_demo_package/frontend_focus/screenshots/`
4. PPT 蓝图：`report_assets/final_ppt_blueprint_cn.md`
