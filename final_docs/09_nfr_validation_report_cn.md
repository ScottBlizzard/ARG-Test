# Non-Functional Requirements Validation Report

日期：`2026-05-07`

本报告对应课程作业中 `1.1.2 Non-Functional Requirements` 的正式化补充，覆盖：

- Performance
- Usability
- Security
- Maintainability

核心证据来源：

- [nfr_validation_summary.md](/D:/软件测试/Final/ARG-Test/final_docs/execution_evidence/nfr_validation_summary.md:1)
- [nfr_validation_summary.json](/D:/软件测试/Final/ARG-Test/final_docs/execution_evidence/nfr_validation_summary.json:1)

## 1. Performance

采用 mock provider 对 `test` split 的 5 条 requirement 做本地基准检查。

结果：

- sample size = `5`
- average mock processing time per requirement = `0.005 s`

结论：

- 对课程项目规模而言，当前本地流程性能充足
- 真正的时间成本主要来自在线模型调用，而不是本地 parser/checker/exporter

## 2. Usability

当前 CLI 已支持：

- `run`
- `run-text`
- `batch`
- `batch-csv`
- `state-model`

这意味着输入形式已经覆盖：

- plain text file
- direct text input
- CSV batch input

同时 README 已补充：

- quick start
- formal run workflow
- direct text input example
- CSV input example
- state-model example

结论：

- 与课程要求相比，输入与使用路径已经比最低要求更完整

## 3. Security

本次检查重点不做“高强度安全测试”，而是做课程项目层面的最关键控制：

- secrets 通过 `.env` / environment variable 注入
- run manifest 记录 provider/model，但不记录 API key
- 对 `outputs / artifacts / final_docs / formal reports` 做 secret leak scan

结果：

- secret leak found = `false`
- manifests record provider metadata without API key disclosure = `true`

结论：

- 当前仓库在课程项目范围内满足基本安全性要求
- 后续最终提交时仍应避免把 `.env` 或 token 截图放入提交包

## 4. Maintainability

当前可维护性证据：

- `src/` Python modules = `27`
- experiment scripts = `14`
- automated test files = `5`
- automated test cases = `23`
- current pytest summary = `23 passed in 0.19s`
- runtime output isolation supported = `true`

其中最重要的可维护性设计包括：

- `src/ / experiments/ / tests/ / final_docs/ / frozen_middle/` 分层明确
- `.local_runs/` 用于隔离正式运行结果
- `run_manifest` / `baseline_manifest` / `ablation_manifest` / `generalization_manifest` / `repeatability_manifest` 保证结果可追踪

结论：

- 当前仓库已经具备清晰的结构化维护基础
- 对课程 final 而言，可维护性不再是短板

## 5. 总结

本次 NFR formalization 的核心成果不是“写了几段说明”，而是：

1. 把 usability 落成了真实 CLI 能力
2. 把 performance/security/maintainability 落成了可复核证据
3. 让 NFR 不再只是作业说明里的空标题

因此，`NFR` 这一项现在可以视为已从“未成型”升级为“有独立证据支撑的正式部分”。
