# Demo Handoff For Recorder

## 1. 这次你要录的不是 PPT

你录的是“工具演示视频”，不是答辩 PPT，也不是报告朗读。

这个视频的目标只有一句话：

`证明 ARG-Test 工具真的能运行，并且 final 项目的核心功能和最终证据都已经准备好了。`

所以录制逻辑应该是：

- 先跑工具
- 再看输出
- 最后展示正式结果和可执行证据

不要把它录成：

- 一边翻 PPT 一边念稿
- 或者一边讲理论一边不展示运行过程

## 2. 你需要准备什么

你只需要准备下面这些：

- 一个 PowerShell 终端
- 一个能打开文件和图片的桌面环境
- 跟着 `final_demo_script_cn.md` 或 `final_demo_script_en.md` 念
- 按 `run_demo_commands.ps1` 跑命令

不需要你自己改代码。  
不需要你自己想命令。  
不需要你自己找展示文件。  
这些我都已经在 package 里给你铺好了。

## 3. 你该按什么顺序做

### 第一步

先看：

- `final_demo_recording_checklist_cn.md`

它告诉你：

- 哪些文件提前打开
- 哪些话不能说错
- 如果时间不够该砍哪里

### 第二步

运行：

- `run_demo_commands.ps1`

这会自动完成三段演示：

- direct text input
- CSV batch input
- state-model extraction

### 第三步

打开下面三个 live 输出：

- `direct_text_demo_summary.json`
- `csv_order_workflow.md`
- `warehouse_pickup_order_workflow.md`

你不用把所有内容念出来，只要指出关键点：

- risk
- state model
- structured export

### 第四步

展示四张 final 图：

- `final_result_scorecard.png`
- `main_vs_baselines.png`
- `reproducibility_stability_overview.png`
- `coupon_module_evidence_scorecard.png`

## 4. 录制时最重要的几句话

这几句是你必须讲清楚的：

1. `For stable live interaction, we use mock mode in the demo.`
2. `The final project quality is represented by our frozen formal result bundle.`
3. `The system outputs not only test cases, but also risk metadata, state models, and structured exports.`
4. `The selected module is backed by executable black-box and white-box evidence.`

## 5. 你千万别做的事

- 不要临时切 live provider
- 不要边录边找文件
- 不要滚长 JSON 很久
- 不要把某个 markdown 表从头念到尾
- 不要自己临场编数字

## 6. 如果现场卡壳怎么办

如果命令已经跑完，但你不想再重复跑：

- 直接打开 `.local_runs/final_demo_mock` 里的现成输出继续讲

如果你讲英文不顺：

- 用 `final_demo_script_cn.md` 讲中文也可以

如果时间不够：

- 砍掉 CSV 部分的一半
- reproducibility 只保留一句结论

## 7. 最后的判断标准

你录完以后，自己检查这 5 件事：

- 视频里有没有真实运行命令
- 有没有展示 direct text / CSV / state-model 至少两种输入方式
- 有没有展示 structured output
- 有没有展示最终 baseline 比较图
- 有没有展示 detailed executable evidence

这 5 件事都有，这个 demo 就已经合格而且不差。
