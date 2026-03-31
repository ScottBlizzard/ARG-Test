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
from src.utils import extract_requirement_id, gold_spec_path, list_requirement_files, read_text, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description='Compare structured-no-checker against the full pipeline.')
    parser.add_argument('--split', choices=['dev', 'test'], default='test')
    parser.add_argument('--provider', default='mock')
    parser.add_argument('--model', default='mock-arg-test')
    parser.add_argument('--candidates', type=int, default=3)
    args = parser.parse_args()

    pipeline = ARGTestPipeline(base_dir=ROOT, provider=args.provider, model=args.model, candidates=args.candidates)
    summaries = []

    for path in list_requirement_files(ROOT, args.split):
        requirement_text = read_text(path)
        requirement_id = extract_requirement_id(requirement_text, path.stem)
        gold_path = gold_spec_path(ROOT, args.split, requirement_id)

        baseline_trace = build_structured_no_checker_trace(requirement_id, requirement_text, pipeline.client, pipeline.generation_prompt(requirement_text))
        baseline_candidate = pipeline.assess_trace(baseline_trace, source='structured_no_checker', repaired=False)
        baseline_metrics = evaluate_suite(baseline_trace.test_cases, gold_path)
        baseline_metrics['checker_score'] = baseline_candidate.score

        full_summary = pipeline.process_requirement_file(path, candidates=args.candidates)
        summaries.append(
            {
                'requirement_id': requirement_id,
                'split': args.split,
                'structured_no_checker': baseline_metrics,
                'full_pipeline': full_summary['metrics'],
            }
        )

    output_path = ROOT / 'outputs' / 'reports' / args.split / 'ablation_summary.json'
    write_json(output_path, summaries)
    print(json.dumps(summaries, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
