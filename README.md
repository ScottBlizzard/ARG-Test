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
├── data/
│   ├── requirements/
│   ├── gold_specs/
│   └── mutants/
├── prompts/
├── src/
│   ├── baselines/
│   ├── checker/
│   └── evaluation/
├── team_assets/
├── artifacts/
├── outputs/
├── experiments/
└── report_assets/
```

## Quick start

```powershell
cd d:\软件测试\ARG-Test
python -m src.main batch --split dev --provider mock --candidates 3
python experiments\run_baselines.py --split test
python experiments\run_ablation.py --split test
```

## Team workflow

Current named owners:

- `1号 / 许奕`: integration, prompts, parser, checker, final run
- `2号 / 张洛梧`: proposal, report, PPT, presentation assets
- `3号`: data assets and main experiments
- `4号`: baselines
- `5号`: evaluation, ablation, failure analysis

Important team docs:

- overall task split: `report_assets/team_task_allocation_cn.md`
- experiment-member runbooks: `team_assets/`
- official result sources for documentation: `team_assets/official_result_sources_cn.md`
- member handoff and issue templates: `team_assets/templates/`

One-click workflows for members 3/4/5:

```powershell
powershell -ExecutionPolicy Bypass -File experiments\run_role3_main_workflow.ps1
powershell -ExecutionPolicy Bypass -File experiments\run_role4_baseline_workflow.ps1
powershell -ExecutionPolicy Bypass -File experiments\run_role5_eval_workflow.ps1
```

## Validation and export helpers

Data validation:

```powershell
python experiments\validate_data_assets.py --split all
```

Export summary tables for docs:

```powershell
python experiments\export_summary_tables.py --kind all --split test
```

Group main results by requirement category:

```powershell
python experiments\run_generalization.py --split test
```

## Environment

Copy `.env.example` to `.env` if you want to use environment variables.

Important defaults:

- `ARG_TEST_PROVIDER=mock`
- `ARG_TEST_MODEL=mock-arg-test`
- `ARG_TEST_CANDIDATES=3`
- `ARG_TEST_ENABLE_REPAIR=true`

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
