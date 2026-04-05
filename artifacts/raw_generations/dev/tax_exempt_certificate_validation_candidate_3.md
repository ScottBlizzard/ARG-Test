Analysis:
- Requirement target: tax_exempt_certificate_validation
- Rule: 1. Tax exemption is supported only for US orders.
- Rule: 2. certificate_id must match pattern EX-XXXXXXXX where X is a digit.
- Rule: 3. certificate_expiry_date must be on or after order_date.
- Rule: 4. If a valid certificate is present for a US order, tax_rate becomes 0.
- Rule: 5. Otherwise tax is calculated normally.

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
| T01 | EP | tax_exempt_certificate_validation | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | EP | tax_exempt_certificate_validation | None | representative invalid input | validation error | invalid partition | High | pending |
| T06 | Decision Table | tax_exempt_certificate_validation | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |