from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils import extract_requirement_id, load_json, read_text, write_json

REQUIRED_GOLD_FIELDS = [
    'requirement_id',
    'recommended_techniques',
    'valid_partitions',
    'invalid_partitions',
    'boundaries',
    'decision_rules',
    'states',
    'illegal_transitions',
    'exception_cases',
]


def validate_split(split: str) -> dict:
    requirement_dir = ROOT / 'data' / 'requirements' / split
    gold_dir = ROOT / 'data' / 'gold_specs' / split
    requirement_files = sorted(requirement_dir.glob('*.txt'))
    gold_files = sorted(gold_dir.glob('*.json'))

    errors: list[str] = []
    warnings: list[str] = []
    requirement_ids: dict[str, str] = {}
    gold_ids: dict[str, str] = {}

    for path in requirement_files:
        text = read_text(path)
        requirement_id = extract_requirement_id(text, path.stem)
        if 'Requirement ID:' not in text:
            errors.append(f'{split}: {path.name} is missing an explicit Requirement ID header')
        if requirement_id in requirement_ids:
            errors.append(f'{split}: duplicate requirement ID {requirement_id} in {path.name} and {requirement_ids[requirement_id]}')
        requirement_ids[requirement_id] = path.name

    for path in gold_files:
        payload = load_json(path)
        requirement_id = str(payload.get('requirement_id', '')).strip()
        if not requirement_id:
            errors.append(f'{split}: {path.name} is missing requirement_id')
            continue
        if requirement_id in gold_ids:
            errors.append(f'{split}: duplicate gold spec requirement_id {requirement_id} in {path.name} and {gold_ids[requirement_id]}')
        gold_ids[requirement_id] = path.name
        missing_fields = [field for field in REQUIRED_GOLD_FIELDS if field not in payload]
        if missing_fields:
            errors.append(f'{split}: {path.name} is missing fields {missing_fields}')
        if path.stem != requirement_id:
            warnings.append(f'{split}: gold spec filename {path.stem} does not match requirement_id {requirement_id}')

    missing_gold = sorted(set(requirement_ids) - set(gold_ids))
    extra_gold = sorted(set(gold_ids) - set(requirement_ids))
    for item in missing_gold:
        errors.append(f'{split}: requirement {item} has no matching gold spec')
    for item in extra_gold:
        errors.append(f'{split}: gold spec {item} has no matching requirement file')

    return {
        'split': split,
        'requirement_count': len(requirement_files),
        'gold_spec_count': len(gold_files),
        'missing_gold_specs': missing_gold,
        'orphan_gold_specs': extra_gold,
        'errors': errors,
        'warnings': warnings,
        'passed': not errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Validate requirement and gold spec assets.')
    parser.add_argument('--split', choices=['dev', 'test', 'all'], default='all')
    args = parser.parse_args()

    splits = ['dev', 'test'] if args.split == 'all' else [args.split]
    results = [validate_split(split) for split in splits]
    overall = {
        'split': args.split,
        'passed': all(item['passed'] for item in results),
        'results': results,
    }

    qa_dir = ROOT / 'outputs' / 'reports' / 'qa'
    qa_dir.mkdir(parents=True, exist_ok=True)
    output_path = qa_dir / f'data_validation_{args.split}.json'
    write_json(output_path, overall)
    print(json.dumps(overall, indent=2, ensure_ascii=False))

    if not overall['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
