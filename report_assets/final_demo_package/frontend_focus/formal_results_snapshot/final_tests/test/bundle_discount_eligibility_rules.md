Analysis:
The requirement defines conditional promotion logic based on cart composition (item types, counts, prices) and external factors (coupon usage). Key input variables include Item Type (Laptop, Mouse, Console, Game), Quantity, Unit Price, and Coupon Code. Key output variables include Applied Discount Amount and Error Status. Rules dictate eligibility criteria (Rule 1, 2), price thresholds (Rule 6), quantity constraints (Rule 2), conflict resolution (Rule 5), and stackability restrictions (Rule 8). Black-box testing will validate these conditions without inspecting internal code logic.

Pattern:
Primary Technique: **Decision Table Testing** to map logical combinations of item types and eligibility (Rules 1, 2, 4, 5, 8). 
Secondary Technique: **Boundary Value Analysis** to test edge cases on numeric thresholds (Rule 6: Laptop Price >= 4000, Rule 2: Exactly 2 Games). 
Rationale: Logic complexity requires exhaustive condition coverage, while numeric limits require boundary precision.

Steps:
1. Execute Decision Table test to verify Bundle A eligibility with Laptop prices at the boundary of 4000 (High/Low).
2. Execute Decision Table test to verify Bundle B eligibility requiring exactly 2 games and console inclusion.
3. Execute Negative Boundary/Conflict tests to verify priority selection (highest discount) and invalid coupon stacking (BUNDLE-EXTRA).

Verification:
- Verified against Step 1 and Rule 6 logic (Threshold 4000).
- Verified against Step 3 and Rule 8 logic (Coupon exclusion).

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | Boundary Value Analysis | Rule 1, Rule 6 | Cart contains 1 Laptop, 1 Mouse | Laptop Price: 4000, Mouse: Eligible | Discount: 120 | Rule 6 (Price Threshold) | Critical | pending |
| T02 | Boundary Value Analysis | Rule 1, Rule 6 | Cart contains 1 Laptop, 1 Mouse | Laptop Price: 3999, Mouse: Eligible | Discount: 80 | Rule 6 (Price Threshold) | Critical | pending |
| T03 | Decision Table Testing | Rule 2, Rule 7 | Cart contains 1 Console, 2 Games | Console: Eligible, Games: 2 | Discount: 150 | Rule 2 (Quantity Exact) | Critical | pending |
| T04 | Decision Table Testing | Rule 4, Rule 5 | Cart qualifies for A (120) & B (150) | Laptop>=4k, Mouse=1, Console=1, Game=2 | Discount: 150 (Bundle B) | Rule 5 (Max Discount) | Critical | pending |
| T05 | Decision Table Testing | Rule 3, Rule 8 | Cart qualifies for Bundle A | Laptop, Mouse, Item Tag: Sale | Discount: None / Error | Rule 3 (Sale Items) | Critical | pending |
| T06 | Decision Table Testing | Rule 8 | Cart qualifies for Bundle A | Laptop, Mouse, Coupon: BUNDLE-EXTRA | Discount: None / Error | Rule 8 (No Stack) | Critical | pending |
