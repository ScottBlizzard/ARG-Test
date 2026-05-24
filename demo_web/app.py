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
from src.utils import extract_requirement_id

BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = Path(__file__).resolve().parent / "static"
FIGURES_DIR = BASE_DIR / "report_assets" / "figures"
FRONTEND_FOCUS_DIR = BASE_DIR / "report_assets" / "final_demo_package" / "frontend_focus"
TRACKED_FORMAL_SNAPSHOT_DIR = FRONTEND_FOCUS_DIR / "formal_results_snapshot"
TRACKED_FORMAL_REPORT_DIR = TRACKED_FORMAL_SNAPSHOT_DIR / "reports" / "test"
TRACKED_FORMAL_FINAL_TEST_DIR = TRACKED_FORMAL_SNAPSHOT_DIR / "final_tests" / "test"
TRACKED_FORMAL_STATE_MODEL_DIR = TRACKED_FORMAL_SNAPSHOT_DIR / "state_models" / "test"
SAMPLE_CSV_PATH = BASE_DIR / "final_docs" / "execution_evidence" / "sample_requirement_batch.csv"
WEB_RUNS_ROOT = BASE_DIR / ".local_runs" / "web_demo_sessions"
REQUIREMENT_ROOT = BASE_DIR / "data" / "requirements"
REQUIREMENT_MANIFEST_PATH = REQUIREMENT_ROOT / "manifest.json"
DEFAULT_PROVIDER = "mock"
DEFAULT_MODEL = "mock-arg-test"
DEFAULT_CANDIDATES = 3
DEFAULT_API_MODE = "chat_completions"
DEFAULT_SEED = 202601
DEFAULT_TEMPERATURE = 0.0
DEFAULT_TOP_P = 1.0


def _prefer_existing_path(*candidates: Path) -> Path:
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


FORMAL_REPORT_DIR = _prefer_existing_path(
    TRACKED_FORMAL_REPORT_DIR,
    BASE_DIR / ".local_runs" / "formal_qwen_novpn" / "outputs" / "reports" / "test",
)
FORMAL_FINAL_TEST_DIR = _prefer_existing_path(
    TRACKED_FORMAL_FINAL_TEST_DIR,
    BASE_DIR / ".local_runs" / "formal_qwen_novpn" / "outputs" / "final_tests" / "test",
)
FORMAL_STATE_MODEL_DIR = _prefer_existing_path(
    TRACKED_FORMAL_STATE_MODEL_DIR,
    BASE_DIR / ".local_runs" / "formal_qwen_novpn" / "outputs" / "state_models" / "test",
)
REPEATABILITY_PATHS = {
    "Mock 3-seed": _prefer_existing_path(
        TRACKED_FORMAL_SNAPSHOT_DIR / "repeatability" / "repro_multi_seed_mock_repeatability_summary.json",
        BASE_DIR / ".local_runs" / "repro_multi_seed_mock" / "outputs" / "reports" / "test" / "repeatability_summary.json",
    ),
    "Live multi-seed": _prefer_existing_path(
        TRACKED_FORMAL_SNAPSHOT_DIR / "repeatability" / "repro_live_qwen_5case_repeatability_summary.json",
        BASE_DIR / ".local_runs" / "repro_live_qwen_5case" / "outputs" / "reports" / "test" / "repeatability_summary.json",
    ),
    "Live same-seed": _prefer_existing_path(
        TRACKED_FORMAL_SNAPSHOT_DIR / "repeatability" / "repro_live_same_seed_3case_repeatability_summary.json",
        BASE_DIR / ".local_runs" / "repro_live_same_seed_3case" / "outputs" / "reports" / "test" / "repeatability_summary.json",
    ),
}

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


def _normalize_requirement_text(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.replace("\ufeff", "").strip().splitlines())


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


def _formal_summary_item(requirement_id: str) -> dict[str, Any] | None:
    main_path = FORMAL_REPORT_DIR / "run_main_summary.json"
    if not main_path.exists():
        return None
    for item in _read_json(main_path):
        if item.get("requirement_id") == requirement_id:
            return item
    return None


def _catalog_text_matches(split: str, requirement_id: str, requirement_text: str) -> bool:
    requirement_path = REQUIREMENT_ROOT / split / f"{requirement_id}.txt"
    if not requirement_path.exists():
        return False
    expected = requirement_path.read_text(encoding="utf-8-sig")
    return _normalize_requirement_text(expected) == _normalize_requirement_text(requirement_text)


def _load_formal_replay_payload(split: str, requirement_id: str, requirement_text: str) -> dict[str, Any] | None:
    if split != "test" or not _catalog_text_matches(split, requirement_id, requirement_text):
        return None
    summary = _formal_summary_item(requirement_id)
    final_test_path = FORMAL_FINAL_TEST_DIR / f"{requirement_id}.json"
    state_model_md_path = FORMAL_STATE_MODEL_DIR / f"{requirement_id}.md"
    state_model_json_path = FORMAL_STATE_MODEL_DIR / f"{requirement_id}.json"
    if not summary or not final_test_path.exists():
        return None

    replay_summary = dict(summary)
    replay_summary["demo_mode"] = "frozen_formal_replay"
    replay_summary["provider"] = DEFAULT_PROVIDER
    replay_summary["model"] = DEFAULT_MODEL
    diagnostics = list(replay_summary.get("diagnostics") or [])
    diagnostics.insert(0, "demo_mode: frozen formal replay; coverage matches the official Formal Evidence dashboard")
    replay_summary["diagnostics"] = diagnostics
    if state_model_json_path.exists() and not replay_summary.get("state_model"):
        replay_summary["state_model"] = _read_json(state_model_json_path)

    return {
        "summary": replay_summary,
        "parsed_trace": _read_json(final_test_path),
        "report_payload": replay_summary,
        "state_model_markdown": state_model_md_path.read_text(encoding="utf-8") if state_model_md_path.exists() else None,
        "replay_source": "frozen_formal_run",
        "artifact_paths": {
            "formal_report_source": _relative(FORMAL_REPORT_DIR / "run_main_summary.json"),
            "final_test_json": _relative(final_test_path),
            "state_model_markdown": _relative(state_model_md_path) if state_model_md_path.exists() else None,
        },
    }


def _run_pipeline_payload(
    *,
    prefix: str,
    provider: str,
    model: str,
    candidates: int,
    api_mode: str,
    seed: int | None,
    temperature: float | None,
    top_p: float | None,
    requirement_text: str,
    requirement_id: str | None,
    split: str,
) -> dict[str, Any]:
    session_root = _build_session_root(prefix)
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
    summary = pipeline.process_requirement_text(
        requirement_text,
        requirement_id=requirement_id,
        split=split,
        candidates=candidates,
        export=True,
    )
    return _load_run_payload(pipeline.config.paths.runtime_root, summary["split"], summary["requirement_id"], summary)


def _load_repeatability_snapshot(path: Path, label: str) -> dict[str, Any] | None:
    if not path.exists():
        return None
    payload = _read_json(path)
    requirement_count = int(payload.get("requirement_count", 0) or 0)
    stable_case_count = int(payload.get("stable_case_count", 0) or 0)
    stable_rate = round(stable_case_count / requirement_count, 3) if requirement_count else 0.0
    return {
        "label": label,
        "source_path": _relative(path),
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
        _load_repeatability_snapshot(path, label)
        for label, path in REPEATABILITY_PATHS.items()
    ]

    return {
        "formal_report_source": _relative(FORMAL_REPORT_DIR),
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


def _build_demo_requirement_catalog() -> dict[str, Any]:
    manifest_items = _read_json(REQUIREMENT_MANIFEST_PATH) if REQUIREMENT_MANIFEST_PATH.exists() else []
    formal_items = _read_json(FORMAL_REPORT_DIR / "run_main_summary.json") if (FORMAL_REPORT_DIR / "run_main_summary.json").exists() else []
    formal_by_id = {
        item.get("requirement_id"): item
        for item in formal_items
        if item.get("requirement_id")
    }
    preferred_order = [
        "pickup_station_contact_validation",
        "warehouse_pickup_order_workflow",
        "order_split_shipment_state_machine",
        "return_exchange_approval_workflow",
        "checkout_promo_stack_and_priority",
        "coupon_discount_engine",
    ]
    order_rank = {requirement_id: index for index, requirement_id in enumerate(preferred_order)}
    requirements: list[dict[str, Any]] = []

    for item in manifest_items:
        requirement_id = item.get("requirement_id")
        split = item.get("split")
        if split != "test" or not requirement_id:
            continue
        requirement_path = REQUIREMENT_ROOT / split / f"{requirement_id}.txt"
        if not requirement_path.exists():
            continue
        formal_item = formal_by_id.get(requirement_id, {})
        metrics = formal_item.get("metrics", {}) if isinstance(formal_item, dict) else {}
        requirements.append(
            {
                "requirement_id": requirement_id,
                "split": split,
                "category": item.get("category") or formal_item.get("category"),
                "recommended_techniques": item.get("recommended_techniques", []),
                "requirement_text": requirement_path.read_text(encoding="utf-8-sig"),
                "checker_score": formal_item.get("score"),
                "overall_coverage": metrics.get("overall_coverage"),
            }
        )

    requirements.sort(
        key=lambda row: (
            order_rank.get(row["requirement_id"], 100),
            row.get("category") or "",
            row["requirement_id"],
        )
    )
    state_requirements = [
        row
        for row in requirements
        if row.get("category") == "workflow_state"
    ]
    return {
        "provider": DEFAULT_PROVIDER,
        "model": DEFAULT_MODEL,
        "seed": DEFAULT_SEED,
        "candidates": DEFAULT_CANDIDATES,
        "direct_requirements": requirements,
        "state_requirements": state_requirements,
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
        "formal_results_source": _relative(FORMAL_REPORT_DIR),
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


@app.get("/api/demo-requirements")
def demo_requirements() -> dict[str, Any]:
    return _build_demo_requirement_catalog()


@app.post("/api/analyze-text")
def analyze_text(payload: AnalyzeTextRequest) -> dict[str, Any]:
    resolved_id = extract_requirement_id(payload.requirement_text, payload.requirement_id or "adhoc_requirement")
    replay_payload = _load_formal_replay_payload(payload.split, resolved_id, payload.requirement_text)
    if payload.provider == DEFAULT_PROVIDER and replay_payload is not None:
        return replay_payload

    return _run_pipeline_payload(
        prefix="text",
        provider=payload.provider,
        model=payload.model,
        candidates=payload.candidates,
        api_mode=payload.api_mode,
        seed=payload.seed,
        temperature=payload.temperature,
        top_p=payload.top_p,
        requirement_id=payload.requirement_id,
        requirement_text=payload.requirement_text,
        split=payload.split,
    )


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
        resolved_id = extract_requirement_id(record.requirement_text, record.requirement_id)
        replay_payload = _load_formal_replay_payload(record.split, resolved_id, record.requirement_text)
        if provider == DEFAULT_PROVIDER and replay_payload is not None:
            rows.append(replay_payload)
            continue
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
