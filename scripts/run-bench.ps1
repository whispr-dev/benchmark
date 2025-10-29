# run-bench.ps1
param(
    [int]$Total = 200000000,
    [int]$Threads = [Environment]::ProcessorCount,
    [string]$LibPath = "C:\GitHub\C-SIMD-RNG-Lib\lib_files\mingw_shared\universal_rng.dll"
)

$exe = ".\build\rng_bench.exe"
$timestamp = (Get-Date).ToString("yyyy-MM-dd_HH-mm-ss")
$resultsDir = "results"
New-Item -ItemType Directory -Force -Path $resultsDir | Out-Null

$generators = @(
    "std_mt19937",
    "std_mt19937_64",
    "std_minstd",
    "ranlux48",
    "xoroshiro128pp",
    "xoshiro256ss",
    "pcg32",
    "sfmt",
    "csimd"
)

foreach ($gen in $generators) {
    $csvPath = "$resultsDir\bench_${gen}_$timestamp.csv"
    Write-Host "`n==> Running $gen ..."
    & $exe --gens $gen --total $Total --threads $Threads --csv $csvPath --csimd-lib $LibPath
}

Write-Host "`nAll benchmarks done! CSVs saved in '$resultsDir\'."
