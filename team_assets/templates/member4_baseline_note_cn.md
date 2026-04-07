# 4 号 Baseline 结果说明模板

## 本次运行配置

- provider: mock
- model: mock-arg-test
- split: test
- 日期: 2026-04-07

## 正式输出文件

- `outputs/reports/test/baseline_summary.json`
- `outputs/reports/test/tables/baseline_summary_table.csv`
- `outputs/reports/test/tables/baseline_summary_table.md`

## Baseline 对比摘要

- 最弱 baseline: `plain_llm`（平均 `overall_coverage` 约 0.253，低于 `rule_based` 约 0.295 和 `structured_no_checker` 约 0.303）。
- plain LLM 的主要问题: 分区类与异常类覆盖不足，`valid_partition_coverage`、`invalid_partition_coverage`、`exception_coverage` 在多数 requirement 上为 0，且平均 `test_count` 仅约 2.0。
- structured-no-checker 的主要优势: 覆盖完整性更好，平均 `overall_coverage` 最高（约 0.303），并能在多个 requirement 上补齐 plain LLM 漏掉的覆盖点，平均 `test_count` 约 4.1。
- rule-based 的主要优势: 稳定、可解释，在规则清晰 requirement 上表现稳健，平均 `overall_coverage` 约 0.295。
- rule-based 的主要局限: 灵活性较弱，面对复杂语义或跨场景需求时覆盖提升有限，整体上限不如 `structured_no_checker`。

## 按 requirement 的观察

### requirement 1
- requirement ID: `coupon_discount_engine`
- 哪个 baseline 最好: `structured_no_checker`
- 原因: 该 requirement 下 `structured_no_checker` 的 `overall_coverage` 为 0.571，高于 `rule_based` 的 0.500 和 `plain_llm` 的 0.286；同时 `decision_rule_coverage` 达到 0.75，覆盖更完整。

### requirement 2
- requirement ID: `payment_3ds_authentication_flow`
- 哪个 baseline 最差: `plain_llm`
- 原因: 该 requirement 下 `plain_llm` 的 `overall_coverage` 为 0.0，而 `rule_based` 与 `structured_no_checker` 均为 0.071，说明 plain LLM 在该状态流转类需求上覆盖明显不足。

## 可以写进报告的结论句

- 在 test 集 baseline 对比中，`structured_no_checker` 的平均 `overall_coverage` 最高，`plain_llm` 最低。
- `plain_llm` 的主要短板是分区类与异常类覆盖不足，导致整体覆盖率偏低且稳定性较差。
- `rule_based` 在可解释性和稳定性上有优势，但覆盖上限低于 `structured_no_checker`。
