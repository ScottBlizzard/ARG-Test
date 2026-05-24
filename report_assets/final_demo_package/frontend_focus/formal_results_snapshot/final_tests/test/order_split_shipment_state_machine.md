Analysis:
The requirement defines a composite state machine where individual shipment lifecycles drive an aggregate Order State. The core risks involve incorrect aggregation logic when handling mixed shipment states, invalid state transitions (regression), and improper constraint enforcement on cancellations. The system must enforce strict forward progress for shipments (pending to delivered) and aggregate these states mathematically.

Pattern:
We utilize **State Transition Testing** to verify individual shipment lifecycle integrity (PENDING to DELIVERED) and negative transition constraints. We supplement this with **Decision Table Testing** to validate the complex combinatorial logic used to derive the Order State based on subsets of shipments (e.g., mixed PENDING and SHIPPED states).

Steps:
1. Initialize an order containing two shipments; verify initial status is ORDER_PENDING.
2. Execute forward state transitions on Shipment A: PENDING -> PACKED -> SHIPPED -> DELIVERED.
3. Construct a decision matrix with Shipment A=SHIPPED and Shipment B=PENDING; verify aggregation.
4. Attempt to cancel Shipment A after it reaches PACKED status.
5. Attempt to revert Shipment A from DELIVERED back to SHIPPED.

Verification:
- Verified against Step 1 (Initialization) and Step 2 (Forward Transitions) to confirm state propagation logic holds.
- Verified against Step 3 (Aggregation) to ensure Decision Table outcomes match expected derivation rules.
- Verified against Step 4 and Step 5 (Constraint Enforcement) to ensure illegal operations are blocked via expected error codes.

FinalAnswer:
| Test ID | Technique | Requirement Target | Preconditions | Input | Expected Output | Covered Item | Priority | Checker Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | STT | Init State | New Order Created | Action: Create Order with 2 items | Order State: ORDER_PENDING | Rule 3a | High | pending |
| T02 | STT | Lifecycle | Order Exists, Shipments=PENDING | Action: Advance Ship A to PACKED | Order State: ORDER_PARTIALLY_FULFILLED | Rule 2, 3b | High | pending |
| T03 | STT | Lifecycle | Ship A=PACKED, Ship B=DELIVERED | Action: Advance Ship A to DELIVERED | Order State: ORDER_DELIVERED | Rule 2, 3d | High | pending |
| T04 | DTT | Aggregation | Ship A=SHIPPED, Ship B=PENDING | Action: Query Order Status | Order State: ORDER_PARTIALLY_FULFILLED | Rule 3b | High | pending |
| T05 | STT | Cancellation | Ship A=PACKED | Action: Cancel Shipment A | Result: Error "Cannot Cancel Non-Pending" | Rule 4 | High | pending |
| T06 | STT | Legal Constraint | Ship A=DELIVERED | Action: Revert Ship A to SHIPPED | Result: Error "Illegal State Transition" | Rule 5 | High | pending |
