Analysis:
- Requirement target: cash_on_delivery_eligibility
- Rule: 1. Cash on delivery (COD) is available only for domestic shipping.
- Rule: 2. COD is available only when order_total is at most 500.
- Rule: 3. COD is not available for digital-only orders.
- Rule: 4. COD is not available for hazardous goods.

Pattern:
- Selected techniques: Decision Table
- Rationale: use partitions for valid/invalid inputs, boundaries for thresholds, and rule/state modeling when behavior depends on combinations or transitions.

Steps:
1. Convert conditional rules into decision rows and map each rule to at least one test case.

Verification:
- Verified against Step 1 for basic coverage of valid and invalid cases.
- Verified against Step 2 for boundary coverage where numeric limits exist.
- Checked that each test case includes an expected output.

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | Decision Table | cash_on_delivery_eligibility | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | Decision Table | cash_on_delivery_eligibility | None | representative invalid input | validation error | invalid partition | High | pending |
| T06 | Decision Table | cash_on_delivery_eligibility | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |