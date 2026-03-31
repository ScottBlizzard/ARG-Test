from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.pipeline import ARGTestPipeline
from src.utils import list_requirement_files, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description='Run the full ARG-Test pipeline over a split.')
    parser.add_argument('--split', choices=['dev', 'test'], default='dev')
    parser.add_argument('--provider', default='mock')
    parser.add_argument('--model', default='mock-arg-test')
    parser.add_argument('--candidates', type=int, default=3)
    parser.add_argument('--limit', type=int, default=0)
    args = parser.parse_args()

    pipeline = ARGTestPipeline(base_dir=ROOT, provider=args.provider, model=args.model, candidates=args.candidates)
    requirement_files = list_requirement_files(ROOT, args.split)
    if args.limit:
        requirement_files = requirement_files[: args.limit]

    summaries = [pipeline.process_requirement_file(path, candidates=args.candidates) for path in requirement_files]
    report_path = ROOT / 'outputs' / 'reports' / args.split / 'run_main_summary.json'
    write_json(report_path, summaries)
    print(json.dumps(summaries, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
