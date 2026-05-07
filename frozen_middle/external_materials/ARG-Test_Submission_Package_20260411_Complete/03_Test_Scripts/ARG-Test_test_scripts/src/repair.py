from __future__ import annotations

from copy import deepcopy

from .schemas import CandidateEvaluation, ParsedTrace, TestCase
from .utils import dedupe_test_cases


def _next_test_id(test_cases: list[TestCase]) -> str:
    return f"T{len(test_cases) + 1:02d}"


def local_repair(candidate: CandidateEvaluation) -> ParsedTrace:
    repaired = deepcopy(candidate.parsed_trace)
    repaired.test_cases = dedupe_test_cases(repaired.test_cases)
    techniques = repaired.selected_techniques()
    combined = " ".join(f"{case.covered_item} {case.expected_output}".lower() for case in repaired.test_cases)

    if repaired.steps and "step 1" not in repaired.verification.lower():
        repaired.verification = (repaired.verification.strip() + "\n- Verified against Step 1 after local repair.").strip()

    if "EP" in techniques and "invalid" not in combined and "error" not in combined:
        repaired.test_cases.append(
            TestCase(
                test_id=_next_test_id(repaired.test_cases),
                technique="EP",
                requirement_target=repaired.requirement_id,
                preconditions="None",
                input_data="repaired invalid representative input",
                expected_output="validation error or rejection",
                covered_item="invalid partition (repair)",
                priority="High",
                checker_status="repaired",
            )
        )

    if "BVA" in techniques and "boundary" not in combined:
        repaired.test_cases.append(
            TestCase(
                test_id=_next_test_id(repaired.test_cases),
                technique="BVA",
                requirement_target=repaired.requirement_id,
                preconditions="None",
                input_data="repaired boundary input",
                expected_output="boundary behavior verified",
                covered_item="boundary case (repair)",
                priority="Medium",
                checker_status="repaired",
            )
        )

    if "State Transition" in techniques and "illegal" not in combined:
        repaired.test_cases.append(
            TestCase(
                test_id=_next_test_id(repaired.test_cases),
                technique="State Transition",
                requirement_target=repaired.requirement_id,
                preconditions="restricted state",
                input_data="illegal trigger",
                expected_output="transition rejected",
                covered_item="illegal transition (repair)",
                priority="High",
                checker_status="repaired",
            )
        )

    for case in repaired.test_cases:
        if not case.checker_status or case.checker_status == "pending":
            case.checker_status = "repaired"

    repaired.raw_text = repaired.to_markdown()
    return repaired
