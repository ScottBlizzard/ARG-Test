# Coupon Discount Engine Mutation Demonstration

- Curated executable cases: `4`
- Seeded mutants: `4`
- Killed mutants: `4`
- Kill rate: `1.0`

## Executable cases

| Case ID | Description |
| --- | --- |
| BB01 | Multiple coupons must be rejected. |
| BB02 | SAVE10 must be accepted on the subtotal=50 boundary. |
| BB03 | SAVE20 must be rejected when sale items are present. |
| BB04 | FREESHIP must be accepted on the subtotal=30 boundary. |

## Mutant results

| Mutant | Description | Killed | Killed By |
| --- | --- | --- | --- |
| multiple_coupons_allowed | Mutant ignores the one-coupon-only rule and silently uses the first coupon. | yes | BB01, BB03 |
| save10_boundary_bug | Mutant rejects SAVE10 exactly at subtotal 50. | yes | BB02 |
| save20_sale_item_bug | Mutant ignores the SAVE20 sale-item restriction. | yes | BB03 |
| freeship_boundary_bug | Mutant rejects FREESHIP exactly at subtotal 30. | yes | BB04 |
