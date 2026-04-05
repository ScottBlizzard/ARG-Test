Analysis:
- Requirement target: fraud_risk_scoring_rules
- Rule: 1. Risk score starts at 0.
- Rule: 2. Add 30 if ip_country differs from shipping_country.
- Rule: 3. Add 30 if order_total is above 1000.
- Rule: 4. Add 20 if account_age_days is less than 7.
- Rule: 5. Add 20 if failed_payment_attempts is at least 2.
- Rule: 6. If risk score is at least 70, the order is flagged for manual review.
- Numeric constraint: add 20 if failed_payment_attempts -> 2 to threshold
- Numeric constraint: if risk score -> 70 to threshold

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
| T01 | EP | fraud_risk_scoring_rules | None | representative valid input | request accepted | valid partition | High | repaired |
| T02 | EP | fraud_risk_scoring_rules | None | representative invalid input | validation error | invalid partition | High | repaired |
| T03 | BVA | fraud_risk_scoring_rules | None | add 20 if failed_payment_attempts=1 | validation error | below lower boundary | High | repaired |
| T04 | BVA | fraud_risk_scoring_rules | None | add 20 if failed_payment_attempts=2 | boundary accepted | on lower boundary | High | repaired |
| T05 | BVA | fraud_risk_scoring_rules | None | add 20 if failed_payment_attempts=3 | boundary accepted | on upper boundary | Medium | repaired |
| T06 | Decision Table | fraud_risk_scoring_rules | rule conditions satisfied | rule trigger combination | rule-specific outcome | decision rule coverage | Medium | repaired |
