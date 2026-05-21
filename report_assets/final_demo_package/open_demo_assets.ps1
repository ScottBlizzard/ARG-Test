$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $repoRoot

$targets = @(
    ".local_runs/final_demo_mock/outputs/reports/adhoc/direct_text_demo_summary.json",
    ".local_runs/final_demo_mock/outputs/final_tests/adhoc/csv_order_workflow.md",
    ".local_runs/final_demo_mock/outputs/state_models/test/warehouse_pickup_order_workflow.md",
    "report_assets/final_demo_package/figures/final_result_scorecard.png",
    "report_assets/final_demo_package/figures/main_vs_baselines.png",
    "report_assets/final_demo_package/figures/reproducibility_stability_overview.png",
    "report_assets/final_demo_package/figures/coupon_module_evidence_scorecard.png"
)

foreach ($relativePath in $targets) {
    $fullPath = Join-Path $repoRoot $relativePath
    if (-not (Test-Path $fullPath)) {
        Write-Warning "Missing asset: $relativePath"
        continue
    }

    switch -Regex ($fullPath) {
        '\.json$' { Start-Process notepad.exe $fullPath; continue }
        '\.md$'   { Start-Process notepad.exe $fullPath; continue }
        default   { Start-Process explorer.exe "/select,`"$fullPath`""; continue }
    }
}

Start-Process explorer.exe (Join-Path $repoRoot ".local_runs\final_demo_mock")
Start-Process explorer.exe (Join-Path $repoRoot "report_assets\final_demo_package\figures")

Write-Host "Opened key demo assets." -ForegroundColor Green
