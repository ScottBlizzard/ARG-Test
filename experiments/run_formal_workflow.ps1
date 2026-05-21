param(
    [ValidateSet('mock', 'openai')]
    [string]$Provider = 'mock',
    [string]$Model = 'mock-arg-test',
    [int]$Candidates = 3,
    [ValidateSet('responses', 'chat_completions')]
    [string]$ApiMode = 'chat_completions',
    [int]$Seed = 202601,
    [double]$Temperature = 0.0,
    [double]$TopP = 1.0,
    [string]$OutputRoot = '.local_runs/formal_run'
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

python experiments/check_runtime_ready.py --provider $Provider --model $Model --candidates $Candidates --api-mode $ApiMode --seed $Seed --temperature $Temperature --top-p $TopP --output-root $OutputRoot
python experiments/run_main.py --split dev --provider $Provider --model $Model --candidates $Candidates --api-mode $ApiMode --seed $Seed --temperature $Temperature --top-p $TopP --output-root $OutputRoot
python experiments/run_main.py --split test --provider $Provider --model $Model --candidates $Candidates --api-mode $ApiMode --seed $Seed --temperature $Temperature --top-p $TopP --output-root $OutputRoot
python experiments/run_baselines.py --split test --provider $Provider --model $Model --api-mode $ApiMode --seed $Seed --temperature $Temperature --top-p $TopP --output-root $OutputRoot
python experiments/run_ablation.py --split test --provider $Provider --model $Model --candidates $Candidates --api-mode $ApiMode --seed $Seed --temperature $Temperature --top-p $TopP --output-root $OutputRoot
python experiments/run_generalization.py --split test --provider $Provider --model $Model --candidates $Candidates --api-mode $ApiMode --seed $Seed --temperature $Temperature --top-p $TopP --output-root $OutputRoot
python experiments/export_summary_tables.py --kind all --split dev --output-root $OutputRoot
python experiments/export_summary_tables.py --kind all --split test --output-root $OutputRoot

Write-Host "Formal workflow completed. Runtime root: $OutputRoot"
