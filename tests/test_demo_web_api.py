from __future__ import annotations

from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient

from demo_web.app import app


client = TestClient(app)
REPO_ROOT = Path(__file__).resolve().parents[1]


def test_demo_web_index() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "ARG-Test Demo Console" in response.text


def test_demo_web_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "frontend_focus" in payload["formal_results_source"]


def test_demo_web_formal_summary() -> None:
    response = client.get("/api/formal-summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["official_run"]["requirement_count"] >= 1
    assert "baseline_averages" in payload
    assert "frontend_focus" in payload["formal_report_source"]


def test_demo_web_requirement_catalog() -> None:
    response = client.get("/api/demo-requirements")
    assert response.status_code == 200
    payload = response.json()
    direct_ids = {item["requirement_id"] for item in payload["direct_requirements"]}
    state_items = payload["state_requirements"]
    assert payload["provider"] == "mock"
    assert len(direct_ids) >= 16
    assert "pickup_station_contact_validation" in direct_ids
    assert "warehouse_pickup_order_workflow" in {item["requirement_id"] for item in state_items}
    assert all(item["split"] == "test" for item in payload["direct_requirements"])
    assert all(item["category"] == "workflow_state" for item in state_items)
    assert all(item["requirement_text"].startswith("Requirement ID:") for item in state_items)


def test_demo_web_replays_frozen_formal_result_for_catalog_requirement() -> None:
    requirement_text = (REPO_ROOT / "data" / "requirements" / "test" / "payment_3ds_authentication_flow.txt").read_text(encoding="utf-8-sig")
    response = client.post(
        "/api/analyze-text",
        json={
            "requirement_id": "payment_3ds_authentication_flow",
            "split": "test",
            "provider": "mock",
            "model": "mock-arg-test",
            "candidates": 3,
            "seed": 202601,
            "requirement_text": requirement_text,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["replay_source"] == "frozen_formal_run"
    assert payload["summary"]["metrics"]["overall_coverage"] == 0.655
    assert payload["summary"]["metrics"]["test_count"] == 5
    assert payload["parsed_trace"]["test_cases"]


def test_demo_web_replays_all_catalog_requirements_consistently() -> None:
    catalog = client.get("/api/demo-requirements").json()
    for item in catalog["direct_requirements"]:
        response = client.post(
            "/api/analyze-text",
            json={
                "requirement_id": item["requirement_id"],
                "split": item["split"],
                "provider": "mock",
                "model": "mock-arg-test",
                "candidates": 3,
                "seed": 202601,
                "requirement_text": item["requirement_text"],
            },
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["replay_source"] == "frozen_formal_run"
        assert payload["summary"]["metrics"]["overall_coverage"] == item["overall_coverage"]
        assert payload["summary"]["score"] == item["checker_score"]


def test_demo_web_all_workflow_catalog_items_have_legal_state_transitions() -> None:
    catalog = client.get("/api/demo-requirements").json()
    for item in catalog["state_requirements"]:
        response = client.post(
            "/api/state-model",
            json={
                "requirement_id": item["requirement_id"],
                "split": item["split"],
                "provider": "mock",
                "model": "mock-arg-test",
                "candidates": 3,
                "seed": 202601,
                "requirement_text": item["requirement_text"],
            },
        )
        assert response.status_code == 200
        state_model = response.json()["state_model_only"]
        assert len(state_model["states"]) >= 2
        assert len(state_model["legal_transitions"]) >= 1


def test_demo_web_state_model_for_payment_workflow_has_transitions() -> None:
    requirement_text = (REPO_ROOT / "data" / "requirements" / "test" / "payment_3ds_authentication_flow.txt").read_text(encoding="utf-8-sig")
    response = client.post(
        "/api/state-model",
        json={
            "requirement_id": "payment_3ds_authentication_flow",
            "split": "test",
            "provider": "mock",
            "model": "mock-arg-test",
            "candidates": 3,
            "seed": 202601,
            "requirement_text": requirement_text,
        },
    )
    assert response.status_code == 200
    state_model = response.json()["state_model_only"]
    assert len(state_model["legal_transitions"]) >= 5
    assert len(state_model["illegal_transitions"]) >= 2
    assert "AUTH_REQUIRED" in state_model["states"]


def test_demo_web_analyze_text_mock() -> None:
    response = client.post(
        "/api/analyze-text",
        json={
            "requirement_id": "demo_web_smoke",
            "split": "adhoc",
            "provider": "mock",
            "model": "mock-arg-test",
            "candidates": 3,
            "seed": 202601,
            "requirement_text": "Requirement ID: demo_web_smoke\nRules:\n1. A request starts in Draft.\n2. Submit is allowed only from Draft and moves the request to Submitted.",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"]["requirement_id"] == "demo_web_smoke"
    assert payload["parsed_trace"]["test_cases"]
    assert payload["summary"]["metrics"]["gold_spec_found"] is False


def test_demo_web_designer_review_guidance_overrides_frozen_replay() -> None:
    requirement_text = (REPO_ROOT / "data" / "requirements" / "test" / "coupon_discount_engine.txt").read_text(encoding="utf-8-sig")
    response = client.post(
        "/api/analyze-text",
        json={
            "requirement_id": "coupon_discount_engine",
            "split": "test",
            "provider": "mock",
            "model": "mock-arg-test",
            "candidates": 3,
            "seed": 202601,
            "requirement_text": requirement_text,
            "forced_techniques": ["Decision Table", "BVA"],
            "coverage_items": ["expired coupon", "premium member threshold"],
            "designer_review_notes": "Emphasize negative financial-rule cases first.",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("replay_source") != "frozen_formal_run"
    review = payload["summary"]["designer_review"]
    assert review["forced_techniques"] == ["Decision Table", "BVA"]
    assert review["coverage_items"] == ["expired coupon", "premium member threshold"]
    assert review["designer_review_notes"] == "Emphasize negative financial-rule cases first."


def test_demo_web_revise_test_suite_exports_manual_revision() -> None:
    response = client.post(
        "/api/revise-test-suite",
        json={
            "requirement_text": "Requirement ID: revise_demo\nRules:\n1. A request starts in Draft.\n2. Submit is allowed only from Draft and moves the request to Submitted.\n3. Cancel is allowed only from Draft and moves the request to Cancelled.",
            "requirement_id": "revise_demo",
            "split": "adhoc",
            "category": "workflow_state",
            "analysis": "Identify the Draft source state and two outgoing actions.",
            "pattern": "State Transition + EP",
            "steps": [
                "Derive valid state transitions from the requirement text.",
                "Preserve one valid path and one invalid attempt in the final suite.",
            ],
            "verification": "Check that valid transitions are explicit and illegal transitions remain rejected.",
            "test_cases": [
                {
                    "technique": "State Transition",
                    "requirement_target": "revise_demo",
                    "preconditions": "Request is in Draft.",
                    "input": "Submit the request.",
                    "expected_output": "State changes to Submitted.",
                    "covered_item": "Draft -> Submitted legal transition",
                    "priority": "High",
                    "checker_status": "covered",
                },
                {
                    "technique": "EP",
                    "requirement_target": "revise_demo",
                    "preconditions": "Request is in Submitted.",
                    "input": "Try to submit again.",
                    "expected_output": "Action is rejected and state remains Submitted.",
                    "covered_item": "Repeated submit is invalid",
                    "priority": "Medium",
                    "checker_status": "revised",
                },
            ],
            "designer_review": {
                "forced_techniques": ["State Transition"],
                "coverage_items": ["illegal repeated submit"],
                "designer_review_notes": "Keep the state path short and explicit.",
            },
            "editor_notes": "Added an explicit invalid repeated-submit case.",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["manual_case_revision"] is True
    assert payload["editor_notes"] == "Added an explicit invalid repeated-submit case."
    assert payload["summary"]["manual_case_revision"] is True
    assert payload["summary"]["demo_mode"] == "manual_case_revision"
    assert payload["summary"]["designer_review"]["manual_case_revision"] is True
    assert len(payload["parsed_trace"]["test_cases"]) == 2
    assert payload["parsed_trace"]["test_cases"][1]["checker_status"] == "revised"
    artifact_root = REPO_ROOT / payload["artifact_paths"]["runtime_root"]
    assert artifact_root.exists()


def test_demo_web_analyze_csv_mock() -> None:
    csv_bytes = BytesIO(
        (
            "requirement_id,split,requirement_text\n"
            "csv_demo_1,adhoc,\"Requirement ID: csv_demo_1\nRules:\n1. A request starts in Draft.\n2. Submit is allowed only from Draft.\"\n"
        ).encode("utf-8")
    )
    response = client.post(
        "/api/analyze-csv",
        files={"file": ("sample.csv", csv_bytes, "text/csv")},
        data={"provider": "mock", "model": "mock-arg-test", "candidates": "3"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["batch_size"] == 1
    assert payload["records"][0]["summary"]["requirement_id"] == "csv_demo_1"


def test_demo_web_sample_csv_replays_frozen_rows() -> None:
    sample_path = REPO_ROOT / "final_docs" / "execution_evidence" / "sample_requirement_batch.csv"
    response = client.post(
        "/api/analyze-csv",
        files={"file": ("sample_requirement_batch.csv", sample_path.read_bytes(), "text/csv")},
        data={"provider": "mock", "model": "mock-arg-test", "candidates": "3"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["batch_size"] == 2
    assert {record["replay_source"] for record in payload["records"]} == {"frozen_formal_run"}
    by_id = {record["summary"]["requirement_id"]: record for record in payload["records"]}
    assert by_id["pickup_station_contact_validation"]["summary"]["metrics"]["overall_coverage"] == 0.713
    assert by_id["warehouse_pickup_order_workflow"]["summary"]["metrics"]["overall_coverage"] == 0.781
