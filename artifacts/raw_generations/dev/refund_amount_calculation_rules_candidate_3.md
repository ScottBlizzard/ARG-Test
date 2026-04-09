Analysis:
- Requirement target: refund_amount_calculation_rules
- Rule: 1. refund_base equals paid_amount minus non_refundable_fees.
- Rule: 2. If item_opened is true, apply restocking_fee_rate 0.10 capped at 50.
- Rule: 3. refund_amount equals refund_base minus restocking_fee, and must be between 0 and paid_amount.
- Rule: 4. If refund_amount would be negative, it becomes 0.

Pattern:
- Selected techniques: EP, BVA, Decision Table
- Rationale: use partitions for valid/invalid inputs, boundaries for thresholds, and rule/state modeling when behavior depends on combinations or transitions.

Steps:
1. Partition inputs into valid and invalid classes for mandatory fields and business constraints.
2. Derive just-below, on-boundary, and just-above values for detected numeric limits.
3. Convert conditional rules into decision rows and map each rule to at least one test case.

Verification:
- Verified against Step 1 for basic coverage of valid and invalid cases.
- Verified against Step 2 for boundary coverage where numeric limits exist.
- Checked that each test case includes an expected output.

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | EP | refund_amount_calculation_rules | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | EP | refund_amount_calculation_rules | None | representative invalid input | validation error | invalid partition | High | pending |
| T06 | Decision Table | refund_amount_calculation_rules | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |