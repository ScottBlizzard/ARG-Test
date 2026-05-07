# Reproducibility Summary

## Seeded configuration

- `api_mode = chat_completions`
- `temperature = 0.0`
- `top_p = 1.0`
- candidate-level deterministic seed control enabled

## Mock evidence

Source:

- `.local_runs/repro_multi_seed_mock/outputs/reports/test/repeatability_summary.json`

Observed:

- `seed_schedule = [101, 202, 303]`
- `stable_case_count = 16/16`
- `avg_max_score_delta = 0.0`
- `avg_max_coverage_delta = 0.0`

Interpretation:

- repository-level deterministic chain is working
- manifests, candidate controls, and repeatability aggregation are wired correctly

## Live multi-seed evidence

Source:

- `.local_runs/repro_live_qwen_5case/outputs/reports/test/repeatability_summary.json`

Observed:

- `stable_case_count = 1/5`
- `avg_score_mean = 0.91`
- `avg_coverage_mean = 0.576`
- `avg_max_score_delta = 0.12`
- `avg_max_coverage_delta = 0.09`

Interpretation:

- live seeded experiments are supported
- current upstream endpoint still shows residual nondeterminism

## Live same-seed evidence

Source:

- `.local_runs/repro_live_same_seed_3case/outputs/reports/test/repeatability_summary.json`

Observed:

- `seed_schedule = [202601, 202601, 202601]`
- `stable_case_count = 0/3`

Interpretation:

- fixed-seed live determinism is not guaranteed by the current endpoint

## Archive-grade replay

Replay script:

- `experiments/replay_seeded_runtime.py`

Smoke output:

- `.local_runs/replay_mock_smoke/outputs/reports/test/run_main_summary.json`

Interpretation:

- the final submission can reproduce frozen seeded outputs from saved raw generations without calling the provider again
- this is the recommended final reproducibility mechanism for the archived project package
