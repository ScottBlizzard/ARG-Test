Analysis:
The requirement defines validation logic for a gift order form involving conditional data entry based on `delivery_channel` (EMAIL/SMS). 
Key Inputs: `recipient_name`, `delivery_channel`, `recipient_email`, `recipient_phone`, `scheduled_send_days_ahead`, `gift_message`.
Constraints: 
1. Mandatory Name.
2. Channel-specific contacts (Email requires valid email string [5-100 chars], SMS requires E.164 phone [+8-15 digits]).
3. Date range [0-365] for scheduling if provided.
4. Max 200 chars for message.
Logic depends heavily on the combination of Channel and available contact fields (Decision logic).

Pattern:
We utilize Decision Table Testing (DTT) to handle the logical dependency between `delivery_channel` and contact fields. Boundary Value Analysis (BVA) is applied to strict numeric limits (0-365 days, 5-100 email chars, 200 message chars). Equivalence Partitioning (EP) distinguishes between valid formats and invalid formats (e.g., malformed emails).

Steps:
1. Execute DTT Valid Scenario for EMAIL channel ensuring email length is within bounds.
2. Execute DTT Valid Scenario for SMS channel ensuring phone is E.164 compliant.
3. Apply BVA Min Boundary to `scheduled_send_days_ahead` (Input: 0).
4. Apply BVA Max Boundary to `scheduled_send_days_ahead` (Input: 365).
5. Apply EP Invalid Scenario: Provide EMAIL channel without `recipient_email`.
6. Apply BVA to `gift_message` exceeding max length (Input: 201 chars).

Verification:
- Verified against Step 1 to ensure EMAIL submission succeeds with 100-character email.
- Verified against Step 2 to confirm SMS requires phone presence regardless of email value.
- Verified against Step 4 and Step 5 to validate rejection of out-of-range dates and missing mandatory contact details.

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | DTT | Req 2, 3 | Logged In User | Channel:EMAIL, Email:test@ex.co, Name:Alice | Order Submitted | EMAIL Path Valid | High | repaired |
| T02 | DTT | Req 2, 4 | Logged In User | Channel:SMS, Phone:+12125551234, Name:Alice | Order Submitted | SMS Path Valid | High | repaired |
| T03 | BVA | Req 5 | Logged In User | Days:0, Name:Bob | Scheduled Future (Today) | Day Boundary Min (0) | High | repaired |
| T04 | BVA | Req 5 | Logged In User | Days:365, Name:Charlie | Scheduled Future (1 Year) | Day Boundary Max (365) | High | repaired |
| T05 | EP | Req 7 | Logged In User | Channel:EMAIL, No Email Provided, Name:Dave | Error: Missing Email | Missing Contact Valid | Critical | repaired |
| T06 | BVA | Req 6 | Logged In User | Msg:201 Chars, Name:Eve | Error: Message Too Long | Message Boundary Fail | High | repaired |
