from __future__ import annotations

from ..parser import verification_references
from ..schemas import CheckResult, ParsedTrace


REQUIRED_TABLE_COLUMNS = {
    "test_id",
    "technique",
    "requirement_target",
    "preconditions",
    "input_data",
    "expected_output",
    "covered_item",
    "priority",
    "checker_status",
}


def check_schema(parsed: ParsedTrace) -> CheckResult:
    diagnostics: list[str] = []
    if parsed.missing_sections:
        diagnostics.append(f"missing sections: {', '.join(parsed.missing_sections)}")
    if not parsed.steps:
        diagnostics.append("steps section is empty")
    refs = verification_references(parsed.verification)
    if parsed.steps and not refs:
        diagnostics.append("verification section does not reference any earlier step")
    invalid_refs = [ref for ref in refs if ref < 1 or ref > len(parsed.steps)]
    if invalid_refs:
        diagnostics.append(f"verification references invalid step numbers: {invalid_refs}")
    if not parsed.test_cases:
        diagnostics.append("final answer does not contain any parseable test cases")
    else:
        first_case_columns = set(parsed.test_cases[0].__dict__.keys())
        missing_columns = REQUIRED_TABLE_COLUMNS - first_case_columns
        if missing_columns:
            diagnostics.append(f"missing table columns after parsing: {sorted(missing_columns)}")
    passed = not diagnostics
    score = 1.0 if passed else 0.5 if parsed.test_cases else 0.0
    return CheckResult(name="schema", passed=passed, score=score, diagnostics=diagnostics)
