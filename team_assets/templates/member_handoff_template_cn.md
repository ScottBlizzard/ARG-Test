# 成员结果交接

## 成员编号 / 姓名

- 成员：5 号
- 日期：2026-04-09
- 负责模块：`experiments/run_ablation.py`、`experiments/run_generalization.py`、`experiments/export_summary_tables.py`；test 分割下的 ablation、generalization、failure analysis 文档；与上述相关的 `src/evaluation/` 使用方式以仓库现状为准

## 本次完成内容

- 在 mock 配置（`provider=mock`，`model=mock-arg-test`，`candidates=3`）下完成 test 分割的 **消融**，生成 `structured_no_checker` 与 `full_pipeline` 对比，并导出 ablation 汇总表。
- 在存在 `outputs/reports/test/run_main_summary.json` 的前提下运行 **`run_generalization.py`**，按 `manifest.json` 中 test 条目的 **category** 聚合，导出 generalization 表。（主实验 summary 由主实验 workflow 产出，通常为 3 号或 1 号维护。）
- 按 `team_assets/templates/member5_failure_analysis_template_cn.md` 撰写 **`outputs/reports/test/failure_analysis_cn.md`**（四类失败模式及 limitations / threats to validity 素材）。
- 按 `team_assets/templates/member5_ablation_note_cn.md` 撰写 **`outputs/reports/test/member5_ablation_note_cn.md`**（ablation 与 generalization 结论文本，供报告引用）。

## 运行命令

```powershell
Set-Location '<本机ARG-Test根目录>'

.\experiments\run_role5_eval_workflow.ps1

# 分步等价：
# python experiments\run_ablation.py --split test --provider mock --model mock-arg-test --candidates 3
# python experiments\export_summary_tables.py --kind ablation --split test
# python experiments\run_generalization.py --split test
# python experiments\export_summary_tables.py --kind generalization --split test
```

## 正式输出文件路径

- `outputs/reports/test/ablation_summary.json`
- `outputs/reports/test/tables/ablation_summary_table.csv`
- `outputs/reports/test/tables/ablation_summary_table.md`
- `outputs/reports/test/generalization_by_category.json`
- `outputs/reports/test/tables/generalization_by_category.csv`
- `outputs/reports/test/tables/generalization_by_category.md`
- `outputs/reports/test/failure_analysis_cn.md`
- `outputs/reports/test/member5_ablation_note_cn.md`
- `outputs/reports/test/run_main_summary.json`（generalization 的输入；主实验产出，非 5 号单独生成）

## 核心结果摘要（5 到 10 行）

- test 分割共 **10** 条需求参与 ablation；汇总表展平约 **20 行**（每需求 × 两臂）。`full_pipeline` 下 `checker_score` 约 **0.65～0.95**；`repaired: false` 见于 `order_approval_state_machine`、`payment_3ds_authentication_flow`。
- 约 **7** 条需求在两臂下 **gold 的 overall_coverage 及分项 coverage 不变**，差异主要在 **checker 分** 与部分 **test_count**；`checkout_promo_stack_and_priority`、`gift_card_and_coupon_combination_rules`、`return_refund_method_eligibility` 等为 `repaired: true` 但摘要指标与 structured 臂相同，与 schema 类问题并存（见 `failure_analysis_cn.md`）。
- `generalization_by_category.json`：**business_rules** 6 条、**input_validation** 1 条、**workflow_state** 3 条；workflow 类平均覆盖约 **0.175**，平均 checker 约 **0.92**，与 business_rules 形成对照。该类聚合读取的是 **`run_main_summary.json`**，与 ablation 的生成脚本不同；当前仓库若主实验与 ablation 均为同一 mock 批次，full 臂数值可与 summary 对照。
- `payment_3ds_authentication_flow` 的 overall_coverage 约 **0.071**（当前 test 子集中最低）。多条需求存在 schema 步骤引用错误、decision 浅覆盖、规则题上 state 类检查失败等，详见 **`failure_analysis_cn.md`**。
- 当前结果为 **mock** 下可复现输出；正式报告若引用真实模型，需由 **1 号** 协调重跑主实验与 5 号脚本并更新产出。

## 已知问题

- 终稿与解析中常见占位表述，与 gold 多维覆盖对齐不足；`decision_contract` 多次提示 shallow。
- `state_contract` 在 business_rules 等类别上频繁未通过，解读时宜区分 **检查契约** 与 **业务语义**。
- checker 分与 overall_coverage 可能差异很大（例如 `payment_3ds_authentication_flow`）。summary 中某维覆盖为 0 而终稿表中出现具体边界值时，宜核对覆盖计算与 gold、`covered_item` 定义是否一致。
- **主实验 summary 更新后**，应 **同步重跑** `run_ablation.py` 与 `run_generalization.py`（并导出表），避免 ablation 与 generalization 引用 **不同次运行** 的结果。

## 需要许奕处理的事情

- 评估是否按 `category` 等对 **state_contract** 做分流或调整，减少规则题上的误读成本。（具体技术方案由 1 号定。）
- 核对覆盖类指标与 `outputs/final_tests/test/`、gold 规格的一致性（可从 `bank_transfer_rule_checker` 等样例入手）。
- 工作流类需求的 prompt / 后处理与 **repair** 判定；关注 `order_approval_state_machine`、`payment_3ds_authentication_flow` 上 `repaired: false` 的原因。
- 真实 **provider / model** 定稿后，统一重跑主实验并更新 `run_main_summary.json`，再重跑 ablation、generalization 及文档中的数字引用。

## 需要张洛梧写进文档的要点

- **主结果**：同时说明 **checker** 与 **gold 覆盖**；按 `generalization_by_category` 分三类撰写，并注明 **input_validation 仅 1 条、workflow_state 仅 3 条**，类均值不宜过度外推。
- **Ablation**：两臂覆盖不变条目较多、部分 `repaired` 与摘要指标不一致等，详见 **`member5_ablation_note_cn.md`**。
- **Limitation / Threat to validity**：可自 **`failure_analysis_cn.md`** 文末两节摘录或缩写。
