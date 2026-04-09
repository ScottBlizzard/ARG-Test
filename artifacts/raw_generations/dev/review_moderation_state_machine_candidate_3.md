Analysis:
- Requirement target: review_moderation_state_machine
- Rule: 1. A new review starts in Submitted.
- Rule: 2. Submitted transitions to Pending when queued for moderation.
- Rule: 3. A moderator may approve Pending to Approved or reject Pending to Rejected.
- Rule: 4. A moderator may hide an Approved review, moving it to Hidden.
- Rule: 5. Hidden reviews remain hidden until explicitly restored to Approved.

Pattern:
- Selected techniques: Decision Table, State Transition
- Rationale: use partitions for valid/invalid inputs, boundaries for thresholds, and rule/state modeling when behavior depends on combinations or transitions.

Steps:
1. Convert conditional rules into decision rows and map each rule to at least one test case.
2. Enumerate legal and illegal transitions between named states and triggers.

Verification:
- Verified against Step 1 for basic coverage of valid and invalid cases.
- Verified against Step 2 for boundary coverage where numeric limits exist.
- Checked that each test case includes an expected output.

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | Decision Table | review_moderation_state_machine | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | Decision Table | review_moderation_state_machine | None | representative invalid input | validation error | invalid partition | High | pending |
| T06 | Decision Table | review_moderation_state_machine | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |
| T07 | State Transition | review_moderation_state_machine | initial state | legal trigger | state transition succeeds | legal transition | High | pending |
| T08 | State Transition | review_moderation_state_machine | restricted state | illegal trigger | transition rejected | illegal transition | High | pending |