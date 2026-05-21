from __future__ import annotations

import argparse
import json
from pathlib import Path

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

    batch_parser = subparsers.add_parser('batch', help='Run the full pipeline for a split')
    batch_parser.add_argument('--split', choices=['dev', 'test'], required=True)
    batch_parser.add_argument('--provider', default='mock')
    batch_parser.add_argument('--model', default='mock-arg-test')
    batch_parser.add_argument('--candidates', type=int, default=3)
    batch_parser.add_argument('--limit', type=int, default=0)
    batch_parser.add_argument('--output-root', default=None)
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

    files = list_requirement_files(pipeline.config.paths.root, args.split)
    if args.limit:
        files = files[: args.limit]
    summaries = [pipeline.process_requirement_file(path, candidates=args.candidates) for path in files]
    print(json.dumps(summaries, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
