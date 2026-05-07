from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .input_loader import load_requirements_from_csv
from .pipeline import ARGTestPipeline
from .utils import list_requirement_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='ARG-Test CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    run_parser = subparsers.add_parser('run', help='Run the full pipeline for one requirement file')
    run_parser.add_argument('--input', required=True, help='Path to a requirement file')
    run_parser.add_argument('--provider', default='mock')
    run_parser.add_argument('--model', default='mock-arg-test')
    run_parser.add_argument('--candidates', type=int, default=3)
    run_parser.add_argument('--output-root', default=None)

    run_text_parser = subparsers.add_parser('run-text', help='Run the full pipeline for direct text input')
    run_text_parser.add_argument('--text', default=None, help='Requirement text. If omitted, read from stdin.')
    run_text_parser.add_argument('--requirement-id', default=None)
    run_text_parser.add_argument('--split', default='adhoc')
    run_text_parser.add_argument('--provider', default='mock')
    run_text_parser.add_argument('--model', default='mock-arg-test')
    run_text_parser.add_argument('--candidates', type=int, default=3)
    run_text_parser.add_argument('--output-root', default=None)

    batch_parser = subparsers.add_parser('batch', help='Run the full pipeline for a split')
    batch_parser.add_argument('--split', choices=['dev', 'test'], required=True)
    batch_parser.add_argument('--provider', default='mock')
    batch_parser.add_argument('--model', default='mock-arg-test')
    batch_parser.add_argument('--candidates', type=int, default=3)
    batch_parser.add_argument('--limit', type=int, default=0)
    batch_parser.add_argument('--output-root', default=None)

    batch_csv_parser = subparsers.add_parser('batch-csv', help='Run the pipeline for requirements loaded from CSV')
    batch_csv_parser.add_argument('--input', required=True, help='Path to a CSV file with requirement rows')
    batch_csv_parser.add_argument('--text-column', default='requirement_text')
    batch_csv_parser.add_argument('--id-column', default='requirement_id')
    batch_csv_parser.add_argument('--split-column', default='split')
    batch_csv_parser.add_argument('--default-split', default='adhoc')
    batch_csv_parser.add_argument('--provider', default='mock')
    batch_csv_parser.add_argument('--model', default='mock-arg-test')
    batch_csv_parser.add_argument('--candidates', type=int, default=3)
    batch_csv_parser.add_argument('--output-root', default=None)

    state_model_parser = subparsers.add_parser('state-model', help='Build a state-transition model from a requirement file or direct text')
    state_model_parser.add_argument('--input', default=None, help='Path to a requirement file')
    state_model_parser.add_argument('--text', default=None, help='Requirement text. If omitted and --input is absent, read from stdin.')
    state_model_parser.add_argument('--requirement-id', default=None)
    state_model_parser.add_argument('--split', default='adhoc')
    state_model_parser.add_argument('--provider', default='mock')
    state_model_parser.add_argument('--model', default='mock-arg-test')
    state_model_parser.add_argument('--candidates', type=int, default=3)
    state_model_parser.add_argument('--output-root', default=None)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    pipeline = ARGTestPipeline(
        provider=args.provider,
        model=args.model,
        candidates=args.candidates,
        output_root=args.output_root,
    )

    if args.command == 'run':
        summary = pipeline.process_requirement_file(Path(args.input), candidates=args.candidates)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return

    if args.command == 'run-text':
        requirement_text = args.text if args.text is not None else sys.stdin.read()
        summary = pipeline.process_requirement_text(
            requirement_text,
            requirement_id=args.requirement_id,
            split=args.split,
            candidates=args.candidates,
        )
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return

    if args.command == 'batch-csv':
        records = load_requirements_from_csv(
            Path(args.input),
            text_column=args.text_column,
            id_column=args.id_column,
            split_column=args.split_column,
            default_split=args.default_split,
        )
        summaries = [
            pipeline.process_requirement_text(
                record.requirement_text,
                requirement_id=record.requirement_id,
                split=record.split,
                candidates=args.candidates,
            )
            for record in records
        ]
        print(json.dumps(summaries, indent=2, ensure_ascii=False))
        return

    if args.command == 'state-model':
        if args.input:
            summary = pipeline.process_requirement_file(Path(args.input), candidates=args.candidates)
        else:
            requirement_text = args.text if args.text is not None else sys.stdin.read()
            summary = pipeline.process_requirement_text(
                requirement_text,
                requirement_id=args.requirement_id,
                split=args.split,
                candidates=args.candidates,
            )
        print(json.dumps(summary.get('state_model'), indent=2, ensure_ascii=False))
        return

    files = list_requirement_files(pipeline.config.paths.root, args.split)
    if args.limit:
        files = files[: args.limit]
    summaries = [pipeline.process_requirement_file(path, candidates=args.candidates) for path in files]
    print(json.dumps(summaries, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
