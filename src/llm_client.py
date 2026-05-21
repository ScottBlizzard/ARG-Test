from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .utils import extract_numeric_hints, extract_rule_lines, infer_techniques


def _prompt_for_index(prompt: str | list[str], index: int) -> str:
    if isinstance(prompt, list):
        if not prompt:
            return ""
        if index < len(prompt):
            return prompt[index]
        return prompt[-1]
    return prompt


class BaseLLMClient(ABC):
    def __init__(
        self,
        model: str,
        *,
        api_mode: str,
        seed: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
    ) -> None:
        self.model = model
        self.api_mode = api_mode
        self.seed = seed
        self.temperature = temperature
        self.top_p = top_p
        self._last_generation_metadata: list[dict[str, Any]] = []
        self._last_plain_metadata: dict[str, Any] = {}
        self._last_repair_metadata: dict[str, Any] = {}

    def get_last_generation_metadata(self) -> list[dict[str, Any]]:
        return [dict(item) for item in self._last_generation_metadata]

    def get_last_plain_metadata(self) -> dict[str, Any]:
        return dict(self._last_plain_metadata)

    def get_last_repair_metadata(self) -> dict[str, Any]:
        return dict(self._last_repair_metadata)

    @abstractmethod
    def generate_structured_candidates(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str | list[str],
        candidates: int,
        candidate_controls: list[dict[str, Any]] | None = None,
    ) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def generate_plain_table(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str,
        control: dict[str, Any] | None = None,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def repair_trace(
        self,
        requirement_id: str,
        requirement_text: str,
        repair_prompt: str,
        control: dict[str, Any] | None = None,
    ) -> str:
        raise NotImplementedError

    def _metadata_payload(
        self,
        *,
        operation: str,
        control: dict[str, Any] | None,
        response_id: str | None = None,
        system_fingerprint: str | None = None,
        finish_reason: str | None = None,
        seed_applied: bool = False,
    ) -> dict[str, Any]:
        payload = {
            "operation": operation,
            "api_mode": self.api_mode,
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "seed": (control or {}).get("seed"),
            "seed_applied": seed_applied,
            "candidate_index": (control or {}).get("candidate_index"),
            "profile_label": (control or {}).get("profile_label"),
            "profile_instruction": (control or {}).get("profile_instruction"),
            "response_id": response_id,
            "system_fingerprint": system_fingerprint,
            "finish_reason": finish_reason,
        }
        return payload


class MockLLMClient(BaseLLMClient):
    def __init__(
        self,
        model: str,
        *,
        seed: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
    ) -> None:
        super().__init__(model, api_mode="mock", seed=seed, temperature=temperature, top_p=top_p)

    def generate_structured_candidates(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str | list[str],
        candidates: int,
        candidate_controls: list[dict[str, Any]] | None = None,
    ) -> list[str]:
        controls = candidate_controls or [{"candidate_index": index + 1, "seed": None} for index in range(candidates)]
        outputs: list[str] = []
        metadata: list[dict[str, Any]] = []
        for index in range(candidates):
            control = controls[index] if index < len(controls) else {"candidate_index": index + 1, "seed": None}
            outputs.append(self._build_structured_trace(requirement_id, requirement_text, candidate_index=index, control=control))
            metadata.append(
                self._metadata_payload(
                    operation="structured_generation",
                    control=control,
                    response_id=f"mock-structured-{requirement_id}-{index + 1}",
                    seed_applied=control.get("seed") is not None,
                )
            )
        self._last_generation_metadata = metadata
        return outputs

    def generate_plain_table(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str,
        control: dict[str, Any] | None = None,
    ) -> str:
        techniques = infer_techniques(requirement_text)
        primary = techniques[0]
        rows = [
            "| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
            f"| T01 | {primary} | {requirement_id} | None | representative valid input | accept request | representative valid partition | High |",
            f"| T02 | {primary} | {requirement_id} | None | representative invalid input | reject request | representative invalid partition | High |",
        ]
        self._last_plain_metadata = self._metadata_payload(
            operation="plain_table_generation",
            control=control,
            response_id=f"mock-plain-{requirement_id}",
            seed_applied=(control or {}).get("seed") is not None,
        )
        return "\n".join(rows)

    def repair_trace(
        self,
        requirement_id: str,
        requirement_text: str,
        repair_prompt: str,
        control: dict[str, Any] | None = None,
    ) -> str:
        self._last_repair_metadata = self._metadata_payload(
            operation="repair_trace",
            control=control,
            response_id=f"mock-repair-{requirement_id}",
            seed_applied=(control or {}).get("seed") is not None,
        )
        return self._build_structured_trace(requirement_id, requirement_text, candidate_index=99, control=control)

    def _build_structured_trace(
        self,
        requirement_id: str,
        requirement_text: str,
        candidate_index: int,
        control: dict[str, Any] | None = None,
    ) -> str:
        techniques = infer_techniques(requirement_text)
        rules = extract_rule_lines(requirement_text)
        numeric_hints = extract_numeric_hints(requirement_text)
        analysis_lines = [f"- Requirement target: {requirement_id}"]
        analysis_lines.extend(f"- Rule: {rule}" for rule in rules[:6])
        if control and control.get("profile_label"):
            analysis_lines.append(f"- Candidate focus: {control['profile_label']}")
        if numeric_hints:
            analysis_lines.extend(
                f"- Numeric constraint: {hint['field']} -> {hint.get('low')} to {hint.get('high', 'threshold')}" for hint in numeric_hints[:4]
            )
        pattern_lines = [
            f"- Selected techniques: {', '.join(techniques)}",
            "- Rationale: use partitions for valid/invalid inputs, boundaries for thresholds, and rule/state modeling when behavior depends on combinations or transitions.",
        ]
        if control and control.get("profile_instruction"):
            pattern_lines.append(f"- Deterministic profile: {control['profile_instruction']}")
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
    def __init__(
        self,
        model: str,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        seed: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
    ) -> None:
        super().__init__(model, api_mode="responses", seed=seed, temperature=temperature, top_p=top_p)
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("openai package is required for provider=openai") from exc
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        if timeout is not None:
            client_kwargs["timeout"] = timeout
        self._client = OpenAI(**client_kwargs)

    def generate_structured_candidates(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str | list[str],
        candidates: int,
        candidate_controls: list[dict[str, Any]] | None = None,
    ) -> list[str]:
        controls = candidate_controls or [{"candidate_index": index + 1, "seed": None} for index in range(candidates)]
        outputs: list[str] = []
        metadata: list[dict[str, Any]] = []
        for index in range(candidates):
            control = controls[index] if index < len(controls) else {"candidate_index": index + 1, "seed": None}
            text, meta = self._run(_prompt_for_index(prompt, index), operation="structured_generation", control=control)
            outputs.append(text)
            metadata.append(meta)
        self._last_generation_metadata = metadata
        return outputs

    def generate_plain_table(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str,
        control: dict[str, Any] | None = None,
    ) -> str:
        text, meta = self._run(prompt, operation="plain_table_generation", control=control)
        self._last_plain_metadata = meta
        return text

    def repair_trace(
        self,
        requirement_id: str,
        requirement_text: str,
        repair_prompt: str,
        control: dict[str, Any] | None = None,
    ) -> str:
        text, meta = self._run(repair_prompt, operation="repair_trace", control=control)
        self._last_repair_metadata = meta
        return text

    def _run(self, prompt: str, *, operation: str, control: dict[str, Any] | None) -> tuple[str, dict[str, Any]]:
        request_kwargs: dict[str, Any] = {"model": self.model, "input": prompt}
        if self.temperature is not None:
            request_kwargs["temperature"] = self.temperature
        if self.top_p is not None:
            request_kwargs["top_p"] = self.top_p
        response = self._client.responses.create(**request_kwargs)
        metadata = self._metadata_payload(
            operation=operation,
            control=control,
            response_id=getattr(response, "id", None),
            system_fingerprint=getattr(response, "system_fingerprint", None),
            seed_applied=False,
        )
        return getattr(response, "output_text", "") or "", metadata


class OpenAIChatCompletionsClient(BaseLLMClient):
    def __init__(
        self,
        model: str,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        seed: int | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
    ) -> None:
        super().__init__(model, api_mode="chat_completions", seed=seed, temperature=temperature, top_p=top_p)
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("openai package is required for provider=openai") from exc
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        if timeout is not None:
            client_kwargs["timeout"] = timeout
        self._client = OpenAI(**client_kwargs)

    def generate_structured_candidates(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str | list[str],
        candidates: int,
        candidate_controls: list[dict[str, Any]] | None = None,
    ) -> list[str]:
        controls = candidate_controls or [{"candidate_index": index + 1, "seed": self.seed} for index in range(candidates)]
        outputs: list[str] = []
        metadata: list[dict[str, Any]] = []
        for index in range(candidates):
            control = controls[index] if index < len(controls) else {"candidate_index": index + 1, "seed": self.seed}
            text, meta = self._run(_prompt_for_index(prompt, index), operation="structured_generation", control=control)
            outputs.append(text)
            metadata.append(meta)
        self._last_generation_metadata = metadata
        return outputs

    def generate_plain_table(
        self,
        requirement_id: str,
        requirement_text: str,
        prompt: str,
        control: dict[str, Any] | None = None,
    ) -> str:
        text, meta = self._run(prompt, operation="plain_table_generation", control=control)
        self._last_plain_metadata = meta
        return text

    def repair_trace(
        self,
        requirement_id: str,
        requirement_text: str,
        repair_prompt: str,
        control: dict[str, Any] | None = None,
    ) -> str:
        text, meta = self._run(repair_prompt, operation="repair_trace", control=control)
        self._last_repair_metadata = meta
        return text

    def _run(self, prompt: str, *, operation: str, control: dict[str, Any] | None) -> tuple[str, dict[str, Any]]:
        request_kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        if self.temperature is not None:
            request_kwargs["temperature"] = self.temperature
        if self.top_p is not None:
            request_kwargs["top_p"] = self.top_p
        seed = (control or {}).get("seed")
        if seed is not None:
            request_kwargs["seed"] = seed
        response = self._client.chat.completions.create(**request_kwargs)
        choice = response.choices[0] if getattr(response, "choices", None) else None
        content = ""
        if choice and getattr(choice, "message", None):
            content = getattr(choice.message, "content", "") or ""
        metadata = self._metadata_payload(
            operation=operation,
            control=control,
            response_id=getattr(response, "id", None),
            system_fingerprint=getattr(response, "system_fingerprint", None),
            finish_reason=getattr(choice, "finish_reason", None) if choice else None,
            seed_applied=seed is not None,
        )
        return content, metadata


def get_llm_client(
    provider: str,
    model: str,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: float | None = None,
    *,
    api_mode: str = "chat_completions",
    seed: int | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
) -> BaseLLMClient:
    provider_key = provider.strip().lower()
    if provider_key == "mock":
        return MockLLMClient(model, seed=seed, temperature=temperature, top_p=top_p)
    if provider_key == "openai":
        api_mode_key = api_mode.strip().lower()
        if api_mode_key == "responses":
            return OpenAIResponsesClient(
                model=model,
                api_key=api_key,
                base_url=base_url,
                timeout=timeout,
                seed=seed,
                temperature=temperature,
                top_p=top_p,
            )
        if api_mode_key == "chat_completions":
            return OpenAIChatCompletionsClient(
                model=model,
                api_key=api_key,
                base_url=base_url,
                timeout=timeout,
                seed=seed,
                temperature=temperature,
                top_p=top_p,
            )
        raise ValueError(f"Unsupported OpenAI API mode: {api_mode}")
    raise ValueError(f"Unsupported provider: {provider}")
