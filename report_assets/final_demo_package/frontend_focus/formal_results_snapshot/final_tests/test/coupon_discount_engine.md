Analysis:
The system handles coupon redemption with strict logical constraints involving monetary thresholds, user status, item types, and temporal validity. Key variables include Coupon Code, Order Subtotal, Customer Member Status, Presence of Sale Items, and Coupon Date Status. The complexity arises from conflicting conditions (e.g., SAVE20 vs. Sale Items) and exclusive application rules (one coupon per order). Black-box testing must cover valid paths, invalid paths, boundary conditions for pricing, and logical contradictions without accessing internal code.

Pattern:
**Selected Technique:** Decision Table Testing.
**Complementary Techniques:** Boundary Value Analysis (for subtotals) and Equivalence Partitioning (for coupon validity statuses).
**Rationale:** Multiple conditional rules (Rule 2-6) dictate mutually exclusive outcomes based on specific combinations of inputs (subtotal ranges, membership, flags). Decision Tables allow us to map these distinct condition permutations to specific outputs (discount applied, rejection reason) ensuring full coverage of interaction logic. Numeric boundaries (30, 50, 100) will be tested using BVA within the decision table entries.

Steps:
1. Initialize order with Subtotal 40.00, Standard Member, No Sale Items, Apply SAVE10.
2. Initialize order with Subtotal 50.00, Standard Member, No Sale Items, Apply SAVE10.
3. Initialize order with Subtotal 100.00, Premium Member, No Sale Items, Valid Date (April 2026), Apply SAVE20.
4. Initialize order with Subtotal 100.00, Premium Member, Has Sale Items, Valid Date, Apply SAVE20.
5. Initialize order with Subtotal 30.00, Any Member, No Sale Items, Valid Date, Apply FREESHIP.
6. Initialize order with Subtotal 200.00, Premium Member, Valid Date, Apply Expired Coupon (Expired March 2026).
7. Initialize order with Subtotal 100.00, Standard Member, No Sale Items, Apply SAVE10 then SAVE20.

Verification:
- Verified logic in Step 2 aligns with Rule 2 threshold minimum (>=50).
- Verified logic in Step 4 covers the exclusion condition defined in Rule 6 against Step 3 result.
- Verified expiration validation in Step 6 references Rule 5 status checking mechanism.
- Verified single coupon constraint in Step 7 references Rule 1 enforcement during input phase.

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | BVA/EP | Rule 2 | Normal Session | Coupon: SAVE10, Subtotal: 40.00, Member: Std, Items: Normal | Discount: 0.00, Final Total: 40.00 | Rule 2 Threshold (Below) | Critical | Pending |
| T02 | BVA/EP | Rule 2 | Normal Session | Coupon: SAVE10, Subtotal: 50.00, Member: Std, Items: Normal | Discount: 5.00, Final Total: 45.00 | Rule 2 Threshold (At) | Critical | Pending |
| T03 | Decision Table | Rule 3 | Normal Session | Coupon: SAVE20, Subtotal: 100.00, Member: Premium, Valid: Apr 2026 | Discount: 20.00, Final Total: 80.00 | Rule 3 Full Logic | Critical | Pending |
| T04 | Decision Table | Rule 6 | Normal Session | Coupon: SAVE20, Subtotal: 100.00, Member: Premium, Items: Sale | Discount: 0.00, Message: "Cannot apply with sale items" | Rule 6 Conflict | Critical | Pending |
| T05 | Decision Table | Rule 4 | Normal Session | Coupon: FREESHIP, Subtotal: 30.00, Member: Any, Valid: Apr 2026 | Shipping: 0.00, Applicable: True | Rule 4 Eligibility | Critical | Pending |
| T06 | EP | Rule 5 | Normal Session | Coupon: SAVE10, Expiry: Mar 2026, Current: Apr 2026 | Status: Invalid, Reason: "Coupon Expired" | Rule 5 Temporal Validity | Critical | Pending |
| T07 | Decision Table | Rule 1 | Normal Session | Coupon Stack: SAVE10 + SAVE20 | Error: "Only one coupon allowed" | Rule 1 Exclusivity | Critical | Pending |
| T08 | Boundary Analysis | Rule 7 | Negative Prevention | Coupon: SAVE10, Subtotal: 0.01 | Discount: 0.00, Result: Non-Negative Total | Rule 7 Safety Math | Critical | Pending |
