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
from src.utils import build_run_manifest, extract_requirement_id, gold_spec_path, list_requirement_files, read_text, write_json


def add_runtime_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--provider', default='mock')
    parser.add_argument('--model', default='mock-arg-test')
    parser.add_argument('--api-mode', default=None, choices=['responses', 'chat_completions'])
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('--temperature', type=float, default=None)
    parser.add_argument('--top-p', type=float, default=None)


def main() -> None:
    parser = argparse.ArgumentParser(description='Run baseline suites over a requirement split.')
    parser.add_argument('--split', choices=['dev', 'test'], default='test')
    add_runtime_args(parser)
    parser.add_argument('--output-root', default=None)
    args = parser.parse_args()

    pipeline = ARGTestPipeline(
        base_dir=ROOT,
        provider=args.provider,
        model=args.model,
        candidates=1,
        openai_api_mode=args.api_mode,
        seed=args.seed,
        temperature=args.temperature,
        top_p=args.top_p,
        output_root=args.output_root,
    )
    summaries = []
    requirement_ids: list[str] = []

    for path in list_requirement_files(ROOT, args.split):
        requirement_text = read_text(path)
        requirement_id = extract_requirement_id(requirement_text, path.stem)
        requirement_ids.append(requirement_id)
        gold_path = gold_spec_path(ROOT, args.split, requirement_id)
        plain_control = pipeline.build_stage_control(requirement_id, stage='plain_llm_baseline', slot=1)
        structured_control = pipeline.build_stage_control(requirement_id, stage='structured_no_checker_baseline', slot=1)
        traces = {
            'rule_based': build_rule_based_trace(requirement_id, requirement_text),
            'plain_llm': build_plain_llm_trace(
                requirement_id,
                requirement_text,
                pipeline.client,
                pipeline.plain_prompt(requirement_text, plain_control),
                control=plain_control,
            ),
            'structured_no_checker': build_structured_no_checker_trace(
                requirement_id,
                requirement_text,
                pipeline.client,
                pipeline.generation_prompt(requirement_text, structured_control),
                control=structured_control,
            ),
        }
        per_requirement = {'requirement_id': requirement_id, 'split': args.split, 'category': None, 'risk_assessment': None, 'baselines': {}}
        for name, trace in traces.items():
            pipeline.annotate_trace(trace, args.split, requirement_text)
            candidate = pipeline.assess_trace(trace, requirement_text=requirement_text, source=name, repaired=False)
            metrics = evaluate_suite(trace.test_cases, gold_path)
            metrics['checker_score'] = candidate.score
            per_requirement['baselines'][name] = metrics
            if per_requirement['category'] is None:
                per_requirement['category'] = trace.category
            if per_requirement['risk_assessment'] is None and trace.risk_assessment:
                per_requirement['risk_assessment'] = trace.risk_assessment.to_dict()
        summaries.append(per_requirement)

    output_path = pipeline.config.paths.outputs / 'reports' / args.split / 'baseline_summary.json'
    write_json(output_path, summaries)
    manifest = build_run_manifest(
        experiment='run_baselines',
        split=args.split,
        provider=pipeline.config.provider,
        model=pipeline.config.model,
        candidates=1,
        openai_api_mode=pipeline.config.openai_api_mode,
        seed=pipeline.config.seed,
        temperature=pipeline.config.temperature,
        top_p=pipeline.config.top_p,
        enable_repair=False,
        runtime_root=pipeline.config.paths.runtime_root,
        requirement_ids=requirement_ids,
        extra={'output_summary_path': str(output_path)},
    )
    write_json(pipeline.config.paths.outputs / 'reports' / args.split / 'baseline_manifest.json', manifest)
    print(json.dumps(summaries, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
