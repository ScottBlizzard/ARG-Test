from __future__ import annotations

from ..schemas import CheckResult, ParsedTrace
from ..utils import normalize_text


def check_bva(parsed: ParsedTrace) -> CheckResult:
    applicable = "BVA" in parsed.selected_techniques() or "boundary" in parsed.pattern.lower() or "boundary" in parsed.analysis.lower()
    if not applicable:
        return CheckResult(name="bva_contract", passed=True, score=1.0, diagnostics=["not applicable"])
    combined = [normalize_text(f"{case.covered_item} {case.input_data}") for case in parsed.test_cases]
    lower = any("lower" in text or "below" in text or "min" in text for text in combined)
    upper = any("upper" in text or "above" in text or "max" in text for text in combined)
    on_boundary = any("boundary" in text or "on " in text for text in combined)
    diagnostics: list[str] = []
    if not lower:
        diagnostics.append("missing lower-boundary or just-below case")
    if not upper:
        diagnostics.append("missing upper-boundary or just-above case")
    if not on_boundary:
        diagnostics.append("missing on-boundary case")
    passed = not diagnostics
    score = 1.0 if passed else 0.5 if lower or upper or on_boundary else 0.0
    return CheckResult(name="bva_contract", passed=passed, score=score, diagnostics=diagnostics)
