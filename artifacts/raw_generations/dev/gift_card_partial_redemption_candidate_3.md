Analysis:
- Requirement target: gift_card_partial_redemption
- Rule: 1. A gift card has balance (non-negative).
- Rule: 2. A user may redeem redeem_amount greater than 0.
- Rule: 3. redeem_amount must not exceed gift card balance.
- Rule: 4. redeem_amount must not exceed order_total.
- Rule: 5. On success, new_balance equals balance minus redeem_amount, and the order payable amount reduces by redeem_amount.

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
| T01 | Decision Table | gift_card_partial_redemption | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | Decision Table | gift_card_partial_redemption | None | representative invalid input | validation error | invalid partition | High | pending |
| T06 | Decision Table | gift_card_partial_redemption | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |