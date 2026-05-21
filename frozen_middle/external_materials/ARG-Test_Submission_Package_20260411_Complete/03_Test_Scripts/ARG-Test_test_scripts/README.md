# ARG-Test

ARG-Test is a requirement-driven AI black-box testing project scaffold for the Software Testing assignment.

It follows the structure implied by the assignment, the project guide, and the reference paper:

- `Analysis -> Pattern -> Steps -> Verification -> FinalAnswer`
- technique-specific contract checking
- candidate reranking and lightweight repair
- deliverable-friendly artifacts, outputs, experiments, and report assets

## Default workflow

1. Put requirement documents in `data/requirements/`.
2. Run the pipeline in mock mode for local dry-runs.
3. Switch `ARG_TEST_PROVIDER` to a real LLM provider when you are ready.
4. Export raw traces, parsed traces, checker logs, and final test cases.
5. Evaluate generated suites against `data/gold_specs/`.

## Repository layout

```text
ARG-Test/
??? data/
?   ??? requirements/
?   ??? gold_specs/
?   ??? mutants/
??? prompts/
??? src/
?   ??? baselines/
?   ??? checker/
?   ??? evaluation/
??? team_assets/
??? artifacts/
??? outputs/
??? experiments/
??? report_assets/
```

## Quick start

```powershell
cd <repo-root>
python -m src.main batch --split dev --provider mock --candidates 3
python experiments/run_baselines.py --split test
python experiments/run_ablation.py --split test
```

## Formal run workflow

Use `.env` or explicit CLI flags for the real provider. The repository loads `.env` automatically from the project root.

Recommended pattern for official runs:

```powershell
Copy-Item .env.example .env
python experiments/check_runtime_ready.py --provider openai --model <your-model> --output-root .local_runs/formal_openai
powershell -ExecutionPolicy Bypass -File experiments/run_formal_workflow.ps1 -Provider openai -Model <your-model> -OutputRoot .local_runs/formal_openai
```

This keeps official artifacts outside tracked `artifacts/` and `outputs/` by writing them into `.local_runs/`.

If you only want a local smoke run without touching tracked outputs:

```powershell
python experiments/run_main.py --split test --provider mock --model mock-arg-test --candidates 3 --output-root .local_runs/smoke_test
python experiments/run_baselines.py --split test --provider mock --model mock-arg-test --output-root .local_runs/smoke_test
python experiments/run_ablation.py --split test --provider mock --model mock-arg-test --candidates 3 --output-root .local_runs/smoke_test
python experiments/run_generalization.py --split test --output-root .local_runs/smoke_test
python experiments/export_summary_tables.py --kind all --split test --output-root .local_runs/smoke_test
```

## Targeted rerun

If the first formal run finishes and only a few requirements need improvement, rerun those requirement IDs without overwriting the entire main summary:

```powershell
python experiments/run_main.py --split test --provider openai --model qwen3.5-flash --ids address_international_format_validation,payment_3ds_authentication_flow,payment_card_expiry_and_cvv_validation --output-root .local_runs/formal_qwen_novpn
python experiments/run_ablation.py --split test --provider openai --model qwen3.5-flash --output-root .local_runs/formal_qwen_novpn
python experiments/export_summary_tables.py --kind all --split test --output-root .local_runs/formal_qwen_novpn
```

`run_ablation.py` now reuses `run_main_summary.json` by default so ablation comparisons stay aligned with the official main run and do not spend extra API calls rerunning the full pipeline.

## Team workflow

Current named owners:

- `1? / ??`: integration, prompts, parser, checker, final run
- `2? / ???`: proposal, report, PPT, presentation assets
- `3?`: data assets and main experiments
- `4?`: baselines
- `5?`: evaluation, ablation, failure analysis

Important team docs:

- overall task split: `report_assets/team_task_allocation_cn.md`
- experiment-member runbooks: `team_assets/`
- official result sources for documentation: `team_assets/official_result_sources_cn.md`
- member handoff and issue templates: `team_assets/templates/`

## Validation and export helpers

Data validation:

```powershell
python experiments/validate_data_assets.py --split all
```

Export summary tables for docs:

```powershell
python experiments/export_summary_tables.py --kind all --split test
```

Group main results by requirement category:

```powershell
python experiments/run_generalization.py --split test
```

## Environment

Copy `.env.example` to `.env` if you want to use environment variables.

Important defaults:

- `ARG_TEST_PROVIDER=mock`
- `ARG_TEST_MODEL=mock-arg-test`
- `ARG_TEST_CANDIDATES=3`
- `ARG_TEST_ENABLE_REPAIR=true`
- `ARG_TEST_OUTPUT_ROOT=` writes into repo-local `artifacts/` and `outputs/`
- `ARG_TEST_OUTPUT_ROOT=.local_runs/formal_openai` keeps formal outputs out of tracked directories

## Deliverable mapping

- prompts and model config: `prompts/`, `.env.example`
- model-generated raw artifacts: `artifacts/raw_generations/`
- parsed traces and checker logs: `artifacts/parsed_traces/`, `artifacts/checker_logs/`
- final test cases and reports: `outputs/final_tests/`, `outputs/reports/`
- experimental scripts: `experiments/`
- report and PPT outlines: `report_assets/`
- team collaboration assets: `team_assets/`

## Notes

- The default `mock` provider is for local scaffolding and parser/checker verification.
- Real evaluation should use an actual LLM through `src/llm_client.py`.
- Gold specs are for evaluation only. Do not feed them into the real generation pipeline.
- `prompts/system_prompt.txt` is prepended to generation, baseline, and repair prompts.
