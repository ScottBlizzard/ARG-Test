# Final Upgrade 实施状态

日期：`2026-05-07`

本文件记录的是“升级方案已经实际做到哪里”，不是前期规划。

## 1. 已完成的升级

### 1.1 风险分析进入主流水线

已完成：

- requirement 级 `risk_score / risk_level / drivers / recommended_focus`
- test case 级 priority 自动提升
- `category + risk_assessment` 写入 summary / checker log / final tables

对应实现：

- `src/risk.py`
- `src/schemas.py`
- `src/pipeline.py`
- `src/exporter.py`

### 1.2 正式运行元数据落盘

已完成：

- `run_main_manifest.json`
- `baseline_manifest.json`
- `ablation_manifest.json`
- `generalization_manifest.json`
- `stability_sanity_manifest.json`
- `repeatability_manifest.json`

这些 manifest 会记录：

- provider
- model
- candidates
- enable_repair
- split
- runtime_root
- requirement_ids
- execution timestamp

### 1.3 新增 repeatability 正式脚本

已完成：

- `experiments/run_repeatability.py`

作用：

- 支持 `3 independent reruns`
- 自动汇总 score mean/std、coverage mean/std、max delta、stable case count
- 直接输出 JSON 和 Markdown

### 1.4 汇总表升级

已完成：

- `experiments/export_summary_tables.py` 现在会导出 `category / risk_level / risk_score`

这意味着后续 PPT 和 final report 可以直接从表格引用风险维度，而不是手工补列。

### 1.5 自动化验证补齐

已完成：

- 新增 `tests/test_risk_assessment.py`
- 当前仓库测试结果：`18 passed`

新增验证覆盖：

- 风险评分
- priority escalation
- mock pipeline 导出 `risk_assessment` 与 `run_context`

### 1.6 详细执行模块继续增强

`coupon_discount_engine` 现在具备：

- black-box tests
- white-box tests
- statement coverage `100%`
- branch coverage `100%`

证据文件：

- `final_docs/execution_evidence/coupon_discount_engine_execution_summary.md`
- `final_docs/execution_evidence/coupon_discount_engine_coverage.xml`
- `final_docs/execution_evidence/coupon_discount_engine_branch_coverage.xml`

## 2. 已完成的运行验证

### 2.1 Full mock end-to-end

已完成完整 mock 验证，路径：

- `.local_runs/upgrade_mock/outputs/reports/test/`
- `.local_runs/upgrade_mock_repeatability/outputs/reports/test/`

已产出：

- main
- baseline
- ablation
- generalization
- tables
- repeatability

关键结果：

- `test = 16/16`
- `business_rules` avg overall coverage = `0.175`
- `input_validation` avg overall coverage = `0.284`
- `workflow_state` avg overall coverage = `0.024`
- mock repeatability = `16/16 stable`

这组结果的意义不是“最终性能数字”，而是“升级后的全链路已经跑通且结构正确”。

### 2.2 Live provider smoke

已完成在线 provider smoke run，路径：

- `.local_runs/formal_qwen_upgrade_smoke/outputs/reports/test/`

已验证：

- 升级后的 `run_main + risk + manifest` 在真实模型上可运行
- `coupon_discount_engine` smoke case 成功出结果

## 3. 结果源现状

这里必须明确区分三类结果：

### 3.1 旧的仓库根目录结果

- `outputs/reports/test/run_main_summary.json`

现状：

- 仍是 `10-case legacy snapshot`
- 不应继续作为 final 主引用源

### 3.2 历史正式 live 结果

- `.local_runs/formal_qwen_novpn/outputs/reports/test/`

现状：

- 已覆盖 `16/16`
- 已通过离线升级脚本补入 `category / risk / manifest / tables`
- 可以直接作为 final 主引用源

### 3.3 升级后的验证结果

- `.local_runs/upgrade_mock/...`
- `.local_runs/formal_qwen_upgrade_smoke/...`

现状：

- 已经带有新的 risk/manifest/table 能力
- 适合证明升级实施完成
- mock 结果不能直接当 final 主实验数字引用

## 4. 现在还剩下什么

严格来说，代码升级本身已经完成。剩余工作主要是“最终成品化”，不是“继续搭底层能力”。

还剩：

1. 固定 final 主引用结果口径
2. 把 final 报告正文写满
3. 把 PPT / demo / presentation script 做成成稿
4. 选定 2 到 3 个最终展示 case 并人工校对表达

## 5. 当前判断

当前项目状态已经从：

- “有升级方案”

进入到了：

- “升级方案已经落地，且有自动化验证和运行证据”

换句话说，后续工作的重心不应再放在“还要不要改架构”，而应放在：

- 冻结结果源
- 写 final report
- 做 presentation
