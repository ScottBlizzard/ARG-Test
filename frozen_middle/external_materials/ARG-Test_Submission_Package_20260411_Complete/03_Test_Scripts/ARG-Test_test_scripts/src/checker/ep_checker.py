from __future__ import annotations

from ..schemas import CheckResult, ParsedTrace
from ..utils import normalize_text


VALID_MARKERS = ["valid", "accepted", "success", "created"]
INVALID_MARKERS = ["invalid", "reject", "error", "locked", "failed"]


def check_ep(parsed: ParsedTrace) -> CheckResult:
    applicable = "EP" in parsed.selected_techniques() or "partition" in parsed.analysis.lower() or "partition" in parsed.pattern.lower()
    if not applicable:
        return CheckResult(name="ep_contract", passed=True, score=1.0, diagnostics=["not applicable"])
    combined = [
        normalize_text(f"{case.covered_item} {case.expected_output} {case.input_data}")
        for case in parsed.test_cases
    ]
    has_valid = any(any(marker in text for marker in VALID_MARKERS) for text in combined)
    has_invalid = any(any(marker in text for marker in INVALID_MARKERS) for text in combined)
    diagnostics: list[str] = []
    if not has_valid:
        diagnostics.append("no representative valid partition was found")
    if not has_invalid:
        diagnostics.append("no representative invalid partition was found")
    unique_targets = {normalize_text(case.covered_item) for case in parsed.test_cases if case.covered_item.strip()}
    if len(unique_targets) < 2:
        diagnostics.append("partition coverage looks too narrow")
    passed = not diagnostics
    score = 1.0 if passed else 0.5 if has_valid or has_invalid else 0.0
    return CheckResult(name="ep_contract", passed=passed, score=score, diagnostics=diagnostics)
