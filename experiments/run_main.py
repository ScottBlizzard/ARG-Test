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
    return {item.strip() for item in raw.split(',') if item.strip()}


def summary_order_for_split(split: str) -> list[str]:
    ordered_ids = []
    for path in list_requirement_files(ROOT, split):
        requirement_text = read_text(path)
        ordered_ids.append(extract_requirement_id(requirement_text, path.stem))
    return ordered_ids


def merge_with_existing(report_path: Path, split: str, new_summaries: list[dict]) -> list[dict]:
    if not report_path.exists():
        return new_summaries
    existing = json.loads(report_path.read_text(encoding='utf-8'))
    by_id = {item['requirement_id']: item for item in existing}
    for item in new_summaries:
        by_id[item['requirement_id']] = item
    ordered_ids = summary_order_for_split(split)
    merged = [by_id[requirement_id] for requirement_id in ordered_ids if requirement_id in by_id]
    extras = [item for requirement_id, item in by_id.items() if requirement_id not in set(ordered_ids)]
    return merged + extras


def main() -> None:
    parser = argparse.ArgumentParser(description='Run the full ARG-Test pipeline over a split.')
    parser.add_argument('--split', choices=['dev', 'test'], default='dev')
    parser.add_argument('--provider', default='mock')
    parser.add_argument('--model', default='mock-arg-test')
    parser.add_argument('--candidates', type=int, default=3)
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--ids', default='', help='Comma-separated requirement_ids for targeted rerun.')
    parser.add_argument('--output-root', default=None)
    args = parser.parse_args()

    pipeline = ARGTestPipeline(
        base_dir=ROOT,
        provider=args.provider,
        model=args.model,
        candidates=args.candidates,
        output_root=args.output_root,
    )
    requirement_files = list_requirement_files(ROOT, args.split)
    selected_ids = parse_ids(args.ids)
    if selected_ids:
        requirement_files = [
            path for path in requirement_files
            if extract_requirement_id(read_text(path), path.stem) in selected_ids
        ]
    if args.limit:
        requirement_files = requirement_files[: args.limit]

    summaries = [pipeline.process_requirement_file(path, candidates=args.candidates) for path in requirement_files]
    report_path = pipeline.config.paths.outputs / 'reports' / args.split / 'run_main_summary.json'
    if selected_ids:
        summaries = merge_with_existing(report_path, args.split, summaries)
    write_json(report_path, summaries)
    manifest = build_run_manifest(
        experiment='run_main',
        split=args.split,
        provider=pipeline.config.provider,
        model=pipeline.config.model,
        candidates=args.candidates,
        enable_repair=pipeline.config.enable_repair,
        runtime_root=pipeline.config.paths.runtime_root,
        requirement_ids=[item['requirement_id'] for item in summaries],
        extra={
            'limit': args.limit,
            'targeted_ids': sorted(selected_ids),
            'merged_with_existing': bool(selected_ids),
            'output_summary_path': str(report_path),
        },
    )
    write_json(pipeline.config.paths.outputs / 'reports' / args.split / 'run_main_manifest.json', manifest)
    print(json.dumps(summaries, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
