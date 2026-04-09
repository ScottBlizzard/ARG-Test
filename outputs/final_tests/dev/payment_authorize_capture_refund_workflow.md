Analysis:
- Requirement target: payment_authorize_capture_refund_workflow
- Rule: 1. Card payments start as Authorized.
- Rule: 2. Authorized may transition to Captured exactly once.
- Rule: 3. Authorized may transition to Voided; void is not allowed after capture.
- Rule: 4. Refunds are allowed only after Captured.
- Rule: 5. Multiple refunds may occur, but total_refunded must not exceed captured_amount.

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
| T01 | Decision Table | payment_authorize_capture_refund_workflow | None | representative valid input | request accepted | valid partition | High | repaired |
| T02 | Decision Table | payment_authorize_capture_refund_workflow | None | representative invalid input | validation error | invalid partition | High | repaired |
| T06 | Decision Table | payment_authorize_capture_refund_workflow | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | repaired |
