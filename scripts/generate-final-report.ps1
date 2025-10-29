# generate-final-report.ps1
# Works in Windows PowerShell 5.x and PowerShell 7+

Write-Host "[INFO] Generating final cross-platform benchmark report..."

# --- paths ---
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
$resultsDir = Join-Path $root "results"
$outputPng  = Join-Path $resultsDir "cross_compiler_dashboard_final.png"
$outputPdf  = Join-Path $resultsDir "cross_compiler_dashboard_final.pdf"
$dashboardScript = Join-Path $root "plot-cross-platform-adv.py"

# --- MiKTeX / latex check ---
$latexCmd = Get-Command latex.exe -ErrorAction SilentlyContinue
if ($latexCmd) {
    Write-Host ("[OK] MiKTeX detected at: " + $latexCmd.Source)
} else {
    Write-Warning "MiKTeX not found; PDF export will still work via Pandoc only."
}

# --- gather csvs ---
$csvFiles = Get-ChildItem -Path $resultsDir -Filter "*.csv" -Recurse | Select-Object -ExpandProperty FullName
if (-not $csvFiles) {
    Write-Host "[ERROR] No CSV files found in $resultsDir"
    exit 1
}

Write-Host "[INFO] Found $($csvFiles.Count) CSV files:"
$csvFiles | ForEach-Object { Write-Host "  $_" }

# --- baseline detection ---
$baselineCsv = ($csvFiles | Where-Object { $_ -match "windows-msvc" } | Select-Object -First 1)
if ($baselineCsv) {
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($baselineCsv)
    $baselineName = $stem -replace '^bench_all_', ''
} else {
    $baselineName = "windows-msvc"
}
Write-Host "[INFO] Using baseline: $baselineName"


# --- run python plotter ---
$pythonExe = "python"
$cmdArgs = @($dashboardScript, "--output", $outputPng, "--baseline", $baselineName)
Write-Host "[INFO] Running: $pythonExe $($cmdArgs -join ' ')"
& $pythonExe @cmdArgs
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python plotting failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

# --- write text summary ---
$reportText = @"
# Cross-Platform RNG Benchmark Report
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Baseline: $baselineName
CSV files used: $($csvFiles.Count)
Dashboard image: $outputPng
"@
$tempTxt = Join-Path $resultsDir "report_temp.txt"
Set-Content -Path $tempTxt -Value $reportText -Encoding UTF8

# --- run python plotter ---
$pythonExe = "python"
$cmdArgs = @($dashboardScript, "--baseline", $baselineName)
Write-Host "[INFO] Running: $pythonExe $($cmdArgs -join ' ')"
& $pythonExe @cmdArgs
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python plotting failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

