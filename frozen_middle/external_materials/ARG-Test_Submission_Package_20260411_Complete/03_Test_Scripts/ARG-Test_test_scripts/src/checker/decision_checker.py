from __future__ import annotations

from ..schemas import CheckResult, ParsedTrace
from ..utils import normalize_text


RULE_MARKERS = ["rule", "decision", "coupon", "otp", "refund", "free shipping"]


def check_decision_table(parsed: ParsedTrace) -> CheckResult:
    applicable = "Decision Table" in parsed.selected_techniques() or "decision" in parsed.pattern.lower() or "rule" in parsed.analysis.lower()
    if not applicable:
        return CheckResult(name="decision_contract", passed=True, score=1.0, diagnostics=["not applicable"])
    diagnostics: list[str] = []
    if "rule" not in parsed.pattern.lower() and "rule" not in " ".join(parsed.steps).lower():
        diagnostics.append("pattern or steps do not explain rule mapping")
    combined = [normalize_text(f"{case.covered_item} {case.expected_output} {case.input_data}") for case in parsed.test_cases]
    rule_case_count = sum(any(marker in text for marker in RULE_MARKERS) for text in combined)
    if rule_case_count == 0:
        diagnostics.append("no rule-oriented test case was found")
    if rule_case_count < 2:
        diagnostics.append("decision table coverage appears shallow")
    passed = not diagnostics
    score = 1.0 if passed else 0.5 if rule_case_count else 0.0
    return CheckResult(name="decision_contract", passed=passed, score=score, diagnostics=diagnostics)
