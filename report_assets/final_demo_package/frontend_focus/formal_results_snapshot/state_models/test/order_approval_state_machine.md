# State Model: order_approval_state_machine

- States: `Draft, Submitted, ManagerApproved, FinanceApproved, Rejected, Closed`
- Start states: `Draft`

## Legal Transitions

| Source | Trigger | Target | Rule |
| --- | --- | --- | --- |
| Draft | Submit | Submitted | Submit is allowed only from Draft and moves the order to Submitted. |
| Submitted | ManagerApprove | ManagerApproved | ManagerApprove is allowed only from Submitted and moves the order to ManagerApproved. |
| Submitted | ManagerReject | Rejected | ManagerReject is allowed only from Submitted and moves the order to Rejected. |
| ManagerApproved | FinanceApprove | FinanceApproved | FinanceApprove is allowed only from ManagerApproved and moves the order to FinanceApproved. |
| ManagerApproved | FinanceReject | Rejected | FinanceReject is allowed only from ManagerApproved and moves the order to Rejected. |
| FinanceApproved | Close | Closed | Close is allowed only from FinanceApproved and moves the order to Closed. |
| Rejected | EditAndResubmit | Draft | EditAndResubmit is allowed only from Rejected and moves the order to Draft. |

## Illegal Transitions

| Source | Trigger | Target | Rule |
| --- | --- | --- | --- |
|  |  |  |  |

## Coverage Plan: All States

- Sequence count: `2`
- Fully covered: `true`

### AS01

- Covered states: `Draft, Submitted, ManagerApproved, FinanceApproved, Closed`
- Covered transitions: `Draft -> Submitted [Submit]; Submitted -> ManagerApproved [ManagerApprove]; ManagerApproved -> FinanceApproved [FinanceApprove]; FinanceApproved -> Closed [Close]`

- Start in Draft
- Trigger `Submit`: Draft -> Submitted
- Trigger `ManagerApprove`: Submitted -> ManagerApproved
- Trigger `FinanceApprove`: ManagerApproved -> FinanceApproved
- Trigger `Close`: FinanceApproved -> Closed

### AS02

- Covered states: `Draft, Submitted, Rejected`
- Covered transitions: `Draft -> Submitted [Submit]; Submitted -> Rejected [ManagerReject]`

- Start in Draft
- Trigger `Submit`: Draft -> Submitted
- Trigger `ManagerReject`: Submitted -> Rejected


## Coverage Plan: All Transitions

- Sequence count: `3`
- Fully covered: `true`

### AT01

- Covered states: `Draft, Submitted, ManagerApproved, FinanceApproved, Closed`
- Covered transitions: `Draft -> Submitted [Submit]; Submitted -> ManagerApproved [ManagerApprove]; ManagerApproved -> FinanceApproved [FinanceApprove]; FinanceApproved -> Closed [Close]`

- Start in Draft
- Trigger `Submit`: Draft -> Submitted
- Trigger `ManagerApprove`: Submitted -> ManagerApproved
- Trigger `FinanceApprove`: ManagerApproved -> FinanceApproved
- Trigger `Close`: FinanceApproved -> Closed

### AT02

- Covered states: `Draft, Submitted, ManagerApproved, Rejected`
- Covered transitions: `Draft -> Submitted [Submit]; Submitted -> ManagerApproved [ManagerApprove]; ManagerApproved -> Rejected [FinanceReject]; Rejected -> Draft [EditAndResubmit]`

- Start in Draft
- Trigger `Submit`: Draft -> Submitted
- Trigger `ManagerApprove`: Submitted -> ManagerApproved
- Trigger `FinanceReject`: ManagerApproved -> Rejected
- Trigger `EditAndResubmit`: Rejected -> Draft

### AT03

- Covered states: `Draft, Submitted, Rejected`
- Covered transitions: `Draft -> Submitted [Submit]; Submitted -> Rejected [ManagerReject]`

- Start in Draft
- Trigger `Submit`: Draft -> Submitted
- Trigger `ManagerReject`: Submitted -> Rejected
