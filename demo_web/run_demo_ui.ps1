$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

Write-Host "Starting ARG-Test demo UI on http://127.0.0.1:8000" -ForegroundColor Cyan
Start-Process "http://127.0.0.1:8000"
python -m uvicorn demo_web.app:app --host 127.0.0.1 --port 8000
