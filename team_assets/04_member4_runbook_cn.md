# 4 号 Runbook：Baseline 实验负责人

你的联系人：

- 技术接口和 bug：许奕
- 文档结果需求：张洛梧

## 当前阶段目标

你当前只负责完成“mock/结构版准备阶段”，不负责最终正式 baseline 结果。

你的阶段目标是：

- 把三个 baseline 的逻辑和输出格式固定下来；
- 验证 baseline 脚本能稳定运行；
- 产出统一可比较的 baseline summary 结构；
- 把结论模板和已知问题整理给许奕。

## 结束条件

当你完成下面三件事后，你这一阶段就结束：

1. runbook 中列出的任务都完成；
2. 交接模板已经填写并交给许奕和张洛梧；
3. baseline 的输出文件和说明文档都已经落盘。

后续真实模型下的正式 baseline 重跑和最终定版，统一由许奕接管。

## 你只能重点修改的目录

- `src/baselines/`
- `experiments/run_baselines.py`

## 你开始工作的标准顺序

### 第一步：检查 baseline 是否都能跑

```powershell
Set-Location 'd:\软件测试\ARG-Test'
python experiments\run_baselines.py --split test --provider mock --model mock-arg-test
```

你要确认三种 baseline 都存在：

- `rule_based`
- `plain_llm`
- `structured_no_checker`

### 第二步：检查输出结构是否统一

你的重点不是让 baseline 更复杂，而是让输出统一可比较。

你必须保证每个 baseline 都能稳定产出：

- `test_count`
- `duplicate_count`
- `coverage`
- `overall_coverage`
- `checker_score`

### 第三步：导出 baseline 对比表

```powershell
Set-Location 'd:\软件测试\ARG-Test'
python experiments\export_summary_tables.py --kind baseline --split test
```

### 第四步：写 baseline 结论

你最后必须提供中文分析，不少于以下四点：

- 哪个 baseline 最弱
- plain LLM 最常见失败是什么
- structured-no-checker 相比 plain LLM 的增益是什么
- rule-based 的优势和局限是什么

建议把说明写到：

- `outputs/reports/test/baseline_notes_cn.md`

## 你最终必须交付的文件

- `outputs/reports/test/baseline_summary.json`
- `outputs/reports/test/tables/baseline_summary_table.csv`
- `outputs/reports/test/tables/baseline_summary_table.md`
- `outputs/reports/test/baseline_notes_cn.md`
- 一份你填写过的交接文档：`team_assets/templates/member_handoff_template_cn.md`

## 你遇到问题时怎么处理

如果 baseline 输出字段不统一、无法比较，先不要动 `pipeline.py`，先把问题记下来发给许奕。

如果你想加新 baseline，也先发给许奕确认，避免最后比较口径不一致。
