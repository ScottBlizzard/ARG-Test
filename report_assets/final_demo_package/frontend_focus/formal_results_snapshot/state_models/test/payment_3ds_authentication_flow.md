# State Model: payment_3ds_authentication_flow

- States: `INITIATED, AUTH_REQUIRED, FAILED, AUTHENTICATED, PENDING_REVIEW`
- Start states: `INITIATED`

## Legal Transitions

| Source | Trigger | Target | Rule |
| --- | --- | --- | --- |
| AUTH_REQUIRED | 3DS fails or the customer cancels | FAILED | If 3DS fails or the customer cancels, the payment becomes FAILED. |

## Illegal Transitions

| Source | Trigger | Target | Rule |
| --- | --- | --- | --- |
| AUTH_REQUIRED | CAPTURE | CAPTURED | Illegal: capture before authentication when 3DS is required. |

## Coverage Plan: All States

- Sequence count: `4`
- Fully covered: `false`

### AS01

- Covered states: ``

- Target state `AUTHENTICATED` is currently unreachable from the declared start states.

### AS02

- Covered states: ``

- Target state `AUTH_REQUIRED` is currently unreachable from the declared start states.

### AS03

- Covered states: ``

- Target state `FAILED` is currently unreachable from the declared start states.

### AS04

- Covered states: ``

- Target state `PENDING_REVIEW` is currently unreachable from the declared start states.


## Coverage Plan: All Transitions

- Sequence count: `1`
- Fully covered: `true`

### AT01

- Covered states: `AUTH_REQUIRED, FAILED`
- Covered transitions: `AUTH_REQUIRED -> FAILED [3DS fails or the customer cancels]`

- Start in AUTH_REQUIRED
- Trigger `3DS fails or the customer cancels`: AUTH_REQUIRED -> FAILED
