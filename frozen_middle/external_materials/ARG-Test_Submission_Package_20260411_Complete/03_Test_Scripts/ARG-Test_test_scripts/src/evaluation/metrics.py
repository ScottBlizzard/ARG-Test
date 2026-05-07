from __future__ import annotations

import re
from pathlib import Path

from ..schemas import TestCase
from ..utils import duplicate_count, load_json, normalize_text

STOPWORDS = {
    'the', 'and', 'for', 'with', 'that', 'this', 'only', 'when', 'must', 'from', 'into', 'than', 'then', 'not', 'all', 'any'
}

COVERAGE_FIELDS = {
    'valid_partition_coverage': 'valid_partitions',
    'invalid_partition_coverage': 'invalid_partitions',
    'boundary_coverage': 'boundaries',
    'decision_rule_coverage': 'decision_rules',
    'state_coverage': 'states',
    'illegal_transition_coverage': 'illegal_transitions',
    'exception_coverage': 'exception_cases',
}


def _texts(test_cases: list[TestCase]) -> list[str]:
    return [normalize_text(f"{case.technique} {case.covered_item} {case.input_data} {case.expected_output}") for case in test_cases]


def _tokens(value: str) -> list[str]:
    return [token for token in re.findall(r"[a-zA-Z0-9]+", value.lower()) if token not in STOPWORDS and len(token) > 1]


def _match_item(item: str, texts: list[str]) -> bool:
    tokens = _tokens(item)
    if not tokens:
        return False
    threshold = min(len(tokens), 2)
    for text in texts:
        if sum(token in text for token in tokens) >= threshold:
            return True
    return False


def _match_boundary(boundary: dict, texts: list[str]) -> bool:
    points = [str(point) for point in boundary.get('points', [])]
    field = normalize_text(str(boundary.get('field', '')))
    for text in texts:
        if field and field not in text:
            continue
        if any(point in text for point in points):
            return True
    return False


def _coverage_ratio(items: list, matcher) -> float | None:
    if not items:
        return None
    covered = sum(1 for item in items if matcher(item))
    return round(covered / len(items), 3)


def evaluate_suite(test_cases: list[TestCase], gold_spec_path: Path | None) -> dict:
    if gold_spec_path is None or not gold_spec_path.exists():
        return {
            'gold_spec_found': False,
            'test_count': len(test_cases),
            'duplicate_count': duplicate_count(test_cases),
            'coverage': {},
            'applicable_dimensions': [],
            'applicable_dimension_count': 0,
            'overall_coverage': 0.0,
        }
    gold = load_json(gold_spec_path)
    texts = _texts(test_cases)
    coverage = {
        'valid_partition_coverage': _coverage_ratio(gold.get('valid_partitions', []), lambda item: _match_item(item, texts)),
        'invalid_partition_coverage': _coverage_ratio(gold.get('invalid_partitions', []), lambda item: _match_item(item, texts)),
        'boundary_coverage': _coverage_ratio(gold.get('boundaries', []), lambda item: _match_boundary(item, texts)),
        'decision_rule_coverage': _coverage_ratio(gold.get('decision_rules', []), lambda item: _match_item(item, texts)),
        'state_coverage': _coverage_ratio(gold.get('states', []), lambda item: _match_item(item, texts)),
        'illegal_transition_coverage': _coverage_ratio(gold.get('illegal_transitions', []), lambda item: _match_item(item, texts)),
        'exception_coverage': _coverage_ratio(gold.get('exception_cases', []), lambda item: _match_item(item, texts)),
    }
    applicable_dimensions = [name for name, spec_field in COVERAGE_FIELDS.items() if gold.get(spec_field, [])]
    applicable_values = [coverage[name] for name in applicable_dimensions if coverage[name] is not None]
    overall = round(sum(applicable_values) / len(applicable_values), 3) if applicable_values else 0.0
    return {
        'gold_spec_found': True,
        'requirement_id': gold.get('requirement_id'),
        'test_count': len(test_cases),
        'duplicate_count': duplicate_count(test_cases),
        'coverage': coverage,
        'applicable_dimensions': applicable_dimensions,
        'applicable_dimension_count': len(applicable_dimensions),
        'overall_coverage': overall,
    }
