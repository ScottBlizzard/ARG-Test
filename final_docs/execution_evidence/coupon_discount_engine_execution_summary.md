# Coupon Discount Engine Execution Summary

## Scope

Detailed module under execution:

- `reference_impl/coupon_discount_engine.py`

Test files:

- `tests/test_coupon_discount_engine_blackbox.py`
- `tests/test_coupon_discount_engine_whitebox.py`

## Commands used

```powershell
python -m pytest tests\test_coupon_discount_engine_blackbox.py tests\test_coupon_discount_engine_whitebox.py -q
python -m pytest tests -q
python -m coverage run --branch -m pytest tests -q
python -m coverage report -m reference_impl\coupon_discount_engine.py
python -m coverage xml -o final_docs\execution_evidence\coupon_discount_engine_coverage.xml
python -m coverage xml -o final_docs\execution_evidence\coupon_discount_engine_branch_coverage.xml
```

## Results

- module-specific tests passed: `15`
- repo-level tests passed: `27`
- module pytest result: `15 passed`
- repo pytest result: `27 passed`
- statement coverage for `reference_impl/coupon_discount_engine.py`: `100%`
- branch coverage for `reference_impl/coupon_discount_engine.py`: `100%`

Coverage summary:

```text
Name                                       Stmts   Miss Branch BrPart  Cover
reference_impl\coupon_discount_engine.py      51      0     26      0   100%
TOTAL                                         51      0     26      0   100%
```

## Interpretation

This evidence gives the final project a concrete detailed-execution anchor:

- black-box cases are represented by threshold, partition, and rule-oriented tests
- white-box evidence is represented by executable branch-oriented tests plus full statement coverage

## Evidence files

- `final_docs/execution_evidence/coupon_discount_engine_coverage.xml`
- `final_docs/execution_evidence/coupon_discount_engine_branch_coverage.xml`
- `final_docs/execution_evidence/coupon_discount_engine_execution_summary.md`
