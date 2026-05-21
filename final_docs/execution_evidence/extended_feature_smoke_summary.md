# Extended Feature Smoke Summary

## Scope

This note records the smoke verification for the newly closed high-bar feature gaps:

- direct text input
- CSV batch input
- explicit state-model generation

## Commands used

```powershell
@'
Requirement ID: direct_text_state_demo
Rules:
1. A request starts in Draft.
2. Submit is allowed only from Draft and moves the request to Submitted.
3. Approve is allowed only from Submitted and moves the request to Approved.
'@ | python -m src.main run-text --requirement-id direct_text_state_demo --split adhoc --provider mock --model mock-arg-test --candidates 3 --output-root .local_runs/input_mode_smokes

python -m src.main batch-csv --input final_docs\execution_evidence\sample_requirement_batch.csv --provider mock --model mock-arg-test --candidates 3 --output-root .local_runs/input_mode_smokes

python -m src.main state-model --input data\requirements\test\order_approval_state_machine.txt --provider mock --model mock-arg-test --candidates 3 --output-root .local_runs/state_model_smoke
```

## Outputs

### Direct text input

- `.local_runs/input_mode_smokes/outputs/reports/adhoc/direct_text_state_demo_summary.json`

Observed result:

- direct text requirement successfully processed without an input file
- `risk_assessment` and `state_model` were both generated

### CSV batch input

- [sample_requirement_batch.csv](/D:/软件测试/Final/ARG-Test/final_docs/execution_evidence/sample_requirement_batch.csv:1)
- `.local_runs/input_mode_smokes/outputs/reports/adhoc/csv_coupon_rule_summary.json`
- `.local_runs/input_mode_smokes/outputs/reports/adhoc/csv_order_workflow_summary.json`

Observed result:

- CSV row ingestion succeeded
- batch processing produced independent per-requirement summaries
- workflow row also produced a `state_model`

### State-model command

- `.local_runs/state_model_smoke/outputs/state_models/test/order_approval_state_machine.json`
- `.local_runs/state_model_smoke/outputs/state_models/test/order_approval_state_machine.md`

Observed result:

- extracted states: `Draft, Submitted, ManagerApproved, FinanceApproved, Rejected, Closed`
- generated `All States` plan
- generated `All Transitions` plan

## Conclusion

The newly added functionality is not only implemented in code. It has also been exercised through repository-level smoke runs and now has traceable output paths for reporting and presentation.
