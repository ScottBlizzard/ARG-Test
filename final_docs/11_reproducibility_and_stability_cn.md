# Reproducibility And Stability Status

## 1. 目标

这轮升级的目标不是只把项目写成“支持 seed”，而是把 final 项目的复现实验链路做完整：

- 显式记录 `api_mode / seed / temperature / top_p`
- 支持固定 seed 与多 seed 的 repeatability 运行
- 支持从已保存 raw generations 离线重建正式结果
- 给 final 报告提供可以直接引用的证据路径

## 2. 已完成的工程升级

代码层已补齐以下能力：

- `chat_completions + seed` 路径：
  - `src/llm_client.py`
- 显式运行配置：
  - `src/config.py`
  - `src/utils.py`
- seed-aware candidate control 与 deterministic candidate profiles：
  - `src/pipeline.py`
- 更强的 deterministic local repair：
  - `src/repair.py`
- 多 seed repeatability：
  - `experiments/run_repeatability.py`
- frozen raw-generation replay：
  - `experiments/replay_seeded_runtime.py`
- formal workflow 脚本已支持显式 reproducibility 参数：
  - `experiments/run_formal_workflow.ps1`

## 3. 当前证据

### 3.1 Mock reproducibility

以下证据表明仓库本身的 deterministic chain 已经成立：

- `.local_runs/repro_mock_main/outputs/reports/test/run_main_summary.json`
- `.local_runs/repro_multi_seed_mock/outputs/reports/test/repeatability_summary.json`

结果：

- `seed_schedule = [101, 202, 303]`
- `stable_case_count = 16/16`
- `avg_max_score_delta = 0.0`
- `avg_max_coverage_delta = 0.0`

这说明：

- 配置记录、candidate control、manifest、repeatability runner 都是通的
- 在 deterministic mock stack 上，3-seed replay behavior 是完全稳定的

### 3.2 Live seeded smoke

真实 provider 的 seeded chat-completions smoke 已打通：

- `.local_runs/repro_live_smoke/outputs/reports/test/coupon_discount_engine_summary.json`

该结果已经包含：

- `api_mode = chat_completions`
- `temperature = 0.0`
- `top_p = 1.0`
- candidate-level applied seed
- provider response id

### 3.3 Live 3-seed stability sample

代表性 5-case live multi-seed evidence：

- `.local_runs/repro_live_qwen_5case/outputs/reports/test/repeatability_summary.json`

当前结果：

- `seed_schedule = [101, 202, 303]`
- `stable_case_count = 1/5`
- `avg_score_mean = 0.91`
- `avg_coverage_mean = 0.576`
- `avg_max_score_delta = 0.12`
- `avg_max_coverage_delta = 0.09`

### 3.4 Live same-seed repeatability sample

固定同一 seed 的 3-case live repeatability evidence：

- `.local_runs/repro_live_same_seed_3case/outputs/reports/test/repeatability_summary.json`

当前结果：

- `seed_schedule = [202601, 202601, 202601]`
- `stable_case_count = 0/3`

## 4. 结论

需要把“可复现”拆成两层看：

### 4.1 仓库级/提交包级 reproducibility

这一层现在已经成立。

原因：

- 所有 seeded runs 都会保存 raw generations 和 metadata
- `experiments/replay_seeded_runtime.py` 可以基于 frozen raw generations 离线重建结果
- 这意味着 final submission 可以做到 archive-grade reproducibility

也就是说：

- 只要 final 提交包里包含 frozen raw generations
- 不依赖再次请求远端模型
- 也能把正式结果 deterministically replay 出来

### 4.2 上游 live provider 的 strict determinism

这一层目前**不能诚实地宣称已经完全实现**。

现有 live evidence 表明：

- 即使使用 `chat_completions + seed + temperature=0.0 + top_p=1.0`
- 当前 OpenAI-compatible endpoint 仍然存在可见波动

因此 final 报告里最稳妥、最技术上正确的写法应该是：

- 我们实现了 `seed-controlled experimental pipeline`
- 我们提供了 `3-seed repeatability evidence`
- 我们提供了 `raw-generation replay`，保证 submission-level full reproducibility
- 同时如实说明：upstream provider still shows residual nondeterminism in live reruns

## 5. 推荐答辩口径

不要说：

- `the live model is perfectly deterministic`
- `3 seeds all produce identical live results`

建议说：

- `We upgraded the project to a seed-controlled experimental pipeline.`
- `We record api_mode, seed, temperature, and top_p in every manifest.`
- `We support 3-seed repeatability studies and archive-grade replay from frozen raw generations.`
- `Live reruns still show residual provider-side nondeterminism, so the final submission uses frozen seeded artifacts plus deterministic replay as the official reproducibility mechanism.`

## 6. 后续建议

如果还想继续冲“更高 live stability”，可以继续做两件事：

1. 进一步增强 deterministic post-processing / canonicalization，让最终测试套件更受 requirement 驱动，而不是受模型表述波动驱动。
2. 如果允许切换 provider，优先选择对 `seed` 与 deterministic decoding 支持更稳定的 endpoint，再跑完整 3-seed full test study。
