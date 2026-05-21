param(
  [string]$Provider = "mock",
  [string]$Model = "mock-arg-test"
)

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python experiments\run_baselines.py --split test --provider $Provider --model $Model
python experiments\export_summary_tables.py --kind baseline --split test
