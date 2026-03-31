param(
  [string]$Provider = "mock",
  [string]$Model = "mock-arg-test",
  [int]$Candidates = 3
)

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python experiments\run_ablation.py --split test --provider $Provider --model $Model --candidates $Candidates
python experiments\export_summary_tables.py --kind ablation --split test

$mainSummary = Join-Path $root 'outputs\reports\test\run_main_summary.json'
if (Test-Path $mainSummary) {
  python experiments\run_generalization.py --split test
  python experiments\export_summary_tables.py --kind generalization --split test
} else {
  Write-Host 'Skip generalization: outputs/reports/test/run_main_summary.json is missing. Ask member 3 to finish the main experiment workflow first.'
}
