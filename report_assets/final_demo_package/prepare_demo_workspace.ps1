$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== Step 1: run demo commands ===" -ForegroundColor Cyan
powershell -ExecutionPolicy Bypass -File (Join-Path $scriptRoot 'run_demo_commands.ps1')

Write-Host ""
Write-Host "=== Step 2: open demo assets ===" -ForegroundColor Cyan
powershell -ExecutionPolicy Bypass -File (Join-Path $scriptRoot 'open_demo_assets.ps1')

Write-Host ""
Write-Host "Demo workspace is ready for recording." -ForegroundColor Green
