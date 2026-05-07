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

DEFAULT_IDS = [
    'bundle_discount_eligibility_rules',
    'return_refund_method_eligibility',
    'pickup_station_contact_validation',
    'payment_card_expiry_and_cvv_validation',
    'payment_3ds_authentication_flow',
]


def parse_ids(raw: str) -> list[str]:
    if not raw.strip():
        return DEFAULT_IDS.copy()
    return [item.strip() for item in raw.split(',') if item.strip()]


def requirement_file_map(split: str) -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for path in list_requirement_files(ROOT, split):
        requirement_id = extract_requirement_id(read_text(path), path.stem)
        mapping[requirement_id] = path
    return mapping


def avg(values: list[float]) -> float:
    return round(sum(values) / len(values), 3) if values else 0.0


def build_markdown(payload: dict) -> str:
    lines = [
        '# Stability Sanity Check',
        '',
        f"- Split: `{payload['split']}`",
        f"- Selected requirements: `{', '.join(payload['selected_ids'])}`",
        f"- Stable cases (|Δscore|<=0.05 and |Δcoverage|<=0.10): `{payload['stable_case_count']}/{payload['count']}`",
        f"- Formal avg score: `{payload['formal_avg_score']}` -> Rerun avg score: `{payload['rerun_avg_score']}`",
        f"- Formal avg coverage: `{payload['formal_avg_coverage']}` -> Rerun avg coverage: `{payload['rerun_avg_coverage']}`",
        f"- Avg absolute score delta: `{payload['avg_abs_score_delta']}`",
        f"- Avg absolute coverage delta: `{payload['avg_abs_coverage_delta']}`",
        '',
        '| Requirement | Category | Formal Score | Rerun Score | Delta | Formal Coverage | Rerun Coverage | Delta | Stable |',
        '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |',
    ]
    for item in payload['comparisons']:
        lines.append(
            f"| {item['requirement_id']} | {item['category']} | {item['formal_score']:.3f} | {item['rerun_score']:.3f} | {item['score_delta']:+.3f} | {item['formal_coverage']:.3f} | {item['rerun_coverage']:.3f} | {item['coverage_delta']:+.3f} | {'yes' if item['stable'] else 'no'} |"
        )
    return '\n'.join(lines) + '\n'


def main() -> None:
    parser = argparse.ArgumentParser(description='Run a small stability sanity check on selected test requirements.')
    parser.add_argument('--split', choices=['dev', 'test'], default='test')
    parser.add_argument('--provider', default='openai')
    parser.add_argument('--model', default='qwen3.5-flash')
    parser.add_argument('--candidates', type=int, default=3)
    parser.add_argument('--ids', default='', help='Comma-separated requirement_ids. Defaults to a representative 5-case set.')
    parser.add_argument('--output-root', required=True, help='Isolated runtime root for the sanity rerun.')
    parser.add_argument('--formal-root', default='.local_runs/formal_qwen_novpn', help='Runtime root of the frozen formal results.')
    args = parser.parse_args()

    selected_ids = parse_ids(args.ids)
    files_by_id = requirement_file_map(args.split)
    missing = [rid for rid in selected_ids if rid not in files_by_id]
    if missing:
        raise SystemExit(f'Missing requirement ids for split {args.split}: {missing}')

    pipeline = ARGTestPipeline(
        base_dir=ROOT,
        provider=args.provider,
        model=args.model,
        candidates=args.candidates,
        output_root=args.output_root,
    )

    rerun_summaries = [pipeline.process_requirement_file(files_by_id[rid], candidates=args.candidates) for rid in selected_ids]

    formal_summary_path = ROOT / args.formal_root / 'outputs' / 'reports' / args.split / 'run_main_summary.json'
    formal_summaries = json.loads(formal_summary_path.read_text(encoding='utf-8'))
    formal_by_id = {item['requirement_id']: item for item in formal_summaries}

    comparisons = []
    abs_score_deltas: list[float] = []
    abs_coverage_deltas: list[float] = []
    for item in rerun_summaries:
        requirement_id = item['requirement_id']
        formal = formal_by_id[requirement_id]
        formal_score = float(formal['score'])
        rerun_score = float(item['score'])
        formal_coverage = float(formal['metrics']['overall_coverage'])
        rerun_coverage = float(item['metrics']['overall_coverage'])
        score_delta = rerun_score - formal_score
        coverage_delta = rerun_coverage - formal_coverage
        stable = abs(score_delta) <= 0.05 and abs(coverage_delta) <= 0.10
        abs_score_deltas.append(abs(score_delta))
        abs_coverage_deltas.append(abs(coverage_delta))
        comparisons.append(
            {
                'requirement_id': requirement_id,
                'category': requirement_category(ROOT, args.split, requirement_id),
                'formal_score': round(formal_score, 3),
                'rerun_score': round(rerun_score, 3),
                'score_delta': round(score_delta, 3),
                'formal_coverage': round(formal_coverage, 3),
                'rerun_coverage': round(rerun_coverage, 3),
                'coverage_delta': round(coverage_delta, 3),
                'formal_test_count': formal['metrics']['test_count'],
                'rerun_test_count': item['metrics']['test_count'],
                'stable': stable,
            }
        )

    payload = {
        'split': args.split,
        'selected_ids': selected_ids,
        'count': len(comparisons),
        'stable_case_count': sum(1 for item in comparisons if item['stable']),
        'formal_avg_score': avg([float(formal_by_id[rid]['score']) for rid in selected_ids]),
        'rerun_avg_score': avg([float(item['score']) for item in rerun_summaries]),
        'formal_avg_coverage': avg([float(formal_by_id[rid]['metrics']['overall_coverage']) for rid in selected_ids]),
        'rerun_avg_coverage': avg([float(item['metrics']['overall_coverage']) for item in rerun_summaries]),
        'avg_abs_score_delta': round(statistics.mean(abs_score_deltas), 3) if abs_score_deltas else 0.0,
        'avg_abs_coverage_delta': round(statistics.mean(abs_coverage_deltas), 3) if abs_coverage_deltas else 0.0,
        'comparisons': comparisons,
    }

    report_dir = ROOT / args.output_root / 'outputs' / 'reports' / args.split
    report_dir.mkdir(parents=True, exist_ok=True)
    write_json(report_dir / 'stability_sanity_summary.json', payload)
    (report_dir / 'stability_sanity_summary.md').write_text(build_markdown(payload), encoding='utf-8')
    manifest = build_run_manifest(
        experiment='run_stability_sanity',
        split=args.split,
        provider=pipeline.config.provider,
        model=pipeline.config.model,
        candidates=args.candidates,
        enable_repair=pipeline.config.enable_repair,
        runtime_root=pipeline.config.paths.runtime_root,
        requirement_ids=selected_ids,
        extra={
            'formal_root': args.formal_root,
            'output_summary_path': str(report_dir / 'stability_sanity_summary.json'),
        },
    )
    write_json(report_dir / 'stability_sanity_manifest.json', manifest)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
