Analysis:
The requirement defines a validation schema for shipping addresses with strict formatting rules. Key logical dependencies exist between `country_code` and `postal_code` necessity/format. Quantitative constraints apply to `address_line1` (1-80), `phone` (+8 to 15 digits), and `postal_code` length. Fields like `full_name` and `city` are mandatory across all countries. `address_line2` is optional. Validation failures return errors; successes allow submission.

Pattern:
Primary technique: **Decision Table Testing** (to handle country-specific postal code logic). Secondary technique: **Boundary Value Analysis** (for length constraints and digit counts). Tertiary technique: **Equivalence Partitioning** (valid vs. invalid formats). These cover conditional logic and limit verification without internal system knowledge.

Steps:
1.  Execute input with Valid US Country Code and compliant ZIP codes (Standard and Extended).
2.  Execute input with Valid UK Country Code and compliant Postcode format.
3.  Execute input with Valid CN Country Code and compliant 6-digit Postal Code.
4.  Execute input with Invalid US Postal Code format while keeping other fields valid.
5.  Execute input with Missing Postal Code for US Country Code.
6.  Execute input with Boundary Address Line 1 length (Minimum 1 char, Maximum 81 chars).
7.  Execute input with Invalid Phone number (Outside +8 to 15 digit range).

Verification:
- Verified against Step 1 and Step 2 confirms successful acceptance for valid country-specific formats.
- Verified against Step 3 ensures Asian region specificity.
- Verified against Step 4 and Step 5 confirms Decision Table logic regarding conditional postal requirements.
- Verified against Step 6 and Step 7 confirms Boundary Value Analysis on length and digit constraints.

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | Boundary Value Analysis | US Postal Format | All required fields present | country_code: US, postal_code: 12345-6789 | Pass Validation | Rule 3 (US Format) | Critical | repaired |
| T02 | Decision Table Testing | UK Postal Format | All required fields present | country_code: UK, postal_code: SW1A 1AA | Pass Validation | Rule 3 (UK Format) | Critical | repaired |
| T03 | Decision Table Testing | CN Postal Format | All required fields present | country_code: CN, postal_code: 100000 | Pass Validation | Rule 2 & 3 (CN Req) | Critical | repaired |
| T04 | Equivalence Partitioning | US Postal Invalid | All required fields present | country_code: US, postal_code: A12345 | Fail Validation | Rule 3 (US Format Error) | Critical | repaired |
| T05 | Decision Table Testing | Missing Postal Code | All required fields present | country_code: US, postal_code: "" | Fail Validation | Rule 2 (Req for US) | Critical | repaired |
| T06 | Boundary Value Analysis | Address Line Length | All required fields present | address_line1: 80 chars | Pass Validation | Rule 5 (Max Length) | Critical | repaired |
| T07 | Boundary Value Analysis | Phone Digit Count | All required fields present | phone: +12345678901234 (15 digits) | Pass Validation | Rule 4 (Max Digits) | Critical | repaired |
| T08 | Boundary Value Analysis | Phone Digit Count | All required fields present | phone: +1234567 (7 digits) | Fail Validation | Rule 4 (Min Digits) | Critical | repaired |
| T09 | BVA | address_international_format_validation | None | repaired boundary input | boundary behavior verified | boundary case (repair) | High | repaired |
