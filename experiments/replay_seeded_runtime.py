from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pipeline import ARGTestPipeline
from src.utils import build_run_manifest, extract_requirement_id, list_requirement_files, read_text, write_json


def parse_ids(raw: str) -> set[str]:
    return {item.strip() for item in raw.split(",") if item.strip()}


def requirement_file_map(split: str) -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for path in list_requirement_files(ROOT, split):
        requirement_text = read_text(path)
        mapping[extract_requirement_id(requirement_text, path.stem)] = path
    return mapping


def load_raw_candidates(source_root: Path, split: str, requirement_id: str) -> tuple[list[str], list[dict], list[dict]]:
    raw_dir = source_root / "artifacts" / "raw_generations" / split
    raw_paths = sorted(raw_dir.glob(f"{requirement_id}_candidate_*.md"))
    if not raw_paths:
        raise SystemExit(f"No raw candidates found for {requirement_id} under {raw_dir}")
    raw_candidates = [path.read_text(encoding="utf-8") for path in raw_paths]
    metadata_rows: list[dict] = []
    controls: list[dict] = []
    for path in raw_paths:
        metadata_path = path.with_suffix(".json")
        if metadata_path.exists():
            payload = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata_rows.append(payload.get("generation_metadata") or {})
            controls.append(payload.get("candidate_control") or {})
        else:
            metadata_rows.append({})
            controls.append({})
    return raw_candidates, metadata_rows, controls


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay a frozen seeded runtime from saved raw generations.")
    parser.add_argument("--source-root", required=True, help="Runtime root containing artifacts/raw_generations from a live seeded run.")
    parser.add_argument("--split", choices=["dev", "test"], default="test")
    parser.add_argument("--ids", default="", help="Optional comma-separated requirement ids to replay.")
    parser.add_argument("--output-root", required=True, help="New runtime root for the deterministic replay outputs.")
    args = parser.parse_args()

    source_root = (ROOT / args.source_root).resolve() if not Path(args.source_root).is_absolute() else Path(args.source_root).resolve()
    selected_ids = parse_ids(args.ids)
    files_by_id = requirement_file_map(args.split)
    replay_ids = sorted(selected_ids) if selected_ids else sorted(files_by_id)
    missing = [requirement_id for requirement_id in replay_ids if requirement_id not in files_by_id]
    if missing:
        raise SystemExit(f"Missing requirement definitions for split {args.split}: {missing}")

    pipeline = ARGTestPipeline(
        base_dir=ROOT,
        provider="mock",
        model="replay-from-raw",
        candidates=3,
        seed=0,
        temperature=0.0,
        top_p=1.0,
        output_root=args.output_root,
    )

    summaries = []
    for requirement_id in replay_ids:
        requirement_text = read_text(files_by_id[requirement_id])
        raw_candidates, metadata_rows, controls = load_raw_candidates(source_root, args.split, requirement_id)
        summaries.append(
            pipeline.summarize_raw_candidates(
                requirement_text,
                requirement_id,
                args.split,
                raw_candidates,
                generation_metadata=metadata_rows,
                candidate_controls=controls,
                export=True,
            )
        )

    report_path = pipeline.config.paths.outputs / "reports" / args.split / "run_main_summary.json"
    write_json(report_path, summaries)
    manifest = build_run_manifest(
        experiment="replay_seeded_runtime",
        split=args.split,
        provider="replay",
        model="replay-from-raw",
        candidates=max((len(item.get("candidate_controls", [])) for item in summaries), default=0),
        openai_api_mode="replay",
        seed=None,
        temperature=0.0,
        top_p=1.0,
        enable_repair=pipeline.config.enable_repair,
        runtime_root=pipeline.config.paths.runtime_root,
        requirement_ids=[item["requirement_id"] for item in summaries],
        extra={
            "source_root": str(source_root),
            "selected_ids": sorted(selected_ids),
            "output_summary_path": str(report_path),
        },
    )
    write_json(pipeline.config.paths.outputs / "reports" / args.split / "run_main_manifest.json", manifest)
    print(json.dumps(summaries, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
