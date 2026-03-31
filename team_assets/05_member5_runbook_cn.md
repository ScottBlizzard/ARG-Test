# 5 号 Runbook：评测、消融、错误分析负责人

你的联系人：

- 技术接口和 bug：许奕
- 文档结果需求：张洛梧

## 当前阶段目标

你当前只负责完成“mock/结构版准备阶段”，不负责最终正式评测结论。

你的阶段目标是：

- 把 `metrics / ablation / generalization / failure analysis` 框架搭好；
- 验证评测脚本、消融脚本、表格导出脚本可执行；
- 固定结果分析的模板和口径；
- 把需要许奕后续正式重跑的点整理清楚。

## 结束条件

当你完成下面三件事后，你这一阶段就结束：

1. runbook 中列出的任务都完成；
2. 交接模板已经填写并交给许奕和张洛梧；
3. 消融、generalization、failure analysis 所需的脚本和模板都已经定型。

后续真实模型下的正式 ablation / generalization 重跑和最终结果定版，统一由许奕接管。

## 你只能重点修改的目录

- `src/evaluation/`
- `experiments/run_ablation.py`
- 必要时新增 `experiments/run_generalization.py`

## 前置依赖

你要完成全部任务，必须先拿到 3 号产出的主实验结果：

- `outputs/reports/test/run_main_summary.json`

如果这个文件还没有，不代表你不能开始工作；你可以先做 metrics 和 ablation 脚本，但 `generalization` 和部分 failure analysis 要等 3 号先交付主实验结果。

## 你开始工作的标准顺序

### 第一步：先看 requirement 分类清单

看：

- `data/requirements/manifest.json`

因为你后面做 requirement-type/generalization 分析要按这个清单分组。

### 第二步：先跑消融实验

```powershell
Set-Location 'd:\软件测试\ARG-Test'
python experiments\run_ablation.py --split test --provider mock --model mock-arg-test --candidates 3
```

### 第三步：导出 ablation 表格

```powershell
Set-Location 'd:\软件测试\ARG-Test'
python experiments\export_summary_tables.py --kind ablation --split test
```

### 第四步：跑 category/generalization 分析

```powershell
Set-Location 'd:\软件测试\ARG-Test'
python experiments\run_generalization.py --split test
python experiments\export_summary_tables.py --kind generalization --split test
```

### 第五步：整理 failure analysis

你需要从以下目录选典型案例：

- `artifacts/raw_generations/test/`
- `artifacts/parsed_traces/test/`
- `artifacts/checker_logs/test/`
- `outputs/final_tests/test/`

你至少要总结：

- 3 类以上失败模式
- 每类给 1 到 2 个 requirement 示例
- 解释失败原因
- 说明它更像数据问题、模型问题还是 checker 问题

建议写到：

- `outputs/reports/test/failure_analysis_cn.md`

## 你最终必须交付的文件

- `outputs/reports/test/ablation_summary.json`
- `outputs/reports/test/tables/ablation_summary_table.csv`
- `outputs/reports/test/tables/ablation_summary_table.md`
- `outputs/reports/test/generalization_by_category.json`
- `outputs/reports/test/tables/generalization_by_category.csv`
- `outputs/reports/test/failure_analysis_cn.md`
- 一份你填写过的交接文档：`team_assets/templates/member_handoff_template_cn.md`

## 你必须额外提供给张洛梧的文字素材

- 一段主结果解释
- 一段 ablation 解释
- 一段 limitation 说明
- 一段 threat to validity 说明
