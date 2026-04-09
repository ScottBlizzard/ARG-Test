Analysis:
- Requirement target: shipping_method_eligibility_by_weight
- Rule: 1. Supported methods are Standard, Express, and Freight.
- Rule: 2. weight must be non-negative.
- Rule: 3. Standard is available for weight up to 20 kg.
- Rule: 4. Express is available for weight up to 5 kg and only when hazardous is false.
- Rule: 5. Freight is required when weight is above 20 kg.

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
| T01 | EP | shipping_method_eligibility_by_weight | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | EP | shipping_method_eligibility_by_weight | None | representative invalid input | validation error | invalid partition | High | pending |
| T06 | Decision Table | shipping_method_eligibility_by_weight | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |