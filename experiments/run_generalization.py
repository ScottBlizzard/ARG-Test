from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import load_runtime_config
from src.utils import build_run_manifest, load_json, write_json


def safe_avg(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 3)


def main() -> None:
    parser = argparse.ArgumentParser(description='Aggregate main experiment results by requirement category.')
    parser.add_argument('--split', choices=['dev', 'test'], default='test')
    parser.add_argument('--output-root', default=None)
    args = parser.parse_args()

    config = load_runtime_config(base_dir=ROOT, output_root=args.output_root)
    manifest_path = ROOT / 'data' / 'requirements' / 'manifest.json'
    main_summary_path = config.paths.outputs / 'reports' / args.split / 'run_main_summary.json'
    if not manifest_path.exists() or not main_summary_path.exists():
        raise SystemExit('manifest.json or run_main_summary.json is missing')

    manifest = [item for item in load_json(manifest_path) if item.get('split') == args.split]
    main_summary = load_json(main_summary_path)
    category_by_id = {item['requirement_id']: item.get('category', 'unknown') for item in manifest}

    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in main_summary:
        requirement_id = item.get('requirement_id', '')
        category = category_by_id.get(requirement_id, 'unknown')
        grouped[category].append(item)

    categories = []
    for category, items in sorted(grouped.items()):
        checker_scores = [float(item.get('score', 0.0) or 0.0) for item in items]
        overall_coverages = [float(item.get('metrics', {}).get('overall_coverage', 0.0) or 0.0) for item in items]
        duplicates = [float(item.get('metrics', {}).get('duplicate_count', 0.0) or 0.0) for item in items]
        test_counts = [float(item.get('metrics', {}).get('test_count', 0.0) or 0.0) for item in items]
        risk_scores = [float((item.get('risk_assessment') or {}).get('score', 0.0) or 0.0) for item in items]
        high_risk_cases = sum(1 for item in items if (item.get('risk_assessment') or {}).get('level') == 'High')
        categories.append(
            {
                'category': category,
                'requirement_count': len(items),
                'avg_checker_score': safe_avg(checker_scores),
                'avg_overall_coverage': safe_avg(overall_coverages),
                'avg_duplicate_count': safe_avg(duplicates),
                'avg_test_count': safe_avg(test_counts),
                'avg_risk_score': safe_avg(risk_scores),
                'high_risk_requirement_count': high_risk_cases,
            }
        )

    payload = {
        'split': args.split,
        'categories': categories,
    }
    output_path = config.paths.outputs / 'reports' / args.split / 'generalization_by_category.json'
    write_json(output_path, payload)
    manifest = build_run_manifest(
        experiment='run_generalization',
        split=args.split,
        provider=config.provider,
        model=config.model,
        candidates=config.candidates,
        enable_repair=config.enable_repair,
        runtime_root=config.paths.runtime_root,
        requirement_ids=[item.get('requirement_id', '') for item in main_summary],
        extra={'output_summary_path': str(output_path)},
    )
    write_json(config.paths.outputs / 'reports' / args.split / 'generalization_manifest.json', manifest)
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
