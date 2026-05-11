from __future__ import annotations

from io import BytesIO

from fastapi.testclient import TestClient

from demo_web.app import app


client = TestClient(app)


def test_demo_web_index() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "ARG-Test Demo Console" in response.text


def test_demo_web_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_demo_web_formal_summary() -> None:
    response = client.get("/api/formal-summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["official_run"]["requirement_count"] >= 1
    assert "baseline_averages" in payload


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
