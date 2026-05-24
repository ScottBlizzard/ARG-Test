Analysis:
The requirement defines a checkout promotion system with strict constraints on coupon application, monetary thresholds, and calculation interactions with tax and loyalty points. Key test objectives include validating input integrity (coupon validity), ensuring mathematical accuracy at thresholds (boundary values), enforcing business rules (stacking prohibition), and confirming financial isolation (tax exclusion and payment caps). The primary risks involve incorrect discount application, over-discounting resulting in negative payables, or tax miscalculations.

Pattern:
We employ **Equivalence Partitioning (EP)** to categorize coupon codes into valid and invalid sets, reducing redundant testing on status codes. We utilize **Boundary Value Analysis (BVA)** to test exact monetary thresholds (e.g., 79.00 vs 80.00) where behavior changes. These techniques allow us to efficiently target the core logic without exhaustive enumeration while adhering to black-box principles.

Steps:
1. Execute input validation for unknown or expired coupon codes to confirm rejection.
2. Execute threshold boundary tests (below, at, and above) for subsidy eligibility rules.
3. Execute negative testing scenarios involving multiple coupon inputs to enforce single-use policy.
4. Validate financial calculations to ensure tax components remain untouched during discount application.
5. Validate post-discount financial limits to ensure loyalty points cannot reduce payable balance below zero.

Verification:
- Verified Test Case T01 against Step 1 (Coupon Validation).
- Verified Test Cases T02 and T03 against Step 2 (Threshold Boundaries).
- Verified Test Case T04 against Step 3 (Stacking Restriction).
- Verified Test Case T05 against Step 4 (Tax Isolation) and Step 5 (Payable Cap).

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | Equivalence Partitioning | Invalid Coupon Handling | Subtotal = 150; Valid Cart | Code: "INVALID_CODE99"; Items: $150 | System rejects code; Message: "Code invalid"; Total unchanged | Rule 5 | High | repaired |
| T02 | Boundary Value Analysis | Shipping Subsidy Threshold | Subtotal near 80; SHIPFREE selected | Code: "SHIPFREE"; Subtotal: 79.99 | Discount N/A; Original shipping fee charged | Rule 2 | High | repaired |
| T03 | Boundary Value Analysis | Percentage Discount Activation | Subtotal near 100; PERCENT10 selected | Code: "PERCENT10"; Subtotal: 100.00 | Merchandise price reduced 10%; Correct new total | Rule 2 | High | repaired |
| T04 | Decision Logic (Rule Based) | Multiple Coupon Rejection | Valid cart; Attempting stack | Code 1: "PERCENT10"; Code 2: "FIXED20" | System rejects input; Error: "Only one promo allowed" | Rule 1, 6 | Critical | repaired |
| T05 | Integration Testing | Tax & Points Calculation | Subtotal 200, Tax 20, Points 500 | Code: "FIXED20"; Apply 500pts | Discount on merch only (Tax 20 kept); Points deducted max to current payable; No negative balance | Rule 3, 4 | High | repaired |
| T06 | BVA | checkout_promo_stack_and_priority | None | repaired boundary input | boundary behavior verified | boundary case (repair) | High | repaired |
