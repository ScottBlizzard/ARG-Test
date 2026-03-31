from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from .utils import extract_numeric_hints, extract_rule_lines, infer_techniques


class BaseLLMClient(ABC):
    def __init__(self, model: str) -> None:
        self.model = model

    @abstractmethod
    def generate_structured_candidates(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str,
        candidates: int,
    ) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def generate_plain_table(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def repair_trace(
        self,
        requirement_id: str,
        requirement_text: str,
        repair_prompt: str,
    ) -> str:
        raise NotImplementedError


class MockLLMClient(BaseLLMClient):
    def generate_structured_candidates(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str,
        candidates: int,
    ) -> list[str]:
        return [self._build_structured_trace(requirement_id, requirement_text, index) for index in range(candidates)]

    def generate_plain_table(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str,
    ) -> str:
        techniques = infer_techniques(requirement_text)
        primary = techniques[0]
        rows = [
            "| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
            f"| T01 | {primary} | {requirement_id} | None | representative valid input | accept request | representative valid partition | High |",
            f"| T02 | {primary} | {requirement_id} | None | representative invalid input | reject request | representative invalid partition | High |",
        ]
        return "\n".join(rows)

    def repair_trace(
        self,
        requirement_id: str,
        requirement_text: str,
        repair_prompt: str,
    ) -> str:
        return self._build_structured_trace(requirement_id, requirement_text, candidate_index=99)

    def _build_structured_trace(self, requirement_id: str, requirement_text: str, candidate_index: int) -> str:
        techniques = infer_techniques(requirement_text)
        rules = extract_rule_lines(requirement_text)
        numeric_hints = extract_numeric_hints(requirement_text)
        analysis_lines = [f"- Requirement target: {requirement_id}"]
        analysis_lines.extend(f"- Rule: {rule}" for rule in rules[:6])
        if numeric_hints:
            analysis_lines.extend(
                f"- Numeric constraint: {hint['field']} -> {hint.get('low')} to {hint.get('high', 'threshold')}" for hint in numeric_hints[:4]
            )
        pattern_lines = [
            f"- Selected techniques: {', '.join(techniques)}",
            "- Rationale: use partitions for valid/invalid inputs, boundaries for thresholds, and rule/state modeling when behavior depends on combinations or transitions.",
        ]
        steps = []
        step_index = 1
        if "EP" in techniques:
            steps.append(f"{step_index}. Partition inputs into valid and invalid classes for mandatory fields and business constraints.")
            step_index += 1
        if "BVA" in techniques:
            steps.append(f"{step_index}. Derive just-below, on-boundary, and just-above values for detected numeric limits.")
            step_index += 1
        if "Decision Table" in techniques:
            steps.append(f"{step_index}. Convert conditional rules into decision rows and map each rule to at least one test case.")
            step_index += 1
        if "State Transition" in techniques:
            steps.append(f"{step_index}. Enumerate legal and illegal transitions between named states and triggers.")
            step_index += 1
        if not steps:
            steps.append("1. Generate representative valid and invalid black-box tests.")
        verification_lines = [
            "- Verified against Step 1 for basic coverage of valid and invalid cases.",
            "- Verified against Step 2 for boundary coverage where numeric limits exist.",
            "- Checked that each test case includes an expected output.",
        ]
        rows = self._build_mock_rows(requirement_id, techniques, numeric_hints, candidate_index)
        return "\n".join(
            [
                "Analysis:",
                *analysis_lines,
                "",
                "Pattern:",
                *pattern_lines,
                "",
                "Steps:",
                *steps,
                "",
                "Verification:",
                *verification_lines,
                "",
                "FinalAnswer:",
                "| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
                *rows,
            ]
        )

    def _build_mock_rows(
        self,
        requirement_id: str,
        techniques: list[str],
        numeric_hints: list[dict[str, object]],
        candidate_index: int,
    ) -> list[str]:
        primary = techniques[0]
        rows: list[list[str]] = [
            ["T01", primary, requirement_id, "None", "representative valid input", "request accepted", "valid partition", "High", "pending"],
            ["T02", primary, requirement_id, "None", "representative invalid input", "validation error", "invalid partition", "High", "pending"],
        ]
        if any(item == "BVA" for item in techniques) and numeric_hints:
            hint = numeric_hints[0]
            low = int(hint.get("low", 1))
            high = int(hint.get("high", low + 1)) if hint.get("high") is not None else low + 1
            rows.extend(
                [
                    ["T03", "BVA", requirement_id, "None", f"{hint['field']}={low - 1}", "validation error", "below lower boundary", "High", "pending"],
                    ["T04", "BVA", requirement_id, "None", f"{hint['field']}={low}", "boundary accepted", "on lower boundary", "High", "pending"],
                    ["T05", "BVA", requirement_id, "None", f"{hint['field']}={high}", "boundary accepted", "on upper boundary", "Medium", "pending"],
                ]
            )
        if any(item == "Decision Table" for item in techniques):
            rows.append(["T06", "Decision Table", requirement_id, "rule conditions satisfied", "rule trigger combination", "rule-specific outcome", "decision rule coverage", "Medium", "pending"])
        if any(item == "State Transition" for item in techniques):
            rows.append(["T07", "State Transition", requirement_id, "initial state", "legal trigger", "state transition succeeds", "legal transition", "High", "pending"])
            rows.append(["T08", "State Transition", requirement_id, "restricted state", "illegal trigger", "transition rejected", "illegal transition", "High", "pending"])
        if candidate_index == 0 and len(rows) > 4:
            rows = rows[:-1]
        return ["| " + " | ".join(item) + " |" for item in rows]


class OpenAIResponsesClient(BaseLLMClient):
    def __init__(self, model: str, api_key: str | None = None) -> None:
        super().__init__(model)
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("openai package is required for provider=openai") from exc
        self._client = OpenAI(api_key=api_key)

    def generate_structured_candidates(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str,
        candidates: int,
    ) -> list[str]:
        return [self._run(prompt) for _ in range(candidates)]

    def generate_plain_table(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str,
    ) -> str:
        return self._run(prompt)

    def repair_trace(
        self,
        requirement_id: str,
        requirement_text: str,
        repair_prompt: str,
    ) -> str:
        return self._run(repair_prompt)

    def _run(self, prompt: str) -> str:
        response = self._client.responses.create(model=self.model, input=prompt)
        return getattr(response, "output_text", "") or ""


def get_llm_client(provider: str, model: str, api_key: str | None = None) -> BaseLLMClient:
    provider_key = provider.strip().lower()
    if provider_key == "mock":
        return MockLLMClient(model)
    if provider_key == "openai":
        return OpenAIResponsesClient(model=model, api_key=api_key)
    raise ValueError(f"Unsupported provider: {provider}")
