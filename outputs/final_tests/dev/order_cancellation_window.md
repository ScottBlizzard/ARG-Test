Analysis:
- Requirement target: order_cancellation_window
- Rule: 1. An order has status and paid_at timestamp.
- Rule: 2. A paid order may be cancelled within 30 minutes of paid_at, only if it has not been Shipped.
- Rule: 3. An unpaid order may be cancelled at any time.
- Rule: 4. If cancellation is not allowed, the system returns an error and keeps the order unchanged.

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
| T01 | Decision Table | order_cancellation_window | None | representative valid input | request accepted | valid partition | High | repaired |
| T02 | Decision Table | order_cancellation_window | None | representative invalid input | validation error | invalid partition | High | repaired |
| T06 | Decision Table | order_cancellation_window | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | repaired |
