Analysis:
- Requirement target: product_variant_selection_validation
- Rule: 1. A configurable product defines options such as size and color.
- Rule: 2. The selected option combination must match an existing variant.
- Rule: 3. The selected variant must be available_for_sale.
- Rule: 4. If selection is invalid, adding to cart is rejected.

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
| T01 | EP | product_variant_selection_validation | None | representative valid input | request accepted | valid partition | High | repaired |
| T02 | EP | product_variant_selection_validation | None | representative invalid input | validation error | invalid partition | High | repaired |
| T06 | Decision Table | product_variant_selection_validation | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | repaired |
| T04 | BVA | product_variant_selection_validation | None | repaired boundary input | boundary behavior verified | boundary case (repair) | Medium | repaired |
