Analysis:
The requirement involves logical combinations of payment methods (Gift Card, Coupon) and validation rules (counts, dates, balances). Key variables are Coupon Count (0, 1, ≥2), Coupon Status (Valid, Expired), Gift Card Status (Valid, Invalid), and Financial Boundaries (Final Payable ≥ 0, Order of Operations). We identify four equivalence partitions for coupon validity, three for gift card status, and two for payment balance results. Decision Table Testing is required to manage the mutually exclusive rules (e.g., multiple coupons vs single coupon) and ordered operations (Discount → Gift Card).

Pattern:
Primary Technique: Decision Table Testing. This addresses the combinatorial logic of Rule 1 (Max 1 Coupon) and Rule 2 & 3 (Calculation Order).
Secondary Technique: Equivalence Partitioning. Used to classify input codes into Valid/Invalid/Expired categories and amounts into Sufficient/Insufficient partitions.
Strategy: Combine decision rules to derive specific test vectors that maximize branch coverage on the payment logic path.

Steps:
1. Design Scenario 1 (Happy Path): Single valid coupon + valid gift card + partial balance coverage.
2. Design Scenario 2 (Rule Violation): Multiple coupons submitted to enforce rejection logic.
3. Design Scenario 3 (Boundary): Gift card balance exceeds calculated subtotal after discount (ensure payable is 0, not negative).
4. Design Scenario 4 (Invalid Input): Expired coupon code provided to verify date validation logic.
5. Design Scenario 5 (Invalid Input): Non-existent gift card code provided to verify code lookup logic.

Verification:
- Verified against Step 1 to ensure Rules 2 and 3 calculate discount before gift card deduction correctly.
- Verified against Step 2 to confirm Rule 1 rejects combinations exceeding one coupon.
- Verified against Step 3 to validate Rule 5 ensuring the final payable never dips below zero currency units.
- Confirmed Step 4 and Step 5 inputs trigger appropriate error messages per Rule 6 without processing the transaction.

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | Decision Table | Rules 2, 3 | Cart = $100 ($80 sub, $10 ship, $10 tax); Coupon 10% off; GC=$50 | 1 Coupon (Valid), 1 GC (Valid) | Apply 10% to $80 sub ($72 rem). Add Ship/Tax ($92). Deduct GC ($42). Final: $42. | Math Order, Mix Allowed | Critical | pending |
| T02 | Decision Table | Rule 1 | Cart = $100; Coupon Set A (Valid); Coupon Set B (Valid); GC=$50 | 2 Coupons (Valid), 1 GC (Valid) | Error: "Cannot combine more than one coupon". Transaction Rejected. | Max Coupon Limit | Critical | pending |
| T03 | Boundary Value | Rule 5 | Cart = $50 (Sub $40, Ship $5, Tax $5); Coupon $45 value; GC=$100 | 1 Coupon (Valid), 1 GC (Valid) | Coupon reduces to $0. Total Due $0. GC Balance Unused ($55). Final Payable: $0.00 | Non-negative Balance | Critical | pending |
| T04 | Equivalence Part | Rule 6, 4 | Cart = $100; Coupon Set Expired (Exp Date < Apr 10 2026); GC=$50 | 1 Coupon (Expired), 1 GC (Valid) | Error: "Coupon has expired". Transaction Rejected. Coupon Logic Skipped. | Expiry Validation | Critical | pending |
| T05 | Equivalence Part | Rule 6 | Cart = $100; Coupon (Valid); Gift Card (Invalid Code) | 1 Coupon (Valid), 1 GC (Invalid) | Error: "Invalid gift card code". Transaction Rejected. No Discount Applied. | Code Validation | Critical | pending |
