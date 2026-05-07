from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.baselines import build_structured_no_checker_trace
from src.evaluation import evaluate_suite
from src.pipeline import ARGTestPipeline
from src.utils import build_run_manifest, extract_requirement_id, gold_spec_path, list_requirement_files, load_json, read_text, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description='Compare structured-no-checker against the full pipeline.')
    parser.add_argument('--split', choices=['dev', 'test'], default='test')
    parser.add_argument('--provider', default='mock')
    parser.add_argument('--model', default='mock-arg-test')
    parser.add_argument('--candidates', type=int, default=3)
    parser.add_argument('--fresh-full-pipeline', action='store_true', help='Rerun the full pipeline instead of reusing run_main_summary.json when available.')
    parser.add_argument('--output-root', default=None)
    args = parser.parse_args()

    pipeline = ARGTestPipeline(
        base_dir=ROOT,
        provider=args.provider,
        model=args.model,
        candidates=args.candidates,
        output_root=args.output_root,
    )
    main_summary_path = pipeline.config.paths.outputs / 'reports' / args.split / 'run_main_summary.json'
    cached_main = {}
    if main_summary_path.exists() and not args.fresh_full_pipeline:
        cached_main = {item['requirement_id']: item for item in load_json(main_summary_path)}
    summaries = []
    requirement_ids: list[str] = []

    for path in list_requirement_files(ROOT, args.split):
        requirement_text = read_text(path)
        requirement_id = extract_requirement_id(requirement_text, path.stem)
        requirement_ids.append(requirement_id)
        gold_path = gold_spec_path(ROOT, args.split, requirement_id)

        baseline_trace = build_structured_no_checker_trace(
            requirement_id,
            requirement_text,
            pipeline.client,
            pipeline.generation_prompt(requirement_text),
        )
        pipeline.annotate_trace(baseline_trace, args.split, requirement_text)
        baseline_candidate = pipeline.assess_trace(baseline_trace, source='structured_no_checker', repaired=False)
        baseline_metrics = evaluate_suite(baseline_trace.test_cases, gold_path)
        baseline_metrics['checker_score'] = baseline_candidate.score

        if requirement_id in cached_main:
            full_metrics = cached_main[requirement_id]['metrics']
        else:
            full_summary = pipeline.process_requirement_file(path, candidates=args.candidates)
            full_metrics = full_summary['metrics']

        summaries.append(
            {
                'requirement_id': requirement_id,
                'split': args.split,
                'category': baseline_trace.category,
                'risk_assessment': baseline_trace.risk_assessment.to_dict() if baseline_trace.risk_assessment else None,
                'structured_no_checker': baseline_metrics,
                'full_pipeline': full_metrics,
            }
        )

    output_path = pipeline.config.paths.outputs / 'reports' / args.split / 'ablation_summary.json'
    write_json(output_path, summaries)
    manifest = build_run_manifest(
        experiment='run_ablation',
        split=args.split,
        provider=pipeline.config.provider,
        model=pipeline.config.model,
        candidates=args.candidates,
        enable_repair=pipeline.config.enable_repair,
        runtime_root=pipeline.config.paths.runtime_root,
        requirement_ids=requirement_ids,
        extra={
            'fresh_full_pipeline': args.fresh_full_pipeline,
            'output_summary_path': str(output_path),
        },
    )
    write_json(pipeline.config.paths.outputs / 'reports' / args.split / 'ablation_manifest.json', manifest)
    print(json.dumps(summaries, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
