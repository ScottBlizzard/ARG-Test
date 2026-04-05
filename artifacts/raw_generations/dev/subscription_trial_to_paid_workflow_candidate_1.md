Analysis:
- Requirement target: subscription_trial_to_paid_workflow
- Rule: 1. A subscription starts in Trial and trial_days is 14.
- Rule: 2. At trial end, the system attempts to charge the customer.
- Rule: 3. If charge succeeds, status becomes Active.
- Rule: 4. If charge fails, status becomes PastDue and the system retries daily up to 3 times.
- Rule: 5. If all retries fail, status becomes Cancelled.
- Rule: 6. The customer may cancel at any time.

Pattern:
- Selected techniques: EP, BVA, Decision Table, State Transition
- Rationale: use partitions for valid/invalid inputs, boundaries for thresholds, and rule/state modeling when behavior depends on combinations or transitions.

Steps:
1. Partition inputs into valid and invalid classes for mandatory fields and business constraints.
2. Derive just-below, on-boundary, and just-above values for detected numeric limits.
3. Convert conditional rules into decision rows and map each rule to at least one test case.
4. Enumerate legal and illegal transitions between named states and triggers.

Verification:
- Verified against Step 1 for basic coverage of valid and invalid cases.
- Verified against Step 2 for boundary coverage where numeric limits exist.
- Checked that each test case includes an expected output.

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | EP | subscription_trial_to_paid_workflow | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | EP | subscription_trial_to_paid_workflow | None | representative invalid input | validation error | invalid partition | High | pending |
| T06 | Decision Table | subscription_trial_to_paid_workflow | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |
| T07 | State Transition | subscription_trial_to_paid_workflow | initial state | legal trigger | state transition succeeds | legal transition | High | pending |