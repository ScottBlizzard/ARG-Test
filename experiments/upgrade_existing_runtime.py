from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.risk import assess_requirement_risk, assign_case_priorities
from src.schemas import ParsedTrace, TestCase
from src.utils import build_run_manifest, list_requirement_files, read_text, requirement_category, write_json


def requirement_text_map(split: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for path in list_requirement_files(ROOT, split):
        text = read_text(path)
        requirement_id = path.stem
        mapping[requirement_id] = text
    return mapping


def trace_from_payload(payload: dict) -> ParsedTrace:
    test_cases = [
        TestCase(
            test_id=item.get("test_id", ""),
            technique=item.get("technique", "EP"),
            requirement_target=item.get("requirement_target", payload.get("requirement_id", "")),
            preconditions=item.get("preconditions", "None"),
            input_data=item.get("input", item.get("input_data", "N/A")),
            expected_output=item.get("expected_output", "TBD"),
            covered_item=item.get("covered_item", ""),
            priority=item.get("priority", "Medium"),
            checker_status=item.get("checker_status", "pending"),
        )
        for item in payload.get("test_cases", [])
    ]
    return ParsedTrace(
        requirement_id=payload.get("requirement_id", ""),
        analysis=payload.get("analysis", ""),
        pattern=payload.get("pattern", ""),
        steps=list(payload.get("steps", [])),
        verification=payload.get("verification", ""),
        test_cases=test_cases,
        raw_text="",
        category=payload.get("category"),
        missing_sections=list(payload.get("missing_sections", [])),
    )


def enrich_main_summary(
    runtime_root: Path,
    split: str,
    provider: str,
    model: str,
    candidates: int,
    enable_repair: bool,
) -> dict[str, dict]:
    report_dir = runtime_root / "outputs" / "reports" / split
    tests_dir = runtime_root / "outputs" / "final_tests" / split
    parsed_dir = runtime_root / "artifacts" / "parsed_traces" / split
    checker_dir = runtime_root / "artifacts" / "checker_logs" / split
    summary_path = report_dir / "run_main_summary.json"
    summaries = json.loads(summary_path.read_text(encoding="utf-8-sig"))

    texts = requirement_text_map(split)
    risk_by_id: dict[str, dict] = {}

    for item in summaries:
        requirement_id = item["requirement_id"]
        trace_path = tests_dir / f"{requirement_id}.json"
        if not trace_path.exists():
            trace_path = parsed_dir / f"{requirement_id}.json"
        payload = json.loads(trace_path.read_text(encoding="utf-8-sig"))
        parsed = trace_from_payload(payload)
        parsed.category = requirement_category(ROOT, split, requirement_id)
        parsed.risk_assessment = assess_requirement_risk(texts[requirement_id], parsed, parsed.category)
        assign_case_priorities(parsed)

        trace_json = parsed.to_dict()
        write_json(trace_path, trace_json)
        if (parsed_dir / f"{requirement_id}.json").exists():
            write_json(parsed_dir / f"{requirement_id}.json", trace_json)
        markdown_path = tests_dir / f"{requirement_id}.md"
        if markdown_path.exists():
            markdown_path.write_text(parsed.to_markdown(), encoding="utf-8")

        item["category"] = parsed.category
        item["risk_assessment"] = parsed.risk_assessment.to_dict()
        risk_by_id[requirement_id] = {
            "category": parsed.category,
            "risk_assessment": parsed.risk_assessment.to_dict(),
        }

        per_requirement_summary = report_dir / f"{requirement_id}_summary.json"
        if per_requirement_summary.exists():
            detail = json.loads(per_requirement_summary.read_text(encoding="utf-8-sig"))
            detail["split"] = split
            detail["category"] = parsed.category
            detail["risk_assessment"] = parsed.risk_assessment.to_dict()
            detail["run_context"] = {
                "split": split,
                "provider": provider,
                "model": model,
                "candidates": candidates,
                "enable_repair": enable_repair,
                "runtime_root": str(runtime_root),
                "outputs_root": str(runtime_root / "outputs"),
                "artifacts_root": str(runtime_root / "artifacts"),
            }
            write_json(per_requirement_summary, detail)

        checker_path = checker_dir / f"{requirement_id}.json"
        if checker_path.exists():
            checker_payload = json.loads(checker_path.read_text(encoding="utf-8-sig"))
            checker_payload["category"] = parsed.category
            checker_payload["risk_assessment"] = parsed.risk_assessment.to_dict()
            checker_payload["run_context"] = {
                "split": split,
                "provider": provider,
                "model": model,
                "candidates": candidates,
                "enable_repair": enable_repair,
                "runtime_root": str(runtime_root),
                "outputs_root": str(runtime_root / "outputs"),
                "artifacts_root": str(runtime_root / "artifacts"),
            }
            write_json(checker_path, checker_payload)

    write_json(summary_path, summaries)
    write_json(
        report_dir / "run_main_manifest.json",
        build_run_manifest(
            experiment="run_main",
            split=split,
            provider=provider,
            model=model,
            candidates=candidates,
            enable_repair=enable_repair,
            runtime_root=runtime_root,
            requirement_ids=[item["requirement_id"] for item in summaries],
            extra={"output_summary_path": str(summary_path), "source": "offline_enrichment"},
        ),
    )
    return risk_by_id


def enrich_baseline_or_ablation(
    runtime_root: Path,
    split: str,
    filename: str,
    manifest_name: str,
    provider: str,
    model: str,
    candidates: int,
    enable_repair: bool,
    risk_by_id: dict[str, dict],
) -> None:
    report_dir = runtime_root / "outputs" / "reports" / split
    path = report_dir / filename
    if not path.exists():
        return
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    requirement_ids: list[str] = []
    for item in payload:
        requirement_id = item.get("requirement_id", "")
        requirement_ids.append(requirement_id)
        risk_info = risk_by_id.get(requirement_id, {})
        item["category"] = risk_info.get("category")
        item["risk_assessment"] = risk_info.get("risk_assessment")
    write_json(path, payload)
    write_json(
        report_dir / manifest_name,
        build_run_manifest(
            experiment=manifest_name.replace("_manifest.json", ""),
            split=split,
            provider=provider,
            model=model,
            candidates=candidates,
            enable_repair=enable_repair,
            runtime_root=runtime_root,
            requirement_ids=requirement_ids,
            extra={"output_summary_path": str(path), "source": "offline_enrichment"},
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline-upgrade an existing runtime with risk metadata and manifests.")
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--split", choices=["dev", "test"], default="test")
    parser.add_argument("--provider", default="openai")
    parser.add_argument("--model", default="qwen3.5-flash")
    parser.add_argument("--candidates", type=int, default=3)
    parser.add_argument("--enable-repair", choices=["true", "false"], default="true")
    args = parser.parse_args()

    runtime_root = Path(args.runtime_root)
    if not runtime_root.is_absolute():
        runtime_root = (ROOT / runtime_root).resolve()

    risk_by_id = enrich_main_summary(
        runtime_root=runtime_root,
        split=args.split,
        provider=args.provider,
        model=args.model,
        candidates=args.candidates,
        enable_repair=args.enable_repair == "true",
    )
    enrich_baseline_or_ablation(
        runtime_root,
        args.split,
        "baseline_summary.json",
        "baseline_manifest.json",
        args.provider,
        args.model,
        1,
        False,
        risk_by_id,
    )
    enrich_baseline_or_ablation(
        runtime_root,
        args.split,
        "ablation_summary.json",
        "ablation_manifest.json",
        args.provider,
        args.model,
        args.candidates,
        args.enable_repair == "true",
        risk_by_id,
    )
    print(
        json.dumps(
            {
                "runtime_root": str(runtime_root),
                "split": args.split,
                "upgraded_requirement_count": len(risk_by_id),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
