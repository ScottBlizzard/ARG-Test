from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.input_loader import load_requirements_from_csv
from src.pipeline import ARGTestPipeline

BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = Path(__file__).resolve().parent / "static"
FIGURES_DIR = BASE_DIR / "report_assets" / "figures"
FORMAL_REPORT_DIR = BASE_DIR / ".local_runs" / "formal_qwen_novpn" / "outputs" / "reports" / "test"
SAMPLE_CSV_PATH = BASE_DIR / "final_docs" / "execution_evidence" / "sample_requirement_batch.csv"
WEB_RUNS_ROOT = BASE_DIR / ".local_runs" / "web_demo_sessions"
DEFAULT_PROVIDER = "mock"
DEFAULT_MODEL = "mock-arg-test"
DEFAULT_CANDIDATES = 3
DEFAULT_API_MODE = "chat_completions"
DEFAULT_SEED = 202601
DEFAULT_TEMPERATURE = 0.0
DEFAULT_TOP_P = 1.0

app = FastAPI(
    title="ARG-Test Demo Web UI",
    summary="A stable frontend/backend demo shell for the course final project.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/demo-assets/figures", StaticFiles(directory=FIGURES_DIR), name="demo-figures")


class AnalyzeTextRequest(BaseModel):
    requirement_text: str = Field(min_length=1)
    requirement_id: str | None = None
    split: str = "adhoc"
    provider: str = DEFAULT_PROVIDER
    model: str = DEFAULT_MODEL
    candidates: int = Field(default=DEFAULT_CANDIDATES, ge=1, le=5)
    api_mode: str = DEFAULT_API_MODE
    seed: int | None = DEFAULT_SEED
    temperature: float | None = DEFAULT_TEMPERATURE
    top_p: float | None = DEFAULT_TOP_P


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _mean(values: list[float]) -> float:
    return round(mean(values), 3) if values else 0.0


def _relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(BASE_DIR))
    except ValueError:
        return str(path.resolve())


def _build_session_root(prefix: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    session_root = WEB_RUNS_ROOT / f"{prefix}_{stamp}"
    session_root.mkdir(parents=True, exist_ok=True)
    return session_root


def _ensure_provider_ready(provider: str) -> None:
    if provider != "mock" and not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=400,
            detail="OPENAI_API_KEY is not configured. Use provider=mock for the recorded demo or set the key first.",
        )


def _build_pipeline(
    *,
    provider: str,
    model: str,
    candidates: int,
    api_mode: str,
    seed: int | None,
    temperature: float | None,
    top_p: float | None,
    output_root: Path,
) -> ARGTestPipeline:
    _ensure_provider_ready(provider)
    return ARGTestPipeline(
        provider=provider,
        model=model,
        candidates=candidates,
        openai_api_mode=api_mode,
        seed=seed,
        temperature=temperature,
        top_p=top_p,
        output_root=str(output_root),
    )


def _load_run_payload(runtime_root: Path, split: str, requirement_id: str, summary: dict[str, Any]) -> dict[str, Any]:
    final_test_path = runtime_root / "outputs" / "final_tests" / split / f"{requirement_id}.json"
    report_path = runtime_root / "outputs" / "reports" / split / f"{requirement_id}_summary.json"
    state_model_md_path = runtime_root / "outputs" / "state_models" / split / f"{requirement_id}.md"
    return {
        "summary": summary,
        "parsed_trace": _read_json(final_test_path) if final_test_path.exists() else None,
        "report_payload": _read_json(report_path) if report_path.exists() else None,
        "state_model_markdown": state_model_md_path.read_text(encoding="utf-8") if state_model_md_path.exists() else None,
        "artifact_paths": {
            "runtime_root": _relative(runtime_root),
            "final_test_json": _relative(final_test_path) if final_test_path.exists() else None,
            "report_json": _relative(report_path) if report_path.exists() else None,
            "state_model_markdown": _relative(state_model_md_path) if state_model_md_path.exists() else None,
        },
    }


def _load_repeatability_snapshot(path: Path, label: str) -> dict[str, Any] | None:
    if not path.exists():
        return None
    payload = _read_json(path)
    requirement_count = int(payload.get("requirement_count", 0) or 0)
    stable_case_count = int(payload.get("stable_case_count", 0) or 0)
    stable_rate = round(stable_case_count / requirement_count, 3) if requirement_count else 0.0
    return {
        "label": label,
        "provider": payload.get("provider"),
        "model": payload.get("model"),
        "requirement_count": requirement_count,
        "stable_case_count": stable_case_count,
        "stable_rate": stable_rate,
        "avg_score_mean": payload.get("avg_score_mean"),
        "avg_coverage_mean": payload.get("avg_coverage_mean"),
        "avg_max_score_delta": payload.get("avg_max_score_delta"),
        "avg_max_coverage_delta": payload.get("avg_max_coverage_delta"),
    }


def _build_formal_summary() -> dict[str, Any]:
    main_path = FORMAL_REPORT_DIR / "run_main_summary.json"
    baseline_path = FORMAL_REPORT_DIR / "baseline_summary.json"
    generalization_path = FORMAL_REPORT_DIR / "generalization_by_category.json"
    ablation_path = FORMAL_REPORT_DIR / "ablation_summary.json"
    main_items = _read_json(main_path) if main_path.exists() else []
    baseline_items = _read_json(baseline_path) if baseline_path.exists() else []
    generalization = _read_json(generalization_path) if generalization_path.exists() else {"categories": []}
    ablation_items = _read_json(ablation_path) if ablation_path.exists() else []

    baseline_names = ["rule_based", "plain_llm", "structured_no_checker"]
    baseline_averages: dict[str, dict[str, float]] = {}
    for name in baseline_names:
        score_values = [item["baselines"][name]["checker_score"] for item in baseline_items if item.get("baselines", {}).get(name)]
        coverage_values = [item["baselines"][name]["overall_coverage"] for item in baseline_items if item.get("baselines", {}).get(name)]
        test_count_values = [item["baselines"][name]["test_count"] for item in baseline_items if item.get("baselines", {}).get(name)]
        baseline_averages[name] = {
            "avg_checker_score": _mean(score_values),
            "avg_overall_coverage": _mean(coverage_values),
            "avg_test_count": _mean(test_count_values),
        }

    ranked_cases = sorted(
        [
            {
                "requirement_id": item["requirement_id"],
                "category": item.get("category"),
                "checker_score": round(float(item.get("score", 0.0)), 3),
                "overall_coverage": round(float(item.get("metrics", {}).get("overall_coverage", 0.0)), 3),
                "risk_level": (item.get("risk_assessment") or {}).get("level"),
            }
            for item in main_items
        ],
        key=lambda row: (row["overall_coverage"], row["checker_score"]),
        reverse=True,
    )

    ablation_snapshot = None
    if ablation_items:
        ablation_snapshot = {
            "structured_no_checker": {
                "avg_checker_score": _mean([item["structured_no_checker"]["checker_score"] for item in ablation_items]),
                "avg_overall_coverage": _mean([item["structured_no_checker"]["overall_coverage"] for item in ablation_items]),
                "avg_test_count": _mean([item["structured_no_checker"]["test_count"] for item in ablation_items]),
            },
            "full_pipeline": {
                "avg_checker_score": _mean([item["full_pipeline"]["checker_score"] for item in ablation_items]),
                "avg_overall_coverage": _mean([item["full_pipeline"]["overall_coverage"] for item in ablation_items]),
                "avg_test_count": _mean([item["full_pipeline"]["test_count"] for item in ablation_items]),
            },
        }

    reproducibility = [
        _load_repeatability_snapshot(
            BASE_DIR / ".local_runs" / "repro_multi_seed_mock" / "outputs" / "reports" / "test" / "repeatability_summary.json",
            "Mock 3-seed",
        ),
        _load_repeatability_snapshot(
            BASE_DIR / ".local_runs" / "repro_live_qwen_5case" / "outputs" / "reports" / "test" / "repeatability_summary.json",
            "Live multi-seed",
        ),
        _load_repeatability_snapshot(
            BASE_DIR / ".local_runs" / "repro_live_same_seed_3case" / "outputs" / "reports" / "test" / "repeatability_summary.json",
            "Live same-seed",
        ),
    ]

    return {
        "official_run": {
            "requirement_count": len(main_items),
            "avg_checker_score": _mean([float(item.get("score", 0.0)) for item in main_items]),
            "avg_overall_coverage": _mean([float(item.get("metrics", {}).get("overall_coverage", 0.0)) for item in main_items]),
            "avg_test_count": _mean([float(item.get("metrics", {}).get("test_count", 0.0)) for item in main_items]),
            "high_risk_count": sum(1 for item in main_items if (item.get("risk_assessment") or {}).get("level") == "High"),
        },
        "baseline_averages": baseline_averages,
        "generalization": generalization.get("categories", []),
        "ablation": ablation_snapshot,
        "recommended_cases": ranked_cases[:5],
        "reproducibility": [snapshot for snapshot in reproducibility if snapshot is not None],
        "figure_gallery": [
            {
                "title": "Main vs Baselines",
                "caption": "Primary comparison figure for the defense.",
                "url": "/demo-assets/figures/main_vs_baselines.png",
            },
            {
                "title": "Final Result Scorecard",
                "caption": "Compact scoreboard for the frozen official test split.",
                "url": "/demo-assets/figures/final_result_scorecard.png",
            },
            {
                "title": "Generalization by Category",
                "caption": "Business-rules, input-validation, and workflow/state coverage profile.",
                "url": "/demo-assets/figures/generalization_by_category.png",
            },
            {
                "title": "Reproducibility and Stability",
                "caption": "Use this with the scripted explanation about replay and provider variance.",
                "url": "/demo-assets/figures/reproducibility_stability_overview.png",
            },
        ],
    }


@app.get("/")
def serve_index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "repo_root": str(BASE_DIR),
        "formal_results_available": FORMAL_REPORT_DIR.exists(),
        "sample_csv_available": SAMPLE_CSV_PATH.exists(),
    }


@app.get("/api/sample-csv")
def download_sample_csv() -> FileResponse:
    if not SAMPLE_CSV_PATH.exists():
        raise HTTPException(status_code=404, detail="Sample CSV is missing.")
    return FileResponse(SAMPLE_CSV_PATH, filename="sample_requirement_batch.csv", media_type="text/csv")


@app.get("/api/formal-summary")
def formal_summary() -> dict[str, Any]:
    return _build_formal_summary()


@app.post("/api/analyze-text")
def analyze_text(payload: AnalyzeTextRequest) -> dict[str, Any]:
    session_root = _build_session_root("text")
    pipeline = _build_pipeline(
        provider=payload.provider,
        model=payload.model,
        candidates=payload.candidates,
        api_mode=payload.api_mode,
        seed=payload.seed,
        temperature=payload.temperature,
        top_p=payload.top_p,
        output_root=session_root,
    )
    summary = pipeline.process_requirement_text(
        payload.requirement_text,
        requirement_id=payload.requirement_id,
        split=payload.split,
        candidates=payload.candidates,
        export=True,
    )
    return _load_run_payload(pipeline.config.paths.runtime_root, summary["split"], summary["requirement_id"], summary)


@app.post("/api/state-model")
def analyze_state_model(payload: AnalyzeTextRequest) -> dict[str, Any]:
    session_root = _build_session_root("state")
    pipeline = _build_pipeline(
        provider=payload.provider,
        model=payload.model,
        candidates=payload.candidates,
        api_mode=payload.api_mode,
        seed=payload.seed,
        temperature=payload.temperature,
        top_p=payload.top_p,
        output_root=session_root,
    )
    summary = pipeline.process_requirement_text(
        payload.requirement_text,
        requirement_id=payload.requirement_id,
        split=payload.split,
        candidates=payload.candidates,
        export=True,
    )
    payload_bundle = _load_run_payload(pipeline.config.paths.runtime_root, summary["split"], summary["requirement_id"], summary)
    payload_bundle["state_model_only"] = summary.get("state_model")
    return payload_bundle


@app.post("/api/analyze-csv")
async def analyze_csv(
    file: UploadFile = File(...),
    provider: str = Form(DEFAULT_PROVIDER),
    model: str = Form(DEFAULT_MODEL),
    candidates: int = Form(DEFAULT_CANDIDATES),
    api_mode: str = Form(DEFAULT_API_MODE),
    seed: int | None = Form(DEFAULT_SEED),
    temperature: float | None = Form(DEFAULT_TEMPERATURE),
    top_p: float | None = Form(DEFAULT_TOP_P),
    text_column: str = Form("requirement_text"),
    id_column: str = Form("requirement_id"),
    split_column: str = Form("split"),
    default_split: str = Form("adhoc"),
) -> dict[str, Any]:
    session_root = _build_session_root("csv")
    upload_dir = session_root / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded CSV is empty.")
    upload_path = upload_dir / (file.filename or "uploaded_requirements.csv")
    upload_path.write_bytes(raw_bytes)

    records = load_requirements_from_csv(
        upload_path,
        text_column=text_column,
        id_column=id_column,
        split_column=split_column,
        default_split=default_split,
    )
    pipeline = _build_pipeline(
        provider=provider,
        model=model,
        candidates=candidates,
        api_mode=api_mode,
        seed=seed,
        temperature=temperature,
        top_p=top_p,
        output_root=session_root,
    )
    rows: list[dict[str, Any]] = []
    for record in records:
        summary = pipeline.process_requirement_text(
            record.requirement_text,
            requirement_id=record.requirement_id,
            split=record.split,
            candidates=candidates,
            export=True,
        )
        rows.append(_load_run_payload(pipeline.config.paths.runtime_root, summary["split"], summary["requirement_id"], summary))
    return {
        "batch_size": len(rows),
        "uploaded_file": upload_path.name,
        "artifact_root": _relative(session_root),
        "records": rows,
    }


if __name__ == "__main__":
    uvicorn.run("demo_web.app:app", host="127.0.0.1", port=8000, reload=False)
