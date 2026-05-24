Analysis:
The requirement mandates validation of six fields during checkout. Critical constraints include alphanumeric character restrictions on names (2-40 chars), numeric digit counts for cards (13-19), calendar logic for expiry (1-12 months, 2026-2041 years, non-past dates), and conditional logic for CVV length (3 digits for Visa/MC, 4 for Amex). The system date is April 11, 2026, establishing the baseline for "current" expiration validity. Input validation must reject masked numbers (*).

Pattern:
We apply **Boundary Value Analysis (BVA)** for numeric ranges (name length, card digits, expiry dates) and **Equivalence Partitioning (EP)** to select representative valid and invalid values for character sets. **Decision Table Testing** principles are applied to map Card Brand to CVV length requirements.

Steps:
1. Execute input form with minimum valid parameters for all fields to establish a positive baseline.
2. Execute inputs at lower boundaries (e.g., 1-char name, 12-digit card, month 0) to trigger error messages.
3. Execute inputs at upper boundaries (e.g., 41-char name, 20-digit card, year 2042) to verify rejection.
4. Execute inputs utilizing mismatched CVV lengths relative to specified card brands.
5. Execute inputs with masked card numbers (* characters) and past dates to verify rejection.

Verification:
- Verified against Step 1 to ensure basic functionality works.
- Verified against Step 2 to ensure boundary rejections occur.
- Verified against Step 4 to confirm brand-dependent CVV logic holds.
- Ensures all expected outputs align with requirement failure conditions.

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | EP | Valid Input | None | Name="Alice Smith", Card="4539123456789012", Exp="12/2028", CVV="123", Brand="Visa" | Validation Passed | All Rules (Valid) | Critical | pending |
| T02 | BVA | Name Length | None | Name="A", Card="4539123456789012", Exp="12/2028", CVV="123", Brand="Visa" | Error: Name length must be 2 to 40 | Name Min Boundary | Critical | pending |
| T03 | BVA | Card Digits | None | Name="Alice", Card="123456789012", Exp="12/2028", CVV="123", Brand="Visa" | Error: Card number must contain 13 to 19 digits | Card Min Boundary | Critical | pending |
| T04 | EP | Card Characters | None | Name="Alice", Card="4539***89012", Exp="12/2028", CVV="123", Brand="Visa" | Error: Masked card numbers not accepted | Illegal Input | Critical | pending |
| T05 | BVA | Expiry Date | None | Name="Alice", Card="4539123456789012", Exp="03/2026", CVV="123", Brand="Visa" | Error: Expiry date cannot be in the past | Date Past Check | Critical | pending |
| T06 | BVA | Expiry Year | None | Name="Alice", Card="4539123456789012", Exp="01/2042", CVV="123", Brand="Visa" | Error: Expiry year must be within 2026 to 2041 | Year Max Boundary | Critical | pending |
| T07 | Decision Table | CVV Length | None | Name="Alice", Card="4539123456789012", Exp="12/2028", CVV="1234", Brand="Visa" | Error: CVV length invalid for brand | Brand CVV Mismatch | Critical | pending |
| T08 | Decision Table | CVV Length | None | Name="Alice", Card="378282246310005", Exp="12/2028", CVV="123", Brand="American Express" | Error: CVV length invalid for brand (Amex requires 4) | Brand CVV Mismatch | Critical | pending |
