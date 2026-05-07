# NFR Validation Summary

## Performance

- Sample size: `5`
- Average mock processing time per requirement: `0.005 s`

| Requirement | Seconds |
| --- | ---: |
| address_international_format_validation | 0.0071 |
| bank_transfer_rule_checker | 0.004 |
| bundle_discount_eligibility_rules | 0.0042 |
| checkout_promo_stack_and_priority | 0.0056 |
| coupon_discount_engine | 0.0042 |

## Usability

- Supported CLI commands: `batch, batch-csv, run, run-text, state-model`
- README quick start available: `true`
- Formal run workflow documented: `true`
- Direct text input supported: `true`
- CSV input supported: `true`
- Export formats: `JSON, CSV, Markdown`

## Security

- Secret leak found in generated/report artifacts: `false`
- Manifests record provider metadata without API key disclosure: `true`

## Maintainability

- `src/` Python modules: `27`
- experiment scripts: `14`
- test files: `5`
- test cases: `23`
- pytest exit code: `0`
- pytest summary: `23 passed in 0.19s`
- runtime output isolation supported: `true`
