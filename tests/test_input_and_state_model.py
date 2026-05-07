import csv
from pathlib import Path

from src.input_loader import load_requirements_from_csv
from src.llm_client import MockLLMClient
from src.parser import parse_trace
from src.pipeline import ARGTestPipeline
from src.state_model import build_state_model
from src.utils import read_text


ROOT = Path(__file__).resolve().parents[1]


def test_load_requirements_from_csv_reads_rows_and_defaults_split(tmp_path):
    csv_path = tmp_path / "requirements.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["requirement_id", "requirement_text"])
        writer.writeheader()
        writer.writerow(
            {
                "requirement_id": "csv_case_1",
                "requirement_text": "Requirement ID: csv_case_1\nRules:\n1. A request starts in Draft.\n2. Submit is allowed only from Draft and moves the request to Submitted.\n",
            }
        )

    records = load_requirements_from_csv(csv_path, default_split="adhoc")

    assert len(records) == 1
    assert records[0].requirement_id == "csv_case_1"
    assert records[0].split == "adhoc"


def test_pipeline_process_requirement_text_supports_direct_input_export(tmp_path):
    requirement_text = """Requirement ID: direct_text_coupon
Rules:
1. SAVE10 requires subtotal at least 50.
2. FREESHIP requires subtotal at least 30.
3. Only one coupon can be applied.
"""
    pipeline = ARGTestPipeline(
        base_dir=ROOT,
        provider="mock",
        model="mock-arg-test",
        candidates=3,
        output_root=str(tmp_path),
    )

    summary = pipeline.process_requirement_text(
        requirement_text,
        requirement_id="direct_text_coupon",
        split="adhoc",
        candidates=3,
        export=True,
    )

    assert summary["split"] == "adhoc"
    assert summary["risk_assessment"] is not None
    assert (tmp_path / "outputs" / "reports" / "adhoc" / "direct_text_coupon_summary.json").exists()


def test_build_state_model_for_order_approval_covers_all_states():
    requirement_path = ROOT / "data" / "requirements" / "test" / "order_approval_state_machine.txt"
    requirement_text = read_text(requirement_path)
    raw_trace = MockLLMClient("mock").generate_structured_candidates(
        requirement_id="order_approval_state_machine",
        requirement_text=requirement_text,
        prompt="",
        candidates=1,
    )[0]
    parsed = parse_trace(raw_trace, "order_approval_state_machine")

    state_model = build_state_model(requirement_text, parsed)

    assert state_model is not None
    assert "Draft" in state_model.states
    assert "Closed" in state_model.states
    assert len(state_model.legal_transitions) >= 7
    all_states_plan = next(plan for plan in state_model.coverage_plans if plan.coverage_goal == "All States")
    covered_states = {state for sequence in all_states_plan.sequences for state in sequence.covered_states}
    covered_states.update(state_model.start_states)
    assert set(state_model.states).issubset(covered_states)
    assert all_states_plan.fully_covered is True


def test_pipeline_exports_state_model_for_workflow_requirement(tmp_path):
    requirement_path = ROOT / "data" / "requirements" / "test" / "order_approval_state_machine.txt"
    pipeline = ARGTestPipeline(
        base_dir=ROOT,
        provider="mock",
        model="mock-arg-test",
        candidates=3,
        output_root=str(tmp_path),
    )

    summary = pipeline.process_requirement_file(requirement_path, candidates=3, export=True)

    assert summary["state_model"] is not None
    assert (tmp_path / "outputs" / "state_models" / "test" / "order_approval_state_machine.json").exists()
