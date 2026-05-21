param(
    [string]$PptxPath = 'report_assets/figures/arg_test_architecture_editable.pptx',
    [string]$OutputDir = 'report_assets/figures/architecture_png'
)

$projectRoot = Split-Path -Parent $PSScriptRoot
$resolvedPptx = Join-Path $projectRoot $PptxPath
$resolvedOutput = Join-Path $projectRoot $OutputDir

New-Item -ItemType Directory -Force -Path $resolvedOutput | Out-Null

$powerpoint = $null
$presentation = $null
try {
    $powerpoint = New-Object -ComObject PowerPoint.Application
    $powerpoint.Visible = -1
    $presentation = $powerpoint.Presentations.Open($resolvedPptx, $true, $false, $false)
    $presentation.Export($resolvedOutput, 'PNG', 2400, 1350)
}
finally {
    if ($presentation) { $presentation.Close() }
    if ($powerpoint) { $powerpoint.Quit() }
}

Write-Output $resolvedOutput
