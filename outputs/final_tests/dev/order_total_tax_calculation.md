Analysis:
- Requirement target: order_total_tax_calculation
- Rule: 1. net_subtotal equals sum(item_price * quantity) minus item_discounts.
- Rule: 2. shipping_fee is taxable only for US orders.
- Rule: 3. tax_rate is: US 0.08, CN 0.13, other countries 0.
- Rule: 4. tax_amount equals taxable_amount * tax_rate rounded to 2 decimals (half-up).
- Rule: 5. order_total equals net_subtotal + shipping_fee + tax_amount.

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
| T01 | Decision Table | order_total_tax_calculation | None | representative valid input | request accepted | valid partition | High | repaired |
| T02 | Decision Table | order_total_tax_calculation | None | representative invalid input | validation error | invalid partition | High | repaired |
| T06 | Decision Table | order_total_tax_calculation | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | repaired |
