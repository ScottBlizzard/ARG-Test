from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import load_runtime_config


def main() -> None:
    parser = argparse.ArgumentParser(description='Validate runtime configuration before a formal run.')
    parser.add_argument('--provider', default=None)
    parser.add_argument('--model', default=None)
    parser.add_argument('--candidates', type=int, default=None)
    parser.add_argument('--output-root', default=None)
    args = parser.parse_args()

    config = load_runtime_config(
        base_dir=ROOT,
        provider=args.provider,
        model=args.model,
        candidates=args.candidates,
        output_root=args.output_root,
    )
    runtime_root = config.paths.runtime_root
    runtime_root.mkdir(parents=True, exist_ok=True)

    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    base_url = os.getenv('OPENAI_BASE_URL', '').strip()
    if config.provider.lower() == 'openai' and not api_key:
        raise SystemExit('OPENAI_API_KEY is required when ARG_TEST_PROVIDER=openai or --provider openai')

    payload = {
        'provider': config.provider,
        'model': config.model,
        'candidates': config.candidates,
        'enable_repair': config.enable_repair,
        'project_root': str(config.paths.root),
        'runtime_root': str(config.paths.runtime_root),
        'outputs_dir': str(config.paths.outputs),
        'artifacts_dir': str(config.paths.artifacts),
        'env_file': str(config.paths.env_file),
        'has_openai_api_key': bool(api_key),
        'has_openai_base_url': bool(base_url),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
