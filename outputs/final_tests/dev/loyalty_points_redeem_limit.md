Analysis:
- Requirement target: loyalty_points_redeem_limit
- Rule: 1. A user may redeem points in multiples of 100.
- Rule: 2. 100 points equals 1 currency unit.
- Rule: 3. redeem_points must not exceed user_points_balance.
- Rule: 4. redemption value must not exceed 20% of order_total.
- Rule: 5. If validation fails, redemption is rejected.

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
| T01 | Decision Table | loyalty_points_redeem_limit | None | representative valid input | request accepted | valid partition | High | repaired |
| T02 | Decision Table | loyalty_points_redeem_limit | None | representative invalid input | validation error | invalid partition | High | repaired |
| T06 | Decision Table | loyalty_points_redeem_limit | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | repaired |
