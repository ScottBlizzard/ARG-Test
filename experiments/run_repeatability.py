from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pipeline import ARGTestPipeline
from src.utils import build_run_manifest, extract_requirement_id, list_requirement_files, read_text, requirement_category, write_json


def parse_ids(raw: str) -> set[str]:
    return {item.strip() for item in raw.split(",") if item.strip()}


def parse_seed_values(raw: str) -> list[int]:
    return [int(item.strip()) for item in raw.split(",") if item.strip()]


def build_seed_schedule(
    repeats: int,
    *,
    seed_values: list[int],
    seed_base: int | None,
    seed_step: int,
    fixed_seed: int | None,
) -> list[int | None]:
    if seed_values:
        if len(seed_values) != repeats:
            raise SystemExit(f"Expected {repeats} seed values but received {len(seed_values)}")
        return seed_values
    if seed_base is not None:
        return [seed_base + index * seed_step for index in range(repeats)]
    if fixed_seed is not None:
        return [fixed_seed for _ in range(repeats)]
    return [None for _ in range(repeats)]


def safe_avg(values: list[float]) -> float:
    return round(sum(values) / len(values), 3) if values else 0.0


def safe_std(values: list[float]) -> float:
    if len(values) <= 1:
        return 0.0
    return round(statistics.pstdev(values), 3)


def build_markdown(payload: dict) -> str:
    lines = [
        "# Repeatability Summary",
        "",
        f"- Split: `{payload['split']}`",
        f"- Repeats: `{payload['repeats']}`",
        f"- Requirements: `{payload['requirement_count']}`",
        f"- Seed schedule: `{', '.join('none' if value is None else str(value) for value in payload['seed_schedule'])}`",
        f"- Stable cases (max score delta<=0.05 and max coverage delta<=0.10): `{payload['stable_case_count']}/{payload['requirement_count']}`",
        f"- Mean checker score across reruns: `{payload['avg_score_mean']}`",
        f"- Mean overall coverage across reruns: `{payload['avg_coverage_mean']}`",
        f"- Avg max score delta: `{payload['avg_max_score_delta']}`",
        f"- Avg max coverage delta: `{payload['avg_max_coverage_delta']}`",
        "",
        "| Requirement | Category | Risk | Score Mean | Score Std | Max Score Delta | Coverage Mean | Coverage Std | Max Coverage Delta | Stable |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for item in payload["requirements"]:
        lines.append(
            f"| {item['requirement_id']} | {item['category']} | {item['risk_level']} | {item['score_mean']:.3f} | {item['score_std']:.3f} | {item['max_score_delta']:.3f} | {item['coverage_mean']:.3f} | {item['coverage_std']:.3f} | {item['max_coverage_delta']:.3f} | {'yes' if item['stable'] else 'no'} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run repeated independent reruns for stability analysis.")
    parser.add_argument("--split", choices=["dev", "test"], default="test")
    parser.add_argument("--provider", default="mock")
    parser.add_argument("--model", default="mock-arg-test")
    parser.add_argument("--candidates", type=int, default=3)
    parser.add_argument("--api-mode", default=None, choices=["responses", "chat_completions"])
    parser.add_argument("--seed", type=int, default=None, help="Fixed seed reused for every repeat.")
    parser.add_argument("--seed-base", type=int, default=None, help="Base seed for a deterministic multi-seed schedule.")
    parser.add_argument("--seed-step", type=int, default=101, help="Seed increment used with --seed-base.")
    parser.add_argument("--seed-values", default="", help="Comma-separated explicit seeds. Length must equal --repeats.")
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--top-p", type=float, default=None)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--ids", default="", help="Comma-separated requirement ids.")
    parser.add_argument("--output-root", required=True, help="Parent runtime root for the repeatability study.")
    args = parser.parse_args()

    selected_ids = parse_ids(args.ids)
    requirement_files = list_requirement_files(ROOT, args.split)
    if selected_ids:
        requirement_files = [
            path for path in requirement_files
            if extract_requirement_id(read_text(path), path.stem) in selected_ids
        ]
    if args.limit:
        requirement_files = requirement_files[: args.limit]
    if not requirement_files:
        raise SystemExit("No requirement files selected for repeatability run")

    requirement_ids = [extract_requirement_id(read_text(path), path.stem) for path in requirement_files]
    seed_schedule = build_seed_schedule(
        args.repeats,
        seed_values=parse_seed_values(args.seed_values),
        seed_base=args.seed_base,
        seed_step=args.seed_step,
        fixed_seed=args.seed,
    )
    repeat_runs: list[dict] = []
    aggregated: dict[str, dict[str, list[float] | dict | str]] = {}
    enable_repair = True

    for repeat_index in range(1, args.repeats + 1):
        rerun_root = Path(args.output_root) / f"rerun_{repeat_index}"
        repeat_seed = seed_schedule[repeat_index - 1]
        pipeline = ARGTestPipeline(
            base_dir=ROOT,
            provider=args.provider,
            model=args.model,
            candidates=args.candidates,
            openai_api_mode=args.api_mode,
            seed=repeat_seed,
            temperature=args.temperature,
            top_p=args.top_p,
            output_root=str(rerun_root),
        )
        enable_repair = pipeline.config.enable_repair
        summaries = [pipeline.process_requirement_file(path, candidates=args.candidates) for path in requirement_files]
        repeat_runs.append(
            {
                "repeat_index": repeat_index,
                "seed": repeat_seed,
                "runtime_root": str(pipeline.config.paths.runtime_root),
                "summaries": summaries,
            }
        )
        for item in summaries:
            bucket = aggregated.setdefault(
                item["requirement_id"],
                {
                    "requirement_id": item["requirement_id"],
                    "category": item.get("category") or requirement_category(ROOT, args.split, item["requirement_id"]) or "unknown",
                    "risk_level": (item.get("risk_assessment") or {}).get("level", ""),
                    "score_values": [],
                    "coverage_values": [],
                },
            )
            bucket["score_values"].append(float(item["score"]))
            bucket["coverage_values"].append(float(item["metrics"]["overall_coverage"]))

    requirement_rows = []
    for requirement_id in requirement_ids:
        bucket = aggregated[requirement_id]
        score_values = list(bucket["score_values"])
        coverage_values = list(bucket["coverage_values"])
        max_score_delta = round(max(score_values) - min(score_values), 3) if score_values else 0.0
        max_coverage_delta = round(max(coverage_values) - min(coverage_values), 3) if coverage_values else 0.0
        requirement_rows.append(
            {
                "requirement_id": requirement_id,
                "category": bucket["category"],
                "risk_level": bucket["risk_level"],
                "score_mean": safe_avg(score_values),
                "score_std": safe_std(score_values),
                "max_score_delta": max_score_delta,
                "coverage_mean": safe_avg(coverage_values),
                "coverage_std": safe_std(coverage_values),
                "max_coverage_delta": max_coverage_delta,
                "stable": max_score_delta <= 0.05 and max_coverage_delta <= 0.10,
            }
        )

    payload = {
        "split": args.split,
        "provider": args.provider,
        "model": args.model,
        "openai_api_mode": pipeline.config.openai_api_mode if repeat_runs else args.api_mode,
        "seed_schedule": seed_schedule,
        "candidates": args.candidates,
        "repeats": args.repeats,
        "requirement_count": len(requirement_rows),
        "selected_ids": sorted(selected_ids),
        "requirements": requirement_rows,
        "stable_case_count": sum(1 for item in requirement_rows if item["stable"]),
        "avg_score_mean": safe_avg([item["score_mean"] for item in requirement_rows]),
        "avg_coverage_mean": safe_avg([item["coverage_mean"] for item in requirement_rows]),
        "avg_max_score_delta": safe_avg([item["max_score_delta"] for item in requirement_rows]),
        "avg_max_coverage_delta": safe_avg([item["max_coverage_delta"] for item in requirement_rows]),
        "runs": repeat_runs,
    }

    runtime_root = ROOT / args.output_root
    report_dir = runtime_root / "outputs" / "reports" / args.split
    report_dir.mkdir(parents=True, exist_ok=True)
    write_json(report_dir / "repeatability_summary.json", payload)
    (report_dir / "repeatability_summary.md").write_text(build_markdown(payload), encoding="utf-8")
    manifest = build_run_manifest(
        experiment="run_repeatability",
        split=args.split,
        provider=args.provider,
        model=args.model,
        candidates=args.candidates,
        openai_api_mode=pipeline.config.openai_api_mode if repeat_runs else args.api_mode,
        seed=None,
        temperature=pipeline.config.temperature if repeat_runs else args.temperature,
        top_p=pipeline.config.top_p if repeat_runs else args.top_p,
        enable_repair=enable_repair,
        runtime_root=runtime_root,
        requirement_ids=requirement_ids,
        extra={
            "repeats": args.repeats,
            "limit": args.limit,
            "selected_ids": sorted(selected_ids),
            "seed_schedule": seed_schedule,
            "output_summary_path": str(report_dir / "repeatability_summary.json"),
        },
    )
    write_json(report_dir / "repeatability_manifest.json", manifest)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
