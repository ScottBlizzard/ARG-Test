from __future__ import annotations

from .schemas import CandidateEvaluation
from .utils import duplicate_count


def aggregate_score(candidate: CandidateEvaluation) -> float:
    scores = [check.score for check in candidate.checks]
    base = sum(scores) / len(scores) if scores else 0.0
    penalty = min(0.2, duplicate_count(candidate.parsed_trace.test_cases) * 0.05)
    bonus = 0.05 if len(candidate.parsed_trace.selected_techniques()) > 1 else 0.0
    return max(0.0, min(1.0, base - penalty + bonus))


def select_best(candidates: list[CandidateEvaluation]) -> CandidateEvaluation:
    ranked = sorted(
        candidates,
        key=lambda item: (item.score, len(item.parsed_trace.test_cases), -len(item.diagnostics())),
        reverse=True,
    )
    return ranked[0]
