# Evidence and Submission Checklist

## 1. Report evidence sources

正式文档引用原则：

- 优先使用已经冻结的正式 live 结果根目录，例如：`.local_runs/formal_qwen_novpn/outputs/reports/`
- 主实验结果：`<formal_root>/reports/dev/run_main_summary.json` 与 `<formal_root>/reports/test/run_main_summary.json`
- baseline：`<formal_root>/reports/test/baseline_summary.json`
- ablation：`<formal_root>/reports/test/ablation_summary.json`
- generalization：`<formal_root>/reports/test/generalization_by_category.json`
- case study raw evidence：`artifacts/raw_generations/`、`artifacts/parsed_traces/`、`artifacts/checker_logs/`、`outputs/final_tests/`

当前特别说明：

- 仓库根目录下的 `outputs/reports/test/run_main_summary.json` 仍是旧的 `10-case` 快照，不应继续作为 final 主引用源
- `.local_runs/upgrade_mock/...` 与 `.local_runs/formal_qwen_upgrade_smoke/...` 用于升级验证，不应直接充当 final 主实验数字来源

## 2. Non-citable sources

下面这些不应直接写进 final 报告主结论：

- terminal 临时输出
- dry-run 或明确标为 mock 的结果
- 未固化到仓库的手工统计
- 未经 final sign-off 的本地试跑结果

## 3. Final submission package checklist

### A. Project artifact

- source code
- prompts
- setup instructions / README
- video demonstration

### B. Risk analysis report

- risk model
- ranked risk table
- mitigation actions

### C. Test plan

- scope
- test items
- architecture
- high-level suite design
- schedule/checklist
- organization chart
- framework rationale
- cost estimation

### D. Detailed test design and execution

- selected module description
- black-box design
- white-box design
- execution evidence
- result analysis

## 4. Demo checklist

建议 demo 流程控制在 3 到 5 分钟：

1. 展示 requirement 输入
2. 展示五段式 trace 输出
3. 展示 checker / diagnostics
4. 展示 final test suite
5. 展示 summary table / figure
6. 若已补 white-box，则展示 pytest / coverage 结果

## 5. Presentation checklist

- first slide has team ID, names, student IDs
- all figures have source paths or can be traced to repo outputs
- main claims have a matching evidence file
- limitations are stated explicitly
- no slide relies on unverifiable numbers

## 6. Final consistency check

提交前应统一核对：

1. 报告中的数字是否与仓库正式结果一致
2. PPT 是否和报告使用同一版本结果
3. detailed module 名称是否在所有文档中一致
4. 所有路径和文件名是否真实存在
