param(
  [string]$Provider = "mock",
  [string]$Model = "mock-arg-test",
  [int]$Candidates = 3
)

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python experiments\validate_data_assets.py --split all
python experiments\run_main.py --split dev --provider $Provider --model $Model --candidates $Candidates
python experiments\run_main.py --split test --provider $Provider --model $Model --candidates $Candidates
python experiments\export_summary_tables.py --kind main --split dev
python experiments\export_summary_tables.py --kind main --split test
