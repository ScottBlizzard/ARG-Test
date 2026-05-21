Analysis:
- Requirement target: preorder_deposit_and_balance_payment
- Rule: 1. A preorder defines deposit_percent between 10 and 30.
- Rule: 2. deposit_amount equals order_total * deposit_percent and is due immediately.
- Rule: 3. The remaining balance is due before ship_deadline_date.
- Rule: 4. If deposit is not paid, the preorder is cancelled.
- Rule: 5. If balance is not paid by the deadline, the preorder is cancelled.
- Numeric constraint: a preorder defines deposit_percent between 10 and 30. -> 10 to 30

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
| T01 | EP | preorder_deposit_and_balance_payment | None | representative valid input | request accepted | valid partition | High | pending |
| T02 | EP | preorder_deposit_and_balance_payment | None | representative invalid input | validation error | invalid partition | High | pending |
| T03 | BVA | preorder_deposit_and_balance_payment | None | a preorder defines deposit_percent between 10 and 30.=9 | validation error | below lower boundary | High | pending |
| T04 | BVA | preorder_deposit_and_balance_payment | None | a preorder defines deposit_percent between 10 and 30.=10 | boundary accepted | on lower boundary | High | pending |
| T05 | BVA | preorder_deposit_and_balance_payment | None | a preorder defines deposit_percent between 10 and 30.=30 | boundary accepted | on upper boundary | Medium | pending |
| T06 | Decision Table | preorder_deposit_and_balance_payment | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | pending |
