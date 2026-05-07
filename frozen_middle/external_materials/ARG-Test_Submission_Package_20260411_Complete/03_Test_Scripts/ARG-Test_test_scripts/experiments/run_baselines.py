from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.baselines import build_plain_llm_trace, build_rule_based_trace, build_structured_no_checker_trace
from src.evaluation import evaluate_suite
from src.pipeline import ARGTestPipeline
from src.utils import extract_requirement_id, gold_spec_path, list_requirement_files, read_text, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description='Run baseline suites over a requirement split.')
    parser.add_argument('--split', choices=['dev', 'test'], default='test')
    parser.add_argument('--provider', default='mock')
    parser.add_argument('--model', default='mock-arg-test')
    parser.add_argument('--output-root', default=None)
    args = parser.parse_args()

    pipeline = ARGTestPipeline(base_dir=ROOT, provider=args.provider, model=args.model, candidates=1, output_root=args.output_root)
    summaries = []

    for path in list_requirement_files(ROOT, args.split):
        requirement_text = read_text(path)
        requirement_id = extract_requirement_id(requirement_text, path.stem)
        gold_path = gold_spec_path(ROOT, args.split, requirement_id)
        traces = {
            'rule_based': build_rule_based_trace(requirement_id, requirement_text),
            'plain_llm': build_plain_llm_trace(requirement_id, requirement_text, pipeline.client, pipeline.plain_prompt(requirement_text)),
            'structured_no_checker': build_structured_no_checker_trace(requirement_id, requirement_text, pipeline.client, pipeline.generation_prompt(requirement_text)),
        }
        per_requirement = {'requirement_id': requirement_id, 'split': args.split, 'baselines': {}}
        for name, trace in traces.items():
            pipeline.annotate_trace(trace, args.split)
            candidate = pipeline.assess_trace(trace, source=name, repaired=False)
            metrics = evaluate_suite(trace.test_cases, gold_path)
            metrics['checker_score'] = candidate.score
            per_requirement['baselines'][name] = metrics
        summaries.append(per_requirement)

    output_path = pipeline.config.paths.outputs / 'reports' / args.split / 'baseline_summary.json'
    write_json(output_path, summaries)
    print(json.dumps(summaries, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
