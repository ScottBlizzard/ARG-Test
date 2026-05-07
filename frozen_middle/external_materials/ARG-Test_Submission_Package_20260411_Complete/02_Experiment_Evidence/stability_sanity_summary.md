# Stability Sanity Check

- Split: `test`
- Selected requirements: `bundle_discount_eligibility_rules, return_refund_method_eligibility, pickup_station_contact_validation, payment_card_expiry_and_cvv_validation, payment_3ds_authentication_flow`
- Stable cases (|Δscore|<=0.05 and |Δcoverage|<=0.10): `2/5`
- Formal avg score: `0.94` -> Rerun avg score: `0.89`
- Formal avg coverage: `0.63` -> Rerun avg coverage: `0.561`
- Avg absolute score delta: `0.05`
- Avg absolute coverage delta: `0.129`

| Requirement | Category | Formal Score | Rerun Score | Delta | Formal Coverage | Rerun Coverage | Delta | Stable |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| bundle_discount_eligibility_rules | business_rules | 0.950 | 0.850 | -0.100 | 0.627 | 0.427 | -0.200 | no |
| return_refund_method_eligibility | business_rules | 0.950 | 0.950 | +0.000 | 0.568 | 0.449 | -0.119 | no |
| pickup_station_contact_validation | input_validation | 0.950 | 0.850 | -0.100 | 0.713 | 0.537 | -0.176 | no |
| payment_card_expiry_and_cvv_validation | input_validation | 0.850 | 0.850 | +0.000 | 0.587 | 0.664 | +0.077 | yes |
| payment_3ds_authentication_flow | workflow_state | 1.000 | 0.950 | -0.050 | 0.655 | 0.726 | +0.071 | yes |
