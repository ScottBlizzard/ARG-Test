Analysis:
- Requirement target: loyalty_points_earn
- Rule: 1. Earned points are computed from net_subtotal (non-negative).
- Rule: 2. earn_rate is 1 point per 1 currency unit.
- Rule: 3. earned_points equals floor(net_subtotal).
- Rule: 4. If an order is cancelled or fully refunded, earned_points become 0.

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
| T01 | Decision Table | loyalty_points_earn | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | Decision Table | loyalty_points_earn | None | representative invalid input | validation error | invalid partition | High | pending |
| T06 | Decision Table | loyalty_points_earn | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |