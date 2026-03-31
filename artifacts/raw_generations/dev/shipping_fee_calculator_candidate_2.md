Analysis:
- Requirement target: shipping_fee_calculator
- Rule: 1. destination zone is one of local, domestic, or international.
- Rule: 2. order subtotal and package weight must be non-negative.
- Rule: 3. For standard shipping, local fees are 5 for weight up to 1 kg, 8 for weight above 1 kg and up to 5 kg, and 12 for weight above 5 kg.
- Rule: 4. For standard shipping, domestic fees are 8 for weight up to 1 kg, 12 for weight above 1 kg and up to 5 kg, and 18 for weight above 5 kg.
- Rule: 5. For standard shipping, international fees are 20 for weight up to 1 kg, 35 for weight above 1 kg and up to 5 kg, and 50 for weight above 5 kg.
- Rule: 6. Express shipping adds a surcharge of 10 for local or domestic and 25 for international.
- Numeric constraint: standard shipping -> 100 to threshold

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
| T01 | EP | shipping_fee_calculator | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | EP | shipping_fee_calculator | None | representative invalid input | validation error | invalid partition | High | pending |
| T03 | BVA | shipping_fee_calculator | None | standard shipping=99 | validation error | below lower boundary | High | pending |
| T04 | BVA | shipping_fee_calculator | None | standard shipping=100 | boundary accepted | on lower boundary | High | pending |
| T05 | BVA | shipping_fee_calculator | None | standard shipping=101 | boundary accepted | on upper boundary | Medium | pending |
| T06 | Decision Table | shipping_fee_calculator | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |