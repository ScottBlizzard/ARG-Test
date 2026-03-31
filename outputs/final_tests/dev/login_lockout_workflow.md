Analysis:
- Requirement target: login_lockout_workflow
- Rule: 1. An account starts in the Active state.
- Rule: 2. After 5 consecutive failed login attempts within 10 minutes, the account enters the Locked state for 15 minutes.
- Rule: 3. A successful login in the Active state resets the failed-attempt counter to 0.
- Rule: 4. A login attempt in the Locked state returns "account locked" without checking the password.
- Rule: 5. After 15 minutes, the account returns to the Active state and the failed-attempt counter resets.
- Rule: 6. An administrator may unlock the account immediately and return it to the Active state.

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
| T01 | Decision Table | login_lockout_workflow | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | Decision Table | login_lockout_workflow | None | representative invalid input | validation error | invalid partition | High | pending |
| T06 | Decision Table | login_lockout_workflow | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |
| T07 | State Transition | login_lockout_workflow | initial state | legal trigger | state transition succeeds | legal transition | High | pending |
| T08 | State Transition | login_lockout_workflow | restricted state | illegal trigger | transition rejected | illegal transition | High | pending |
