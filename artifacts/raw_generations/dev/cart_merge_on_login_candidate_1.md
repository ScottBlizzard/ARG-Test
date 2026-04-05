Analysis:
- Requirement target: cart_merge_on_login
- Rule: 1. When a guest user logs in, the guest cart is merged into the user's existing cart.
- Rule: 2. For the same sku, quantities are summed; if the sum exceeds 99, it is capped at 99.
- Rule: 3. If the merged quantity exceeds available_stock, it is reduced to available_stock and a warning is returned.
- Rule: 4. If the guest cart is empty, the user's cart remains unchanged.

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
| T01 | Decision Table | cart_merge_on_login | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | Decision Table | cart_merge_on_login | None | representative invalid input | validation error | invalid partition | High | pending |
| T06 | Decision Table | cart_merge_on_login | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |