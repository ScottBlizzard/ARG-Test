# Upgrade Pipeline Verification Summary

## Scope

This note records the verification evidence for the final-project upgrade itself, not just the `coupon_discount_engine` module.

## What was verified

### 1. Code-level upgrade completion

The following upgrade capabilities are now implemented in the repository:

- risk-aware requirement scoring and case prioritization
- run manifest export for `main / baseline / ablation / generalization / stability / repeatability`
- risk/category columns in summary tables
- repeatability runner for `3 independent reruns`
- upgraded unit/integration tests for the new pipeline logic

Key files:

- `src/risk.py`
- `src/schemas.py`
- `src/pipeline.py`
- `src/exporter.py`
- `src/utils.py`
- `experiments/run_main.py`
- `experiments/run_baselines.py`
- `experiments/run_ablation.py`
- `experiments/run_generalization.py`
- `experiments/run_stability_sanity.py`
- `experiments/run_repeatability.py`
- `experiments/export_summary_tables.py`

### 2. Automated tests

Commands used:

```powershell
python -m pytest tests -q
```

Result:

- `18 passed`

Test coverage of upgrade logic includes:

- risk assessment
- priority escalation
- mock pipeline export with `risk_assessment` and `run_context`

### 3. Full mock end-to-end validation

Commands used:

```powershell
python experiments\run_main.py --split test --provider mock --model mock-arg-test --candidates 3 --output-root .local_runs\upgrade_mock
python experiments\run_baselines.py --split test --provider mock --model mock-arg-test --output-root .local_runs\upgrade_mock
python experiments\run_ablation.py --split test --provider mock --model mock-arg-test --candidates 3 --output-root .local_runs\upgrade_mock
python experiments\run_generalization.py --split test --output-root .local_runs\upgrade_mock
python experiments\export_summary_tables.py --kind all --split test --output-root .local_runs\upgrade_mock
python experiments\run_repeatability.py --split test --provider mock --model mock-arg-test --candidates 3 --repeats 3 --output-root .local_runs\upgrade_mock_repeatability
```

Validated outputs:

- `.local_runs/upgrade_mock/outputs/reports/test/run_main_summary.json`
- `.local_runs/upgrade_mock/outputs/reports/test/run_main_manifest.json`
- `.local_runs/upgrade_mock/outputs/reports/test/baseline_summary.json`
- `.local_runs/upgrade_mock/outputs/reports/test/baseline_manifest.json`
- `.local_runs/upgrade_mock/outputs/reports/test/ablation_summary.json`
- `.local_runs/upgrade_mock/outputs/reports/test/ablation_manifest.json`
- `.local_runs/upgrade_mock/outputs/reports/test/generalization_by_category.json`
- `.local_runs/upgrade_mock/outputs/reports/test/generalization_manifest.json`
- `.local_runs/upgrade_mock/outputs/reports/test/tables/`
- `.local_runs/upgrade_mock_repeatability/outputs/reports/test/repeatability_summary.json`
- `.local_runs/upgrade_mock_repeatability/outputs/reports/test/repeatability_manifest.json`

Observed high-level results:

- `test` split coverage scope: `16/16 requirements`
- category summary:
  - `business_rules`: avg checker score `0.907`, avg overall coverage `0.175`
  - `input_validation`: avg checker score `0.950`, avg overall coverage `0.284`
  - `workflow_state`: avg checker score `0.930`, avg overall coverage `0.024`
- repeatability sanity on the deterministic mock stack: `16/16 stable`

Interpretation:

- the upgrade pipeline is structurally complete
- the new risk/manifest/table outputs are wired through the whole experiment chain
- `workflow_state` remains the weakest category and should be treated as a real limitation / improvement target in the final report

### 4. Live-provider smoke validation

Command used:

```powershell
python experiments\run_main.py --split test --ids coupon_discount_engine --provider openai --model qwen3.5-flash --candidates 3 --output-root .local_runs\formal_qwen_upgrade_smoke
```

Validated outputs:

- `.local_runs/formal_qwen_upgrade_smoke/outputs/reports/test/run_main_summary.json`
- `.local_runs/formal_qwen_upgrade_smoke/outputs/reports/test/run_main_manifest.json`

Observed result for `coupon_discount_engine`:

- checker score: `0.95`
- overall coverage: `0.517`
- risk level: `High`

Interpretation:

- the upgraded pipeline is not only mock-valid
- the online provider path also runs successfully with the new risk/manifest export flow

### 5. Offline upgrade of the frozen formal live runtime

Commands used:

```powershell
python experiments\upgrade_existing_runtime.py --runtime-root .local_runs\formal_qwen_novpn --split test --provider openai --model qwen3.5-flash --candidates 3 --enable-repair true
python experiments\upgrade_existing_runtime.py --runtime-root .local_runs\formal_qwen_novpn --split dev --provider openai --model qwen3.5-flash --candidates 3 --enable-repair true
python experiments\run_generalization.py --split test --output-root .local_runs\formal_qwen_novpn
python experiments\run_generalization.py --split dev --output-root .local_runs\formal_qwen_novpn
python experiments\export_summary_tables.py --kind all --split test --output-root .local_runs\formal_qwen_novpn
python experiments\export_summary_tables.py --kind all --split dev --output-root .local_runs\formal_qwen_novpn
```

Validated outputs:

- `.local_runs/formal_qwen_novpn/outputs/reports/test/run_main_summary.json`
- `.local_runs/formal_qwen_novpn/outputs/reports/test/run_main_manifest.json`
- `.local_runs/formal_qwen_novpn/outputs/reports/test/baseline_manifest.json`
- `.local_runs/formal_qwen_novpn/outputs/reports/test/ablation_manifest.json`
- `.local_runs/formal_qwen_novpn/outputs/reports/test/generalization_manifest.json`
- `.local_runs/formal_qwen_novpn/outputs/reports/test/tables/`
- `.local_runs/formal_qwen_novpn/outputs/reports/dev/run_main_manifest.json`
- `.local_runs/formal_qwen_novpn/outputs/reports/dev/generalization_manifest.json`
- `.local_runs/formal_qwen_novpn/outputs/reports/dev/tables/`

Observed formal live test-summary highlights:

- `test` split requirement count: `16`
- `business_rules` avg overall coverage: `0.577`
- `input_validation` avg overall coverage: `0.579`
- `workflow_state` avg overall coverage: `0.697`
- risk-aware category summaries are now exported together with the existing formal live results

Interpretation:

- the historical formal runtime no longer needs to stay “legacy”
- it has been upgraded into a citable final-result source with category/risk/manifest/table support

## Result-source caution

At repository root, the legacy path `outputs/reports/test/run_main_summary.json` still contains an outdated `10-case` snapshot and should not be used as the final evidence source.

Preferred formal source policy:

- upgraded historical formal live results: `.local_runs/formal_qwen_novpn/outputs/reports/`
- upgrade verification results: `.local_runs/upgrade_mock/...` and `.local_runs/formal_qwen_upgrade_smoke/...`

## Conclusion

The final-project upgrade has moved from planning into implementation:

- code upgrades are complete
- tests are passing
- full mock end-to-end verification is complete
- live-provider smoke verification is complete
- frozen formal live results have been upgraded offline and re-exported with manifests/tables

The remaining work is no longer “build the upgrade”, but “freeze the final evidence package and presentation materials”.
