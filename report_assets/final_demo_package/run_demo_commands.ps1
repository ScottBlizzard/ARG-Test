$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $repoRoot

$outputRoot = ".local_runs/final_demo_mock"

Write-Host ""
Write-Host "=== ARG-Test Final Demo: direct text input ===" -ForegroundColor Cyan
@'
Requirement ID: direct_text_demo
Rules:
1. A request starts in Draft.
2. Submit is allowed only from Draft and moves the request to Submitted.
3. Approve is allowed only from Submitted and moves the request to Approved.
4. Reject is allowed only from Submitted and moves the request to Rejected.
5. Approve from Draft must be blocked.
'@ | python -m src.main run-text --requirement-id direct_text_demo --split adhoc --provider mock --output-root $outputRoot

Write-Host ""
Write-Host "=== ARG-Test Final Demo: CSV batch input ===" -ForegroundColor Cyan
python -m src.main batch-csv --input final_docs\execution_evidence\sample_requirement_batch.csv --provider mock --output-root $outputRoot

Write-Host ""
Write-Host "=== ARG-Test Final Demo: state-model extraction ===" -ForegroundColor Cyan
python -m src.main state-model --input data\requirements\test\warehouse_pickup_order_workflow.txt --provider mock --output-root $outputRoot

Write-Host ""
Write-Host "Demo outputs are ready under: $outputRoot" -ForegroundColor Green
Write-Host "Open these files during recording:" -ForegroundColor Yellow
Write-Host "  - .local_runs/final_demo_mock/outputs/reports/adhoc/direct_text_demo_summary.json"
Write-Host "  - .local_runs/final_demo_mock/outputs/final_tests/adhoc/csv_order_workflow.md"
Write-Host "  - .local_runs/final_demo_mock/outputs/state_models/test/warehouse_pickup_order_workflow.md"
