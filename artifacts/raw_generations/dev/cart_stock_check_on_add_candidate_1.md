Analysis:
- Requirement target: cart_stock_check_on_add
- Rule: 1. When adding to cart, the system checks current available_stock for the sku.
- Rule: 2. If available_stock is 0, adding is rejected as out-of-stock.
- Rule: 3. If requested quantity is less than or equal to available_stock, adding succeeds.
- Rule: 4. If requested quantity is greater than available_stock, adding is rejected.

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
| T01 | Decision Table | cart_stock_check_on_add | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | Decision Table | cart_stock_check_on_add | None | representative invalid input | validation error | invalid partition | High | pending |
| T06 | Decision Table | cart_stock_check_on_add | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |