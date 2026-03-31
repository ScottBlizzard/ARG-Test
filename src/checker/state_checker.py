from __future__ import annotations

from ..schemas import CheckResult, ParsedTrace
from ..utils import normalize_text


STATE_MARKERS = ["state", "transition", "locked", "approved", "rejected", "draft", "submitted"]


def check_state_transition(parsed: ParsedTrace) -> CheckResult:
    applicable = "State Transition" in parsed.selected_techniques() or "state" in parsed.analysis.lower() or "transition" in parsed.pattern.lower()
    if not applicable:
        return CheckResult(name="state_contract", passed=True, score=1.0, diagnostics=["not applicable"])
    combined = [normalize_text(f"{case.covered_item} {case.expected_output} {case.input_data}") for case in parsed.test_cases]
    has_legal = any("legal" in text or "succeeds" in text or "approved" in text for text in combined)
    has_illegal = any("illegal" in text or "reject" in text or "locked" in text for text in combined)
    diagnostics: list[str] = []
    if not any(marker in parsed.analysis.lower() or marker in " ".join(parsed.steps).lower() for marker in STATE_MARKERS):
        diagnostics.append("analysis and steps do not clearly model states or transitions")
    if not has_legal:
        diagnostics.append("missing legal transition test")
    if not has_illegal:
        diagnostics.append("missing illegal transition test")
    passed = not diagnostics
    score = 1.0 if passed else 0.5 if has_legal or has_illegal else 0.0
    return CheckResult(name="state_contract", passed=passed, score=score, diagnostics=diagnostics)
