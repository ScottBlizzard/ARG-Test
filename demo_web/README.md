# ARG-Test Demo Web

This directory contains a minimal but formal frontend/backend shell for the final-project demo.

## Why this exists

The repository originally had a strong CLI pipeline but no UI layer.  
For the final defense, the demo teammate should not build a new system from scratch.  
Instead, they should polish this stable shell:

- backend: `FastAPI`
- frontend: static `HTML + CSS + JavaScript`
- core logic: existing `src.pipeline.ARGTestPipeline`

## What the UI already covers

- direct requirement-text analysis
- CSV batch import
- state-model extraction
- formal-result dashboard based on frozen official outputs
- figure gallery for the final presentation

The formal dashboard now prefers the tracked snapshot under:

- `report_assets/final_demo_package/frontend_focus/formal_results_snapshot/`

This avoids depending on ignored `.local_runs/` data for cloned teammates.

## Recommended teammate scope

The demo teammate should focus on:

1. visual polish
2. spacing, typography, and card hierarchy
3. smoother recording flow
4. small interaction refinements
5. stability checks before recording

They should not rewrite the generation pipeline or evaluation logic.

## Run locally

```powershell
cd D:\软件测试\Final\ARG-Test
python -m uvicorn demo_web.app:app --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000
```

Or run:

```powershell
powershell -ExecutionPolicy Bypass -File demo_web\run_demo_ui.ps1
```

## Demo policy

- For recorded interaction, prefer `provider=mock`.
- For final quality claims, use the frozen official results shown in the dashboard.
- Do not claim live provider determinism. Use the reproducibility card with the precise scripted explanation.
