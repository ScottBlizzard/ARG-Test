from pathlib import Path

from src.llm_client import MockLLMClient
from src.parser import parse_trace
from src.pipeline import ARGTestPipeline
from src.risk import assess_requirement_risk, assign_case_priorities
from src.schemas import ParsedTrace, RiskAssessment, TestCase as TraceTestCase
from src.utils import extract_requirement_id, list_requirement_files, read_text


ROOT = Path(__file__).resolve().parents[1]


def test_assess_requirement_risk_flags_high_risk_stateful_payment_rule():
    requirement_text = """Requirement ID: payment_3ds_authentication_flow
1. The payment flow must reject transactions when 3DS authentication fails.
2. The order remains pending until the customer completes authentication.
3. The system must only allow capture after successful authentication.
4. Retry is allowed only once before the payment is locked.
"""
    raw_trace = MockLLMClient("mock").generate_structured_candidates(
        requirement_id="payment_3ds_authentication_flow",
        requirement_text=requirement_text,
        prompt="",
        candidates=1,
    )[0]
    parsed = parse_trace(raw_trace, "payment_3ds_authentication_flow")

    assessment = assess_requirement_risk(requirement_text, parsed, "workflow_state")

    assert assessment.level == "High"
    assert assessment.score >= 5.0
    assert "category=workflow_state" in assessment.drivers
    assert "illegal transitions" in assessment.recommended_focus


def test_assign_case_priorities_escalates_negative_and_stateful_cases():
    parsed = ParsedTrace(
        requirement_id="demo",
        analysis="demo",
        pattern="State Transition + Decision Table",
        steps=["1. demo"],
        verification="demo",
        raw_text="demo",
        risk_assessment=RiskAssessment(
            level="High",
            score=5.5,
            rule_count=4,
            numeric_constraint_count=0,
            technique_count=2,
            drivers=["demo"],
            recommended_focus=["illegal transitions"],
        ),
        test_cases=[
            TraceTestCase(
                test_id="T01",
                technique="State Transition",
                requirement_target="demo",
                preconditions="restricted state",
                input_data="illegal trigger",
                expected_output="transition rejected",
                covered_item="illegal transition",
                priority="Medium",
            ),
            TraceTestCase(
                test_id="T02",
                technique="BVA",
                requirement_target="demo",
                preconditions="None",
                input_data="boundary input",
                expected_output="accepted",
                covered_item="upper boundary",
                priority="Low",
            ),
        ],
    )

    assign_case_priorities(parsed)

    assert parsed.test_cases[0].priority == "Critical"
    assert parsed.test_cases[1].priority == "High"


def test_pipeline_process_requirement_file_exports_risk_summary(tmp_path):
    requirement_path = next(path for path in list_requirement_files(ROOT, "test") if path.stem == "coupon_discount_engine")
    pipeline = ARGTestPipeline(
        base_dir=ROOT,
        provider="mock",
        model="mock-arg-test",
        candidates=3,
        output_root=str(tmp_path),
    )

    summary = pipeline.process_requirement_file(requirement_path, candidates=3, export=True)

    assert summary["category"] is not None
    assert summary["risk_assessment"] is not None
    assert summary["risk_assessment"]["level"] in {"Low", "Medium", "High"}

    requirement_text = read_text(requirement_path)
    requirement_id = extract_requirement_id(requirement_text, requirement_path.stem)
    report_path = tmp_path / "outputs" / "reports" / "test" / f"{requirement_id}_summary.json"
    assert report_path.exists()

    report_payload = report_path.read_text(encoding="utf-8")
    assert '"risk_assessment"' in report_payload
    assert '"run_context"' in report_payload
