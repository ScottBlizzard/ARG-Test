Analysis:
- Requirement target: return_refund_method_eligibility
- Rule: 1. A return is eligible only if requested within 30 days of delivery and the item is not marked final-sale.
- Rule: 2. Refund method depends on original payment method:
- Rule: 3. Shipping fee is refundable only when the return reason is SELLER_FAULT.
- Rule: 4. Refund amount must never exceed the amount paid for the returned items.

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
| T01 | Decision Table | return_refund_method_eligibility | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | Decision Table | return_refund_method_eligibility | None | representative invalid input | validation error | invalid partition | High | pending |
| T06 | Decision Table | return_refund_method_eligibility | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |