Analysis:
- Requirement target: backorder_policy_and_eta
- Rule: 1. If available_stock is 0 and backorder_allowed is true, the item may be purchased as backorder.
- Rule: 2. Backorder requires estimated_ship_days between 1 and 60.
- Rule: 3. If backorder_allowed is false and stock is 0, checkout is rejected.
- Rule: 4. Negative stock is invalid.
- Numeric constraint: backorder requires estimated_ship_days between 1 and 60. -> 1 to 60

Pattern:
- Selected techniques: EP, BVA, Decision Table
- Rationale: use partitions for valid/invalid inputs, boundaries for thresholds, and rule/state modeling when behavior depends on combinations or transitions.

Steps:
1. Partition inputs into valid and invalid classes for mandatory fields and business constraints.
2. Derive just-below, on-boundary, and just-above values for detected numeric limits.
3. Convert conditional rules into decision rows and map each rule to at least one test case.

Verification:
- Verified against Step 1 for basic coverage of valid and invalid cases.
- Verified against Step 2 for boundary coverage where numeric limits exist.
- Checked that each test case includes an expected output.

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | EP | backorder_policy_and_eta | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | EP | backorder_policy_and_eta | None | representative invalid input | validation error | invalid partition | High | pending |
| T03 | BVA | backorder_policy_and_eta | None | backorder requires estimated_ship_days between 1 and 60.=0 | validation error | below lower boundary | High | pending |
| T04 | BVA | backorder_policy_and_eta | None | backorder requires estimated_ship_days between 1 and 60.=1 | boundary accepted | on lower boundary | High | pending |
| T05 | BVA | backorder_policy_and_eta | None | backorder requires estimated_ship_days between 1 and 60.=60 | boundary accepted | on upper boundary | Medium | pending |
| T06 | Decision Table | backorder_policy_and_eta | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |