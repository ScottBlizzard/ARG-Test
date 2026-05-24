# NFR Validation Summary

## Performance

- Sample size: `5`
- Average mock processing time per requirement: `0.014 s`

| Requirement | Seconds |
| --- | ---: |
| address_international_format_validation | 0.0189 |
| bank_transfer_rule_checker | 0.0123 |
| bundle_discount_eligibility_rules | 0.0138 |
| checkout_promo_stack_and_priority | 0.0117 |
| coupon_discount_engine | 0.0135 |

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
- experiment scripts: `18`
- test files: `7`
- test cases: `38`
- pytest exit code: `0`
- pytest summary: `38 passed in 5.72s`
- runtime output isolation supported: `true`
