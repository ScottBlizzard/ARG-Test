from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import load_runtime_config
from src.utils import load_json


OUTPUTS_ROOT = ROOT / 'outputs'


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def render_value(value):
    if value is None:
        return ''
    if isinstance(value, float):
        return f'{value:.3f}'.rstrip('0').rstrip('.')
    return value


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text('', encoding='utf-8')
        return
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows([{key: render_value(value) for key, value in row.items()} for row in rows])


def write_md(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text('', encoding='utf-8')
        return
    headers = list(rows[0].keys())
    lines = [
        '| ' + ' | '.join(headers) + ' |',
        '| ' + ' | '.join(['---'] * len(headers)) + ' |',
    ]
    for row in rows:
        lines.append('| ' + ' | '.join(str(render_value(row.get(header, ''))).replace('|', '/') for header in headers) + ' |')
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def flatten_main(split: str) -> list[dict]:
    path = OUTPUTS_ROOT / 'reports' / split / 'run_main_summary.json'
    if not path.exists():
        return []
    payload = load_json(path)
    rows = []
    for item in payload:
        metrics = item.get('metrics', {})
        coverage = metrics.get('coverage', {})
        rows.append(
            {
                'requirement_id': item.get('requirement_id', ''),
                'split': split,
                'checker_score': item.get('score', ''),
                'overall_coverage': metrics.get('overall_coverage', ''),
                'duplicate_count': metrics.get('duplicate_count', ''),
                'test_count': metrics.get('test_count', ''),
                'repaired': item.get('repaired', False),
                'applicable_dimension_count': metrics.get('applicable_dimension_count', ''),
                'valid_partition_coverage': coverage.get('valid_partition_coverage', ''),
                'invalid_partition_coverage': coverage.get('invalid_partition_coverage', ''),
                'boundary_coverage': coverage.get('boundary_coverage', ''),
                'decision_rule_coverage': coverage.get('decision_rule_coverage', ''),
                'state_coverage': coverage.get('state_coverage', ''),
                'illegal_transition_coverage': coverage.get('illegal_transition_coverage', ''),
                'exception_coverage': coverage.get('exception_coverage', ''),
                'diagnostics_count': len(item.get('diagnostics', [])),
            }
        )
    return rows


def flatten_baseline(split: str) -> list[dict]:
    path = OUTPUTS_ROOT / 'reports' / split / 'baseline_summary.json'
    if not path.exists():
        return []
    payload = load_json(path)
    rows = []
    for item in payload:
        for baseline, metrics in item.get('baselines', {}).items():
            coverage = metrics.get('coverage', {})
            rows.append(
                {
                    'requirement_id': item.get('requirement_id', ''),
                    'split': split,
                    'baseline': baseline,
                    'checker_score': metrics.get('checker_score', ''),
                    'overall_coverage': metrics.get('overall_coverage', ''),
                    'duplicate_count': metrics.get('duplicate_count', ''),
                    'test_count': metrics.get('test_count', ''),
                    'applicable_dimension_count': metrics.get('applicable_dimension_count', ''),
                    'valid_partition_coverage': coverage.get('valid_partition_coverage', ''),
                    'invalid_partition_coverage': coverage.get('invalid_partition_coverage', ''),
                    'boundary_coverage': coverage.get('boundary_coverage', ''),
                    'decision_rule_coverage': coverage.get('decision_rule_coverage', ''),
                    'state_coverage': coverage.get('state_coverage', ''),
                    'illegal_transition_coverage': coverage.get('illegal_transition_coverage', ''),
                    'exception_coverage': coverage.get('exception_coverage', ''),
                }
            )
    return rows


def flatten_ablation(split: str) -> list[dict]:
    path = OUTPUTS_ROOT / 'reports' / split / 'ablation_summary.json'
    if not path.exists():
        return []
    payload = load_json(path)
    rows = []
    for item in payload:
        for variant in ['structured_no_checker', 'full_pipeline']:
            metrics = item.get(variant, {})
            coverage = metrics.get('coverage', {})
            rows.append(
                {
                    'requirement_id': item.get('requirement_id', ''),
                    'split': split,
                    'variant': variant,
                    'checker_score': metrics.get('checker_score', ''),
                    'overall_coverage': metrics.get('overall_coverage', ''),
                    'duplicate_count': metrics.get('duplicate_count', ''),
                    'test_count': metrics.get('test_count', ''),
                    'repaired': metrics.get('repaired', ''),
                    'applicable_dimension_count': metrics.get('applicable_dimension_count', ''),
                    'valid_partition_coverage': coverage.get('valid_partition_coverage', ''),
                    'invalid_partition_coverage': coverage.get('invalid_partition_coverage', ''),
                    'boundary_coverage': coverage.get('boundary_coverage', ''),
                    'decision_rule_coverage': coverage.get('decision_rule_coverage', ''),
                    'state_coverage': coverage.get('state_coverage', ''),
                    'illegal_transition_coverage': coverage.get('illegal_transition_coverage', ''),
                    'exception_coverage': coverage.get('exception_coverage', ''),
                }
            )
    return rows


def flatten_generalization(split: str) -> list[dict]:
    path = OUTPUTS_ROOT / 'reports' / split / 'generalization_by_category.json'
    if not path.exists():
        return []
    payload = load_json(path)
    rows = []
    for item in payload.get('categories', []):
        rows.append(item)
    return rows


def main() -> None:
    global OUTPUTS_ROOT

    parser = argparse.ArgumentParser(description='Export report summary JSON files to CSV and Markdown tables.')
    parser.add_argument('--kind', choices=['main', 'baseline', 'ablation', 'generalization', 'all'], default='all')
    parser.add_argument('--split', choices=['dev', 'test'], default='test')
    parser.add_argument('--output-root', default=None)
    args = parser.parse_args()

    config = load_runtime_config(base_dir=ROOT, output_root=args.output_root)
    OUTPUTS_ROOT = config.paths.outputs
    table_dir = OUTPUTS_ROOT / 'reports' / args.split / 'tables'
    table_dir.mkdir(parents=True, exist_ok=True)

    mapping = {
        'main': flatten_main,
        'baseline': flatten_baseline,
        'ablation': flatten_ablation,
        'generalization': flatten_generalization,
    }
    kinds = list(mapping) if args.kind == 'all' else [args.kind]
    exported = {}

    for kind in kinds:
        rows = mapping[kind](args.split)
        csv_path = table_dir / (f'{kind}_summary_table.csv' if kind != 'generalization' else 'generalization_by_category.csv')
        md_path = table_dir / (f'{kind}_summary_table.md' if kind != 'generalization' else 'generalization_by_category.md')
        write_csv(csv_path, rows)
        write_md(md_path, rows)
        exported[kind] = {
            'rows': len(rows),
            'csv': display_path(csv_path),
            'md': display_path(md_path),
        }

    print(json.dumps({'split': args.split, 'exported': exported}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
