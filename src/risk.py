from __future__ import annotations

from .schemas import ParsedTrace, RiskAssessment, TestCase
from .utils import extract_numeric_hints, extract_rule_lines

HIGH_IMPACT_KEYWORDS = {
    "payment",
    "refund",
    "coupon",
    "discount",
    "price",
    "billing",
    "invoice",
    "card",
    "cvv",
    "authentication",
    "shipping",
    "wallet",
    "balance",
}
STRICTNESS_KEYWORDS = {
    "must not",
    "cannot",
    "only one",
    "exactly one",
    "unless",
    "except",
    "required",
    "reject",
    "rejected",
    "error",
    "invalid",
    "at least",
    "up to",
}
WORKFLOW_KEYWORDS = {
    "state",
    "transition",
    "status",
    "pending",
    "approved",
    "rejected",
    "expired",
    "locked",
    "unlock",
    "retry",
    "before",
    "after",
}
PRIORITY_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def _hits(text: str, keywords: set[str]) -> list[str]:
    lowered = text.lower()
    return sorted(keyword for keyword in keywords if keyword in lowered)


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        unique.append(item)
    return unique


def assess_requirement_risk(
    requirement_text: str,
    parsed: ParsedTrace,
    category: str | None,
) -> RiskAssessment:
    rules = extract_rule_lines(requirement_text)
    numeric_hints = extract_numeric_hints(requirement_text)
    techniques = parsed.selected_techniques()
    lowered = requirement_text.lower()

    score = 1.0
    drivers: list[str] = []
    focus: list[str] = ["core happy path"]

    category_bonus = {
        "workflow_state": 1.3,
        "business_rules": 1.1,
        "input_validation": 0.8,
    }
    if category in category_bonus:
        score += category_bonus[category]
        drivers.append(f"category={category}")

    if rules:
        rule_bonus = min(len(rules) * 0.35, 2.0)
        score += rule_bonus
        drivers.append(f"{len(rules)} explicit rule lines")
        if len(rules) >= 4:
            focus.append("rule combination coverage")

    if numeric_hints:
        numeric_bonus = min(0.75 + (len(numeric_hints) - 1) * 0.25, 1.5)
        score += numeric_bonus
        drivers.append(f"{len(numeric_hints)} numeric constraints")
        focus.append("boundary coverage")

    if "Decision Table" in techniques:
        score += 0.8
        drivers.append("decision-table logic")
        focus.append("decision combinations")
    if "State Transition" in techniques:
        score += 1.25
        drivers.append("stateful workflow behavior")
        focus.extend(["legal transitions", "illegal transitions"])
    if "BVA" in techniques:
        score += 0.45
    if "EP" in techniques:
        focus.append("invalid partitions")

    impact_hits = _hits(lowered, HIGH_IMPACT_KEYWORDS)
    if impact_hits:
        score += min(0.75 + (len(impact_hits) - 1) * 0.1, 1.15)
        drivers.append(f"business impact keywords: {', '.join(impact_hits[:4])}")
        focus.append("business-critical rules")

    strict_hits = _hits(lowered, STRICTNESS_KEYWORDS)
    if strict_hits:
        score += min(0.55 + (len(strict_hits) - 1) * 0.1, 1.0)
        drivers.append(f"strict rejection/constraint language: {', '.join(strict_hits[:4])}")
        focus.append("negative/error handling")

    workflow_hits = _hits(lowered, WORKFLOW_KEYWORDS)
    if workflow_hits and "State Transition" not in techniques:
        score += 0.45
        drivers.append(f"workflow cues: {', '.join(workflow_hits[:4])}")
        focus.append("state-dependent behavior")

    score = round(score, 3)
    if score >= 7.0:
        level = "High"
    elif score >= 4.5:
        level = "Medium"
    else:
        level = "Low"

    return RiskAssessment(
        level=level,
        score=score,
        rule_count=len(rules),
        numeric_constraint_count=len(numeric_hints),
        technique_count=len(techniques),
        drivers=_dedupe(drivers) or ["generic black-box requirement"],
        recommended_focus=_dedupe(focus),
    )


def _priority_rank(priority: str) -> int:
    return PRIORITY_ORDER.get(priority.strip().lower(), PRIORITY_ORDER["medium"])


def _coerce_priority(priority: str) -> str:
    key = priority.strip().lower()
    if key not in PRIORITY_ORDER:
        key = "medium"
    return key.title()


def _case_priority(case: TestCase, risk_level: str) -> str:
    evidence = " ".join(
        [
            case.technique,
            case.covered_item,
            case.expected_output,
            case.input_data,
            case.preconditions,
        ]
    ).lower()
    technique = case.technique.lower()
    risk = risk_level.strip().lower()

    is_negative = any(token in evidence for token in ["invalid", "error", "reject", "illegal", "forbidden"])
    is_boundary = "boundary" in evidence or technique == "bva"
    is_stateful = "state transition" in technique or "transition" in evidence or "state" in evidence
    is_decision = "decision table" in technique or "decision" in evidence or "rule" in evidence

    if risk == "high":
        if is_negative or is_stateful or is_decision:
            return "Critical"
        if is_boundary:
            return "High"
        return "Medium"
    if risk == "medium":
        if is_negative or is_stateful or is_decision or is_boundary:
            return "High"
        return "Medium"
    if is_negative or is_boundary:
        return "Medium"
    return "Low"


def assign_case_priorities(parsed: ParsedTrace) -> None:
    risk_level = parsed.risk_assessment.level if parsed.risk_assessment else "Medium"
    for case in parsed.test_cases:
        suggested = _case_priority(case, risk_level)
        current = _coerce_priority(case.priority)
        case.priority = suggested if _priority_rank(suggested) >= _priority_rank(current) else current
