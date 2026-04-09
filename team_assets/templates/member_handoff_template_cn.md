# 成员结果交接模板

## 成员编号 / 姓名

- 成员：4号
- 日期：2026-04-07
- 负责模块：Baseline 实验（mock/结构版准备）

## 本次完成内容

- 完成 `run_baselines.py` 在 `test + mock` 配置下的运行，确认 `rule_based / plain_llm / structured_no_checker` 三个 baseline 均可运行。
- 确认 baseline 输出字段统一，均包含 `test_count / duplicate_count / coverage / overall_coverage / checker_score`。
- 导出 baseline 对比表并完成中文结果说明文档（`baseline_notes_cn.md`）。

## 运行命令

```powershell
Set-Location 'D:\projects\ARG-Test'
python experiments\run_baselines.py --split test --provider mock --model mock-arg-test
python experiments\export_summary_tables.py --kind baseline --split test
```

## 正式输出文件路径

- `outputs/reports/test/baseline_summary.json`
- `outputs/reports/test/tables/baseline_summary_table.csv`
- `outputs/reports/test/tables/baseline_summary_table.md`
- `outputs/reports/test/baseline_notes_cn.md`

## 核心结果摘要（5 到 10 行）

- 本次 baseline 对比已完成，test 集共导出 30 行对比记录（10 个 requirement × 3 个 baseline）。
- 从 `overall_coverage` 均值看：`structured_no_checker`（约 0.303）最好，`rule_based`（约 0.295）次之，`plain_llm`（约 0.253）最弱。
- 指标解释上，本次以 `overall_coverage` 作为主指标，以 `checker_score` 作为辅助参考（`checker_score` 主要反映格式/规则符合度）。
- `plain_llm` 的主要问题是覆盖不充分，分区类与异常类覆盖经常为 0，导致总体覆盖偏低。
- `structured_no_checker` 相比 `plain_llm` 的主要增益是覆盖更完整，且平均 `test_count` 更高（约 4.1 vs 2.0）。
- `rule_based` 优势是稳定和可解释，局限是对复杂语义场景的覆盖提升有限。
- 当前结果为 mock/结构版阶段结果，可用于后续正式实验与文档框架搭建，不作为最终真实模型定版结论。

## 已知问题

- `checker_score` 与 `overall_coverage` 在部分 requirement 上存在不一致（例如 coverage 低但 checker_score 偏高），需要分开考虑。
- 多个 requirement 的 `exception_coverage` 仍为 0，后续若要强化结论，建议在正式阶段补充异常场景样例。

## 需要许奕处理的事情

- 正式阶段接入真实 provider/model 后，统一重跑 baseline 并确认与主流程、ablation 的口径一致。
- 若后续要新增统计项或调整 summary 字段，请由 1 号统一修改并同步给 4 号/5 号，避免比较口径漂移。

## 需要张洛梧写进文档的要点

- baseline 对比结论建议写为：`structured_no_checker` 在覆盖完整性上整体优于 `plain_llm`，`rule_based` 稳定但上限有限。
- 文档中应强调当前结果来自 mock/结构版准备阶段，最终正式结论以 1 号统一重跑后的正式结果为准。
