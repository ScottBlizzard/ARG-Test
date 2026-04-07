# Baseline 结果说明（4号）

## 本次运行配置

- provider: mock
- model: mock-arg-test
- split: test
- 数据来源：
  - `outputs/reports/test/baseline_summary.json`
  - `outputs/reports/test/tables/baseline_summary_table.csv`
  - `outputs/reports/test/tables/baseline_summary_table.md`

## Baseline 对比摘要

- 最弱 baseline：`plain_llm`。  
  从 `overall_coverage` 看，`plain_llm` 平均约为 **0.253**，低于 `rule_based`（约 **0.295**）和 `structured_no_checker`（约 **0.303**）。

- plain LLM 最常见失败：  
  主要是覆盖不全，尤其在 `valid_partition_coverage`、`invalid_partition_coverage`、`exception_coverage` 上经常为 0；另外在不少 requirement 上 `boundary_coverage` 和 `decision_rule_coverage` 也偏低，导致总体覆盖率不稳定。

- structured-no-checker 相比 plain LLM 的增益：  
  整体覆盖率更高（`overall_coverage` 均值更高），并且在多个 requirement 上能补齐 plain LLM 漏掉的分区/规则类覆盖点；同时 `test_count` 更高（平均约 4.1 vs 2.0），说明其生成用例更充分。

- rule-based 的优势和局限：  
  优势是结果稳定、可解释性强，在规则明确的 requirement 上表现稳健；局限是灵活性不足，遇到复杂语义或跨场景变化时覆盖提升有限，整体上限不如 `structured_no_checker`。

## 给 1 号与 2 号可直接引用的结论句

- 在 test 集 baseline 对比中，`structured_no_checker` 的平均 `overall_coverage` 最好（约 0.303），`plain_llm` 最弱（约 0.253）。
- `plain_llm` 的主要短板是分区类与异常类覆盖不足，导致总体覆盖率偏低且不稳定。
- `rule_based` 具备稳定和可解释优势，但在复杂 requirement 上存在覆盖上限；`structured_no_checker` 在覆盖完整性上更有优势。
