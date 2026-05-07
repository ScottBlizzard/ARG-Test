from __future__ import annotations

import sys
import types
from pathlib import Path

from experiments.run_repeatability import build_seed_schedule
from src.llm_client import get_llm_client
from src.pipeline import ARGTestPipeline
from src.repair import local_repair
from src.schemas import CandidateEvaluation, ParsedTrace, StateModel, StateTransition, TestCase as SchemaTestCase


def test_build_seed_schedule_supports_explicit_values() -> None:
    schedule = build_seed_schedule(
        3,
        seed_values=[101, 202, 303],
        seed_base=None,
        seed_step=17,
        fixed_seed=None,
    )
    assert schedule == [101, 202, 303]


def test_pipeline_candidate_controls_are_deterministic() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    pipeline = ARGTestPipeline(
        base_dir=repo_root,
        provider="mock",
        model="mock-arg-test",
        candidates=3,
        seed=4242,
        temperature=0.0,
        top_p=1.0,
        output_root=".local_runs/test_seed_controls",
    )
    first = pipeline.build_candidate_controls("coupon_discount_engine", 3)
    second = pipeline.build_candidate_controls("coupon_discount_engine", 3)

    assert first == second
    assert [item["candidate_index"] for item in first] == [1, 2, 3]
    assert len({item["seed"] for item in first}) == 3
    assert first[0]["profile_label"] == "balanced_coverage"
    assert "Deterministic candidate focus" in pipeline.generation_prompt("Requirement:\n1. Example rule.", first[0])


def test_openai_chat_client_applies_seed_and_sampling(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeMessage:
        content = "Analysis:\n...\n\nPattern:\n...\n\nSteps:\n1. ...\n\nVerification:\n- ...\n\nFinalAnswer:\n| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| T01 | EP | demo | None | x | y | z | High | pending |"

    class FakeChoice:
        message = FakeMessage()
        finish_reason = "stop"

    class FakeResponse:
        id = "resp_123"
        system_fingerprint = "fp_456"
        choices = [FakeChoice()]

    class FakeChatCompletions:
        def create(self, **kwargs):
            captured.update(kwargs)
            return FakeResponse()

    class FakeChat:
        def __init__(self) -> None:
            self.completions = FakeChatCompletions()

    class FakeOpenAI:
        def __init__(self, **kwargs) -> None:
            captured["client_kwargs"] = kwargs
            self.chat = FakeChat()

    fake_module = types.SimpleNamespace(OpenAI=FakeOpenAI)
    monkeypatch.setitem(sys.modules, "openai", fake_module)

    client = get_llm_client(
        provider="openai",
        model="gpt-test",
        api_key="test-key",
        api_mode="chat_completions",
        seed=111,
        temperature=0.0,
        top_p=1.0,
    )
    outputs = client.generate_structured_candidates(
        requirement_id="demo_requirement",
        requirement_text="Requirement text",
        prompt="prompt body",
        candidates=1,
        candidate_controls=[{"candidate_index": 1, "seed": 987, "profile_label": "balanced_coverage"}],
    )
    metadata = client.get_last_generation_metadata()

    assert outputs[0].startswith("Analysis:")
    assert captured["seed"] == 987
    assert captured["temperature"] == 0.0
    assert captured["top_p"] == 1.0
    assert captured["messages"] == [{"role": "user", "content": "prompt body"}]
    assert metadata[0]["seed_applied"] is True
    assert metadata[0]["system_fingerprint"] == "fp_456"


def test_local_repair_adds_canonical_boundary_rule_and_state_cases() -> None:
    parsed = ParsedTrace(
        requirement_id="demo_requirement",
        analysis="- Rule: amount must be between 1 and 5\n- Rule: If approval succeeds, continue",
        pattern="- Selected techniques: EP, BVA, Decision Table, State Transition",
        steps=["1. Partition valid and invalid inputs."],
        verification="- Verified against Step 1.",
        test_cases=[
                SchemaTestCase(
                test_id="T01",
                technique="EP",
                requirement_target="demo_requirement",
                preconditions="None",
                input_data="amount=2",
                expected_output="request accepted",
                covered_item="valid partition",
            )
        ],
        raw_text="",
        category="workflow_state",
        state_model=StateModel(
            states=["Draft", "Approved", "Rejected"],
            start_states=["Draft"],
            legal_transitions=[StateTransition(source_state="Draft", trigger="Approve", target_state="Approved", legal=True)],
            illegal_transitions=[StateTransition(source_state="Approved", trigger="Edit", target_state="Draft", legal=False)],
        ),
    )
    candidate = CandidateEvaluation(
        requirement_id="demo_requirement",
        requirement_text="1. amount must be between 1 and 5.\n2. If approved, continue.\n3. Edit from Approved is illegal.",
        raw_text="",
        parsed_trace=parsed,
        checks=[],
        score=0.4,
    )

    repaired = local_repair(candidate)
    combined = " ".join(f"{case.covered_item} {case.input_data} {case.expected_output}".lower() for case in repaired.test_cases)

    assert "lower boundary just-below case" in combined
    assert "on-boundary case" in combined
    assert "upper boundary just-above case" in combined
    assert "decision rule:" in combined
    assert "legal transition:" in combined
    assert "illegal transition:" in combined
