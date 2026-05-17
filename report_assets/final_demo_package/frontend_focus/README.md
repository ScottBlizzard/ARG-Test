# Frontend Focus

如果你是负责 `demo UI / 前端展示` 的同学，**只看这个目录就够了**。  
上一级目录里的其他脚本和讲稿保留作归档参考，不是你当前最优先要看的材料。

## 1. 你现在真正要关心的文件

- 前端页面：`demo_web/static/index.html`
- 前端脚本：`demo_web/static/app.js`
- 前端样式：`demo_web/static/styles.css`
- 后端接口：`demo_web/app.py`
- 前端示例 CSV：`final_docs/execution_evidence/sample_requirement_batch.csv`
- 正式结果快照：`formal_results_snapshot/`

## 2. 前端页面必须分析和展示哪些数据

### 2.1 Direct Requirement Input

你需要关注：

1. `Checker Score`
2. `Overall Coverage`
3. `Selected Candidate`
4. `Risk Assessment`
5. `Generated Test Cases`
6. `Diagnostics`

注意：

- 如果当前输入没有对应 `gold spec`，覆盖率必须显示成 `N/A`，不能误导成 `0.0%`
- 页面默认示例已经换成 test split 里的真实 requirement，所以默认情况下应能看到有效 coverage

### 2.2 CSV Batch Import

你需要关注：

1. `Batch Size`
2. 每条 requirement 的 `Category`
3. 每条 requirement 的 `Checker`
4. 每条 requirement 的 `Coverage`
5. 每条 requirement 的 `Risk`

注意：

- CSV 示例现在也换成了正式测试集 requirement
- 如果别人上传的是 adhoc CSV，没有 gold spec，就应该显示 `N/A`

### 2.3 State-Model Extraction

你需要关注：

1. `States`
2. `Legal Transitions`
3. `Illegal Transitions`
4. `Coverage Plans`
5. 对应的 `Risk Assessment`

这里的重点不是 overall coverage，而是状态建模和迁移展示是否清楚。

### 2.4 Formal Evidence Dashboard

这是最重要的一块，因为它承接 final report 的正式结果。你要重点看：

1. `Tracked Formal Data Source`
2. `Official Test Requirements`
3. `Avg Checker Score`
4. `Avg Overall Coverage`
5. `Avg Test Count`
6. `Baseline Averages`
7. `Category Generalization`
8. `Reproducibility Snapshot`
9. `Recommended Cases`
10. `Figure Gallery`

## 3. 哪些数据是正式可引用的

正式展示和答辩时，优先引用这里的快照：

- `formal_results_snapshot/reports/test/run_main_summary.json`
- `formal_results_snapshot/reports/test/baseline_summary.json`
- `formal_results_snapshot/reports/test/generalization_by_category.json`
- `formal_results_snapshot/reports/test/ablation_summary.json`
- `formal_results_snapshot/repeatability/`

这些是专门为了前端演示和仓库追踪整理出来的版本，不依赖 `.local_runs`。

## 4. 你现在不需要关心什么

你现在不需要先看：

1. 旧的 CLI 录屏脚本
2. 旧的命令行讲稿
3. 归档式 asset map

除非你后面要录传统终端 demo，否则先别被这些文件干扰。

## 5. 你最终应该做什么

1. 把页面视觉再做顺一点
2. 检查默认示例能稳定跑出好看的结果
3. 确保 formal dashboard 读取的是这里的 tracked snapshot
4. 最后录一个以网页为主的 demo，而不是命令行为主的 demo
