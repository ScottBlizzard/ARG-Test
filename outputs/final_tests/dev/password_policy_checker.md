Analysis:
- Requirement target: password_policy_checker
- Rule: 1. password is required and must be 8 to 20 characters.
- Rule: 2. password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character from ! @ # $ %.
- Rule: 3. password must not contain whitespace.
- Rule: 4. password must not contain the username as a substring.
- Rule: 5. If the password is invalid, the system returns a validation error and stores nothing.
- Rule: 6. If the password is valid, the system accepts it and stores the hashed password.
- Numeric constraint: password -> 8 to 20

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
| T01 | EP | password_policy_checker | None | representative valid input | request accepted | valid partition | High | repaired |
| T02 | EP | password_policy_checker | None | representative invalid input | validation error | invalid partition | High | repaired |
| T03 | BVA | password_policy_checker | None | password=7 | validation error | below lower boundary | High | repaired |
| T04 | BVA | password_policy_checker | None | password=8 | boundary accepted | on lower boundary | High | repaired |
| T05 | BVA | password_policy_checker | None | password=20 | boundary accepted | on upper boundary | Medium | repaired |
| T06 | Decision Table | password_policy_checker | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | repaired |
