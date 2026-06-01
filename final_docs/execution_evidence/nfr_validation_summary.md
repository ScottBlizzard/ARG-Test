# NFR Validation Summary

## Performance

- Sample size: `100`
- Unique requirement files used before cycling: `66`
- Total mock/local processing time: `0.3646 s`
- Average mock processing time per requirement: `0.0036 s`
- Maximum single-requirement mock processing time: `0.0056 s`
- Passes NFR 4.1.1 local-path threshold (100 requirements within 5 seconds): `true`
- Passes NFR 4.1.2 local-path threshold (single requirement within 2 seconds): `true`

| Requirement preview | Seconds |
| --- | ---: |
| age_restricted_product_purchase_validation | 0.0056 |
| backorder_policy_and_eta | 0.0041 |
| cart_item_quantity_limit | 0.0037 |
| cart_merge_on_login | 0.0033 |
| cart_stock_check_on_add | 0.0033 |
| cash_on_delivery_eligibility | 0.0034 |
| checkout_address_postcode_format | 0.0036 |
| checkout_address_required_fields | 0.0037 |
| coupon_code_format_validation | 0.0034 |
| coupon_expiry_and_timezone | 0.0032 |
| ... 90 additional requirements omitted from preview ... | |

## Usability

- Supported CLI commands: `batch, batch-csv, run, run-text, state-model`
- README quick start available: `true`
- Formal run workflow documented: `true`
- Direct text input supported: `true`
- CSV input supported: `true`
- Web demo available: `true`
- Web demo formal replay snapshot available: `true`
- Web demo tabs: `Direct Input, CSV Batch, State Model, Formal Evidence`
- Export formats: `JSON, CSV, Markdown`

## Security

- Secret leak found in generated/report artifacts: `false`
- Manifests record provider metadata without API key disclosure: `true`

## Maintainability

- `src/` Python modules: `27`
- experiment scripts: `19`
- test files: `8`
- test cases: `45`
- pytest exit code: `0`
- pytest summary: `45 passed, 1 warning in 1.41s`
- runtime output isolation supported: `true`
