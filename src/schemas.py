from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class TestCase:
    test_id: str
    technique: str
    requirement_target: str
    preconditions: str
    input_data: str
    expected_output: str
    covered_item: str
    priority: str = "Medium"
    checker_status: str = "pending"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["input"] = payload.pop("input_data")
        return payload

    def normalized_signature(self) -> str:
        return " | ".join(
            [
                self.technique.strip().lower(),
                self.requirement_target.strip().lower(),
                self.input_data.strip().lower(),
                self.expected_output.strip().lower(),
            ]
        )


@dataclass
class RiskAssessment:
    level: str
    score: float
    rule_count: int
    numeric_constraint_count: int
    technique_count: int
    drivers: list[str] = field(default_factory=list)
    recommended_focus: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["score"] = round(float(self.score), 3)
        return payload


@dataclass
class ParsedTrace:
    requirement_id: str
    analysis: str
    pattern: str
    steps: list[str]
    verification: str
    test_cases: list[TestCase]
    raw_text: str
    category: str | None = None
    risk_assessment: RiskAssessment | None = None
    missing_sections: list[str] = field(default_factory=list)

    def selected_techniques(self) -> list[str]:
        techniques: list[str] = []
        lowered = self.pattern.lower()
        mapping = {
            "EP": ["ep", "equivalence partition"],
            "BVA": ["bva", "boundary value"],
            "Decision Table": ["decision table"],
            "State Transition": ["state transition"],
        }
        for label, aliases in mapping.items():
            if any(alias in lowered for alias in aliases):
                techniques.append(label)
        return techniques

    def to_dict(self) -> dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "category": self.category,
            "risk_assessment": self.risk_assessment.to_dict() if self.risk_assessment else None,
            "analysis": self.analysis,
            "pattern": self.pattern,
            "steps": self.steps,
            "verification": self.verification,
            "missing_sections": self.missing_sections,
            "test_cases": [case.to_dict() for case in self.test_cases],
        }

    def to_markdown(self) -> str:
        lines = [
            "Analysis:",
            self.analysis.strip(),
            "",
            "Pattern:",
            self.pattern.strip(),
            "",
            "Steps:",
        ]
        if self.steps:
            lines.extend(self.steps)
        else:
            lines.append("1. No steps were captured.")
        lines.extend(["", "Verification:", self.verification.strip(), "", "FinalAnswer:"])
        lines.extend(
            [
                "| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for case in self.test_cases:
            row = [
                case.test_id,
                case.technique,
                case.requirement_target,
                case.preconditions,
                case.input_data,
                case.expected_output,
                case.covered_item,
                case.priority,
                case.checker_status,
            ]
            lines.append("| " + " | ".join(cell.replace("|", "/") for cell in row) + " |")
        return "\n".join(lines).strip() + "\n"


@dataclass
class CheckResult:
    name: str
    passed: bool
    score: float
    diagnostics: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CandidateEvaluation:
    requirement_id: str
    raw_text: str
    parsed_trace: ParsedTrace
    checks: list[CheckResult]
    score: float
    repaired: bool = False
    source: str = "structured"

    def to_dict(self) -> dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "score": self.score,
            "repaired": self.repaired,
            "source": self.source,
            "checks": [check.to_dict() for check in self.checks],
            "parsed_trace": self.parsed_trace.to_dict(),
        }

    def diagnostics(self) -> list[str]:
        details: list[str] = []
        for check in self.checks:
            details.extend([f"{check.name}: {item}" for item in check.diagnostics])
        return details
