# State Model: warehouse_pickup_order_workflow

- States: `READY_FOR_PICKUP, PICKED_UP, EXPIRED, RETURN_IN_TRANSIT, HOLD_FOR_REVIEW`
- Start states: `READY_FOR_PICKUP`

## Legal Transitions

| Source | Trigger | Target | Rule |
| --- | --- | --- | --- |
| READY_FOR_PICKUP | the customer provides the correct pickup code within the pickup window | PICKED_UP | If the customer provides the correct pickup code within the pickup window, the order moves to PICKED_UP. |
| PICKED_UP | the pickup window expires before pickup | EXPIRED | If the pickup window expires before pickup, the order moves to EXPIRED. |
| EXPIRED | staff may | RETURN_IN_TRANSIT | From EXPIRED, staff may transition the order to RETURN_IN_TRANSIT. |
| RETURN_IN_TRANSIT | station staff report parcel damage | HOLD_FOR_REVIEW | If station staff report parcel damage, the order moves to HOLD_FOR_REVIEW. |

## Illegal Transitions

| Source | Trigger | Target | Rule |
| --- | --- | --- | --- |
| Illegal | ILLEGAL | PICKED_UP | Illegal: PICKED_UP back to READY_FOR_PICKUP. |

## Coverage Plan: All States

- Sequence count: `2`
- Fully covered: `true`

### AS01

- Covered states: `READY_FOR_PICKUP, PICKED_UP, EXPIRED`
- Covered transitions: `READY_FOR_PICKUP -> PICKED_UP [the customer provides the correct pickup code within the pickup window]; PICKED_UP -> EXPIRED [the pickup window expires before pickup]`

- Start in READY_FOR_PICKUP
- Trigger `the customer provides the correct pickup code within the pickup window`: READY_FOR_PICKUP -> PICKED_UP
- Trigger `the pickup window expires before pickup`: PICKED_UP -> EXPIRED

### AS02

- Covered states: `READY_FOR_PICKUP, PICKED_UP, EXPIRED, RETURN_IN_TRANSIT, HOLD_FOR_REVIEW`
- Covered transitions: `READY_FOR_PICKUP -> PICKED_UP [the customer provides the correct pickup code within the pickup window]; PICKED_UP -> EXPIRED [the pickup window expires before pickup]; EXPIRED -> RETURN_IN_TRANSIT [staff may]; RETURN_IN_TRANSIT -> HOLD_FOR_REVIEW [station staff report parcel damage]`

- Start in READY_FOR_PICKUP
- Trigger `the customer provides the correct pickup code within the pickup window`: READY_FOR_PICKUP -> PICKED_UP
- Trigger `the pickup window expires before pickup`: PICKED_UP -> EXPIRED
- Trigger `staff may`: EXPIRED -> RETURN_IN_TRANSIT
- Trigger `station staff report parcel damage`: RETURN_IN_TRANSIT -> HOLD_FOR_REVIEW


## Coverage Plan: All Transitions

- Sequence count: `1`
- Fully covered: `true`

### AT01

- Covered states: `READY_FOR_PICKUP, PICKED_UP, EXPIRED, RETURN_IN_TRANSIT, HOLD_FOR_REVIEW`
- Covered transitions: `READY_FOR_PICKUP -> PICKED_UP [the customer provides the correct pickup code within the pickup window]; PICKED_UP -> EXPIRED [the pickup window expires before pickup]; EXPIRED -> RETURN_IN_TRANSIT [staff may]; RETURN_IN_TRANSIT -> HOLD_FOR_REVIEW [station staff report parcel damage]`

- Start in READY_FOR_PICKUP
- Trigger `the customer provides the correct pickup code within the pickup window`: READY_FOR_PICKUP -> PICKED_UP
- Trigger `the pickup window expires before pickup`: PICKED_UP -> EXPIRED
- Trigger `staff may`: EXPIRED -> RETURN_IN_TRANSIT
- Trigger `station staff report parcel damage`: RETURN_IN_TRANSIT -> HOLD_FOR_REVIEW
