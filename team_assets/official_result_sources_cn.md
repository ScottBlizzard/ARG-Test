# 官方结果来源说明

本文件用于告诉全组：哪些结果文件可以被张洛梧直接拿去写文档，哪些只是中间产物。

## 一、主实验正式结果

正式来源：

- `outputs/reports/dev/run_main_summary.json`
- `outputs/reports/test/run_main_summary.json`

辅助表格来源：

- `outputs/reports/dev/tables/main_summary_table.csv`
- `outputs/reports/dev/tables/main_summary_table.md`
- `outputs/reports/test/tables/main_summary_table.csv`
- `outputs/reports/test/tables/main_summary_table.md`

说明：

- 3 号跑完主实验后，先检查 `run_main_summary.json`。
- 如果要给 2 号和 1 号交结果，优先交 `run_main_summary.json` 和 `tables/main_summary_table.*`。

## 二、Baseline 正式结果

正式来源：

- `outputs/reports/test/baseline_summary.json`

辅助表格来源：

- `outputs/reports/test/tables/baseline_summary_table.csv`
- `outputs/reports/test/tables/baseline_summary_table.md`

说明：

- 4 号所有对比结论必须以 `baseline_summary.json` 为主。

## 三、Ablation 正式结果

正式来源：

- `outputs/reports/test/ablation_summary.json`

辅助表格来源：

- `outputs/reports/test/tables/ablation_summary_table.csv`
- `outputs/reports/test/tables/ablation_summary_table.md`

说明：

- 5 号所有消融实验分析必须以 `ablation_summary.json` 为主。

## 四、Generalization / Requirement-Type 分析

正式来源：

- `outputs/reports/test/generalization_by_category.json`

辅助表格来源：

- `outputs/reports/test/tables/generalization_by_category.csv`
- `outputs/reports/test/tables/generalization_by_category.md`

## 五、案例分析原始来源

如需展示具体 requirement 的生成样例，统一使用：

- 原始候选：`artifacts/raw_generations/<split>/`
- 解析后结构：`artifacts/parsed_traces/<split>/`
- checker 日志：`artifacts/checker_logs/<split>/`
- 最终测试用例：`outputs/final_tests/<split>/`

## 六、禁止引用的非正式来源

下面这些不能直接写进报告：

- 终端临时输出截图
- `mock` 运行结果（除非明确说是 dry-run）
- 组员本地手工统计但未落盘的数字
- 未经 1 号确认的临时实验结果
