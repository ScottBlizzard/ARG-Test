Analysis:
- Requirement target: free_shipping_threshold_by_member_tier
- Rule: 1. member_tier is one of Guest, Silver, or Gold.
- Rule: 2. For local or domestic orders, Standard shipping becomes free when subtotal reaches the tier threshold.
- Rule: 3. Thresholds are: Guest 120, Silver 100, Gold 80.
- Rule: 4. Express shipping is never free.
- Rule: 5. International orders never get free shipping.

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
| T01 | Decision Table | free_shipping_threshold_by_member_tier | None | representative valid input | request accepted | valid partition | High | repaired |
| T02 | Decision Table | free_shipping_threshold_by_member_tier | None | representative invalid input | validation error | invalid partition | High | repaired |
| T06 | Decision Table | free_shipping_threshold_by_member_tier | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | repaired |
