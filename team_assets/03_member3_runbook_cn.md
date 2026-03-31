# 3 号 Runbook：数据集与主实验负责人

你的联系人：

- 技术接口和 bug：许奕
- 文档结果需求：张洛梧

## 当前阶段目标

你当前只负责完成“mock/结构版准备阶段”，不负责最终正式实验结果。

你的阶段目标是：

- 把 `data/requirements/` 和 `data/gold_specs/` 做扎实；
- 验证主实验流程在当前仓库里能跑通；
- 产出稳定、统一、可交接的主实验结果格式；
- 把问题和已知风险整理给许奕。

## 结束条件

当你完成下面三件事后，你这一阶段就结束：

1. runbook 中列出的任务都完成；
2. 交接模板已经填写并交给许奕和张洛梧；
3. 你负责的正式输出文件已经落盘并路径清楚。

后续真实模型接入、正式主实验重跑、最终结果定版，统一由许奕接管。

## 你只能重点修改的目录

- `data/requirements/dev/`
- `data/requirements/test/`
- `data/gold_specs/dev/`
- `data/gold_specs/test/`

## 你开始工作的标准顺序

### 第一步：验证数据资产是否规范

先运行：

```powershell
Set-Location 'd:\软件测试\ARG-Test'
python experiments\validate_data_assets.py --split all
```

你要检查输出：

- 有没有 requirement 缺 `Requirement ID`
- 有没有 gold spec 缺字段
- requirement 文件名和 gold spec 文件名是否匹配
- 同一个 split 下 requirement ID 是否重复

如果这里报错，不要跳过，先修好再跑主实验。

### 第二步：检查 requirement 清单和类别

看：

- `data/requirements/manifest.json`

你要确认：

- split 是否正确
- category 是否合理
- requirement 描述是否足够清晰

如果你新增 requirement，也必须同步更新 `manifest.json`。

### 第三步：跑主实验

先用 dry-run 或 mock 检查：

```powershell
Set-Location 'd:\软件测试\ARG-Test'
python experiments\run_main.py --split dev --provider mock --model mock-arg-test --candidates 3
python experiments\run_main.py --split test --provider mock --model mock-arg-test --candidates 3
```

### 第四步：导出主实验表格

```powershell
Set-Location 'd:\软件测试\ARG-Test'
python experiments\export_summary_tables.py --kind main --split dev
python experiments\export_summary_tables.py --kind main --split test
```

### 第五步：整理交付物

你最后交给许奕和张洛梧的至少包括：

- `outputs/reports/dev/run_main_summary.json`
- `outputs/reports/test/run_main_summary.json`
- `outputs/reports/dev/tables/main_summary_table.csv`
- `outputs/reports/test/tables/main_summary_table.csv`
- 一份你填写过的交接文档：`team_assets/templates/member_handoff_template_cn.md`

## 你必须完成的检查项

- 每个 requirement 都有对应 gold spec
- 每个 gold spec 都包含必需字段
- 主实验结果里没有 requirement 缺失
- 如果有明显异常 requirement，要单独列出来
- 至少挑 2 个成功样例和 2 个失败样例给张洛梧

## 你遇到问题时怎么报

如果发现问题，不要直接改核心代码，按这个格式发给许奕：

- requirement ID
- split
- 命令
- 输出文件路径
- 问题现象
- 你认为属于数据问题还是 pipeline 问题

模板直接用：

- `team_assets/templates/issue_report_template_cn.md`
