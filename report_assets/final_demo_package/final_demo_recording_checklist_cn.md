# Final Demo Recording Checklist

## 1. 录制前准备

- 打开仓库根目录：`D:\软件测试\Final\ARG-Test`
- 把终端工作目录切到仓库根目录
- 终端窗口字号调大一点
- 提前把下面这些文件放到容易点开的地方
- 不要在录制时现场找路径

建议提前开好的资源：

- PowerShell 终端
- 文件管理器到 `.local_runs/final_demo_mock`
- 图片查看器或浏览器可打开 `report_assets/final_demo_package/figures/`

## 2. 录制时不要做的事

- 不要使用 live provider
- 不要现场改代码
- 不要在屏幕上滚太长的 JSON
- 不要展示太多原始 markdown 行
- 不要把无关目录都点开

## 3. 推荐录制顺序

1. 先说这次 demo 用 `mock` 做 live interaction，用 frozen formal results 展示最终质量
2. 运行 `run_demo_commands.ps1`
3. 打开 `direct_text_demo_summary.json`
4. 打开 `csv_order_workflow.md`
5. 打开 `warehouse_pickup_order_workflow.md`
6. 展示 `final_result_scorecard.png`
7. 展示 `main_vs_baselines.png`
8. 展示 `reproducibility_stability_overview.png`
9. 展示 `coupon_module_evidence_scorecard.png`
10. 结束

## 4. 录制时必须讲清楚的话

- live 部分用 `mock` 是为了稳定、快速、可重复
- final 质量看的是 frozen formal result
- 我们不是只输出 test list，还有 risk score、state model、structured export
- 详细模块还有 executable evidence

## 5. 容易说错的话

不要说：

- `we trained the model`
- `the rule-based baseline comes from a paper`
- `the live provider is fully deterministic`
- `checker score is the same as correctness`

## 6. 如果时间不够

优先保留：

1. live command run
2. direct-text summary
3. main_vs_baselines
4. coupon module evidence

可以缩短：

- CSV 结果展示时间
- reproducibility 讲解时间

## 7. 最佳录屏长度

- `4` 分钟左右最好
- 最长不要超过 `5` 分钟
