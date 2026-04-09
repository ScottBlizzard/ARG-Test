Analysis:
- Requirement target: checkout_promo_stack_and_priority
- Rule: 1. At most one coupon code may be applied to an order.
- Rule: 2. Supported coupons:
- Rule: 3. Coupons never apply to tax; percent/fixed coupons apply only to merchandise subtotal (excluding shipping and tax).
- Rule: 4. Loyalty points may be redeemed after coupon discount; points redemption is capped by the remaining payable amount (cannot make payable negative).
- Rule: 5. Expired/unknown coupon codes are invalid.
- Rule: 6. If multiple coupons are provided, the checkout must reject the promotion input.

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
| T01 | Decision Table | checkout_promo_stack_and_priority | None | representative valid input | request accepted | valid partition | High | repaired |
| T02 | Decision Table | checkout_promo_stack_and_priority | None | representative invalid input | validation error | invalid partition | High | repaired |
| T06 | Decision Table | checkout_promo_stack_and_priority | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | repaired |
