from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reference_impl.coupon_discount_engine import apply_coupon
from reference_impl.coupon_discount_engine_mutants import COUPON_MUTANTS
from src.utils import write_json


CURATED_CASES = [
    {
        "case_id": "BB01",
        "description": "Multiple coupons must be rejected.",
        "kwargs": {"subtotal": 100, "shipping_fee": 10, "coupons": ["SAVE10", "FREESHIP"]},
        "expected": {"status": "rejected", "reason": "multiple coupons are not allowed"},
    },
    {
        "case_id": "BB02",
        "description": "SAVE10 must be accepted on the subtotal=50 boundary.",
        "kwargs": {"subtotal": 50, "shipping_fee": 8, "coupons": ["SAVE10"]},
        "expected": {"status": "accepted", "subtotal": 45.0, "discount_amount": 5.0},
    },
    {
        "case_id": "BB03",
        "description": "SAVE20 must be rejected when sale items are present.",
        "kwargs": {
            "subtotal": 120,
            "shipping_fee": 10,
            "coupons": ["SAVE20"],
            "is_premium": True,
            "has_sale_items": True,
        },
        "expected": {"status": "rejected", "reason": "SAVE20 cannot be used with sale items"},
    },
    {
        "case_id": "BB04",
        "description": "FREESHIP must be accepted on the subtotal=30 boundary.",
        "kwargs": {"subtotal": 30, "shipping_fee": 6, "coupons": ["FREESHIP"]},
        "expected": {"status": "accepted", "shipping_fee": 0.0},
    },
]


def assert_case(fn, case: dict) -> None:
    result = fn(**case["kwargs"])
    for key, expected_value in case["expected"].items():
        actual_value = getattr(result, key)
        if actual_value != expected_value:
            raise AssertionError(
                f"{case['case_id']} expected {key}={expected_value!r}, got {actual_value!r}"
            )


def build_mutation_demo_payload() -> dict:
    reference_failures = []
    for case in CURATED_CASES:
        try:
            assert_case(apply_coupon, case)
        except AssertionError as exc:
            reference_failures.append({"case_id": case["case_id"], "error": str(exc)})

    mutants = []
    for mutant_id, payload in COUPON_MUTANTS.items():
        killed_by = []
        for case in CURATED_CASES:
            try:
                assert_case(payload["callable"], case)
            except AssertionError:
                killed_by.append(case["case_id"])
        mutants.append(
            {
                "mutant_id": mutant_id,
                "description": payload["description"],
                "killed": bool(killed_by),
                "killed_by": killed_by,
                "killed_case_count": len(killed_by),
            }
        )

    killed_mutants = sum(1 for item in mutants if item["killed"])
    return {
        "reference_case_count": len(CURATED_CASES),
        "reference_failures": reference_failures,
        "mutant_count": len(mutants),
        "killed_mutant_count": killed_mutants,
        "kill_rate": round(killed_mutants / len(mutants), 3) if mutants else 0.0,
        "cases": CURATED_CASES,
        "mutants": mutants,
    }


def build_markdown(payload: dict) -> str:
    lines = [
        "# Coupon Discount Engine Mutation Demonstration",
        "",
        f"- Curated executable cases: `{payload['reference_case_count']}`",
        f"- Seeded mutants: `{payload['mutant_count']}`",
        f"- Killed mutants: `{payload['killed_mutant_count']}`",
        f"- Kill rate: `{payload['kill_rate']}`",
        "",
        "## Executable cases",
        "",
        "| Case ID | Description |",
        "| --- | --- |",
    ]
    for case in payload["cases"]:
        lines.append(f"| {case['case_id']} | {case['description']} |")

    lines.extend(
        [
            "",
            "## Mutant results",
            "",
            "| Mutant | Description | Killed | Killed By |",
            "| --- | --- | --- | --- |",
        ]
    )
    for mutant in payload["mutants"]:
        lines.append(
            f"| {mutant['mutant_id']} | {mutant['description']} | {'yes' if mutant['killed'] else 'no'} | {', '.join(mutant['killed_by']) or '-'} |"
        )
    if payload["reference_failures"]:
        lines.extend(["", "## Reference Failures", ""])
        for item in payload["reference_failures"]:
            lines.append(f"- {item['case_id']}: {item['error']}")
    return "\n".join(lines) + "\n"


def main() -> None:
    payload = build_mutation_demo_payload()
    evidence_dir = ROOT / "final_docs" / "execution_evidence"
    write_json(evidence_dir / "coupon_discount_engine_mutation_demo.json", payload)
    (evidence_dir / "coupon_discount_engine_mutation_demo.md").write_text(
        build_markdown(payload),
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
