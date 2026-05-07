from __future__ import annotations

from copy import deepcopy

from .schemas import CandidateEvaluation, ParsedTrace, StateTransition, TestCase
from .utils import dedupe_test_cases, extract_numeric_hints, extract_rule_lines, infer_techniques, normalize_text


def _next_test_id(test_cases: list[TestCase]) -> str:
    return f"T{len(test_cases) + 1:02d}"


def _combined_case_text(repaired: ParsedTrace) -> list[str]:
    return [
        normalize_text(f"{case.technique} {case.covered_item} {case.expected_output} {case.input_data} {case.preconditions}")
        for case in repaired.test_cases
    ]


def _append_case(repaired: ParsedTrace, case: TestCase) -> None:
    repaired.test_cases.append(case)


def _renumber_cases(repaired: ParsedTrace) -> None:
    for index, case in enumerate(repaired.test_cases, start=1):
        case.test_id = f"T{index:02d}"


def _ensure_verification_reference(repaired: ParsedTrace) -> None:
    if repaired.steps and "step 1" not in repaired.verification.lower():
        repaired.verification = (repaired.verification.strip() + "\n- Verified against Step 1 after local repair.").strip()


def _ensure_decision_step(repaired: ParsedTrace) -> None:
    lowered_steps = " ".join(repaired.steps).lower()
    if "rule mapping" in lowered_steps or "decision row" in lowered_steps:
        return
    repaired.steps.append(f"{len(repaired.steps) + 1}. Map each explicit rule to a decision-table row and at least one expected outcome.")


def _ensure_state_step(repaired: ParsedTrace) -> None:
    lowered_steps = " ".join(repaired.steps).lower()
    if "legal transition" in lowered_steps or "illegal transition" in lowered_steps:
        return
    repaired.steps.append(f"{len(repaired.steps) + 1}. Enumerate legal and illegal transitions between named states and triggers.")


def _has_lower_boundary(combined: list[str]) -> bool:
    return any("lower" in text or "below" in text or "min" in text for text in combined)


def _has_upper_boundary(combined: list[str]) -> bool:
    return any("upper" in text or "above" in text or "max" in text for text in combined)


def _has_on_boundary(combined: list[str]) -> bool:
    return any("boundary" in text or "on-boundary" in text or "on boundary" in text for text in combined)


def _repair_ep(repaired: ParsedTrace, combined: list[str]) -> None:
    has_invalid = any("invalid" in text or "error" in text or "reject" in text for text in combined)
    if has_invalid:
        return
    _append_case(
        repaired,
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
        ),
    )


def _repair_bva(repaired: ParsedTrace, requirement_text: str, combined: list[str]) -> None:
    numeric_hints = extract_numeric_hints(requirement_text)
    hint = numeric_hints[0] if numeric_hints else {"field": "numeric field", "low": 1, "high": 2}
    field = str(hint.get("field", "numeric field")).strip() or "numeric field"
    low = int(hint.get("low", 1))
    high = int(hint.get("high", low + 1)) if hint.get("high") is not None else low + 1

    if not _has_lower_boundary(combined):
        _append_case(
            repaired,
            TestCase(
                test_id=_next_test_id(repaired.test_cases),
                technique="BVA",
                requirement_target=repaired.requirement_id,
                preconditions="None",
                input_data=f"{field}={low - 1}",
                expected_output="validation error below lower boundary",
                covered_item=f"lower boundary just-below case for {field}",
                priority="High",
                checker_status="repaired",
            ),
        )
    if not _has_on_boundary(combined):
        _append_case(
            repaired,
            TestCase(
                test_id=_next_test_id(repaired.test_cases),
                technique="BVA",
                requirement_target=repaired.requirement_id,
                preconditions="None",
                input_data=f"{field}={low}",
                expected_output="accepted on boundary when all other rules are satisfied",
                covered_item=f"on-boundary case for {field}",
                priority="High",
                checker_status="repaired",
            ),
        )
    if not _has_upper_boundary(combined):
        _append_case(
            repaired,
            TestCase(
                test_id=_next_test_id(repaired.test_cases),
                technique="BVA",
                requirement_target=repaired.requirement_id,
                preconditions="None",
                input_data=f"{field}={high + 1}",
                expected_output="validation error above upper boundary",
                covered_item=f"upper boundary just-above case for {field}",
                priority="High",
                checker_status="repaired",
            ),
        )


def _repair_decision(repaired: ParsedTrace, requirement_text: str, combined: list[str]) -> None:
    _ensure_decision_step(repaired)
    rule_case_count = sum(any(marker in text for marker in ["rule", "decision", "coupon", "otp", "refund", "free shipping"]) for text in combined)
    if rule_case_count >= 2:
        return
    rules = extract_rule_lines(requirement_text)
    for rule in rules[: max(0, 2 - rule_case_count)]:
        _append_case(
            repaired,
            TestCase(
                test_id=_next_test_id(repaired.test_cases),
                technique="Decision Table",
                requirement_target=repaired.requirement_id,
                preconditions="rule conditions satisfied",
                input_data=f"conditions satisfying: {rule}",
                expected_output="rule-specific outcome verified",
                covered_item=f"decision rule: {rule}",
                priority="High",
                checker_status="repaired",
            ),
        )


def _transition_case(repaired: ParsedTrace, transition: StateTransition, *, legal: bool) -> TestCase:
    transition_kind = "legal transition" if legal else "illegal transition"
    expected = "transition succeeds" if legal else "transition rejected"
    preconditions = transition.source_state
    input_data = transition.trigger
    covered_item = f"{transition_kind}: {transition.source_state} -> {transition.target_state}"
    return TestCase(
        test_id=_next_test_id(repaired.test_cases),
        technique="State Transition",
        requirement_target=repaired.requirement_id,
        preconditions=preconditions,
        input_data=input_data,
        expected_output=expected,
        covered_item=covered_item,
        priority="High",
        checker_status="repaired",
    )


def _repair_state(repaired: ParsedTrace, combined: list[str]) -> None:
    _ensure_state_step(repaired)
    has_legal = any("legal" in text or "succeeds" in text or "approved" in text for text in combined)
    has_illegal = any("illegal transition" in text or ("transition" in text and "reject" in text) or "locked" in text for text in combined)
    state_model = repaired.state_model

    if not has_legal:
        if state_model and state_model.legal_transitions:
            _append_case(repaired, _transition_case(repaired, state_model.legal_transitions[0], legal=True))
        else:
            _append_case(
                repaired,
                TestCase(
                    test_id=_next_test_id(repaired.test_cases),
                    technique="State Transition",
                    requirement_target=repaired.requirement_id,
                    preconditions="valid source state",
                    input_data="legal trigger",
                    expected_output="transition succeeds",
                    covered_item="legal transition (repair)",
                    priority="High",
                    checker_status="repaired",
                ),
            )

    if not has_illegal:
        if state_model and state_model.illegal_transitions:
            _append_case(repaired, _transition_case(repaired, state_model.illegal_transitions[0], legal=False))
        else:
            _append_case(
                repaired,
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
                ),
            )


def local_repair(candidate: CandidateEvaluation) -> ParsedTrace:
    repaired = deepcopy(candidate.parsed_trace)
    repaired.test_cases = dedupe_test_cases(repaired.test_cases)
    techniques = list(dict.fromkeys(repaired.selected_techniques() + infer_techniques(candidate.requirement_text)))
    combined = _combined_case_text(repaired)

    _ensure_verification_reference(repaired)

    if "EP" in techniques:
        _repair_ep(repaired, combined)
        combined = _combined_case_text(repaired)

    if "BVA" in techniques:
        _repair_bva(repaired, candidate.requirement_text, combined)
        combined = _combined_case_text(repaired)

    if "Decision Table" in techniques:
        _repair_decision(repaired, candidate.requirement_text, combined)
        combined = _combined_case_text(repaired)

    if "State Transition" in techniques or repaired.category == "workflow_state":
        _repair_state(repaired, combined)

    repaired.test_cases = dedupe_test_cases(repaired.test_cases)
    _renumber_cases(repaired)
    for case in repaired.test_cases:
        if not case.checker_status or case.checker_status == "pending":
            case.checker_status = "repaired"

    repaired.raw_text = repaired.to_markdown()
    return repaired
