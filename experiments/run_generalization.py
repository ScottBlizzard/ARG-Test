from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils import load_json, write_json


def safe_avg(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 3)


def main() -> None:
    parser = argparse.ArgumentParser(description='Aggregate main experiment results by requirement category.')
    parser.add_argument('--split', choices=['dev', 'test'], default='test')
    args = parser.parse_args()

    manifest_path = ROOT / 'data' / 'requirements' / 'manifest.json'
    main_summary_path = ROOT / 'outputs' / 'reports' / args.split / 'run_main_summary.json'
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
        categories.append(
            {
                'category': category,
                'requirement_count': len(items),
                'avg_checker_score': safe_avg(checker_scores),
                'avg_overall_coverage': safe_avg(overall_coverages),
                'avg_duplicate_count': safe_avg(duplicates),
                'avg_test_count': safe_avg(test_counts),
            }
        )

    payload = {
        'split': args.split,
        'categories': categories,
    }
    output_path = ROOT / 'outputs' / 'reports' / args.split / 'generalization_by_category.json'
    write_json(output_path, payload)
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
