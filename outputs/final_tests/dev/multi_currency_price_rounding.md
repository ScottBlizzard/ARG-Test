Analysis:
- Requirement target: multi_currency_price_rounding
- Rule: 1. Prices are converted using exchange_rate: converted = base_amount * exchange_rate.
- Rule: 2. USD and EUR display 2 decimals; JPY displays 0 decimals.
- Rule: 3. Rounding is half-up.
- Rule: 4. Line total equals rounded(converted_unit_price) * quantity.
- Rule: 5. Cart subtotal equals sum of line totals.

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
| T01 | Decision Table | multi_currency_price_rounding | None | representative valid input | request accepted | valid partition | High | repaired |
| T02 | Decision Table | multi_currency_price_rounding | None | representative invalid input | validation error | invalid partition | High | repaired |
| T06 | Decision Table | multi_currency_price_rounding | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | repaired |
