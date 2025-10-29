\
# rename_headers_by_platform.ps1
Param(
  [string]$base = "D:\code\Universal-Architecture-RNG-Lib\v1.7",
  [string[]]$platforms = @("win_msvc","win_msys2","linux","macos")
)

foreach ($p in $platforms) {
  $src = Join-Path $base "$p\ua_rng-1.7\include\ua"
  if (Test-Path $src) {
    Get-ChildItem $src -Filter *.h | ForEach-Object {
      $new = Join-Path $src ("{0}_{1}" -f $p, $_.Name)
      Rename-Item -Path $_.FullName -NewName (Split-Path $new -Leaf)
    }
  }
}
Write-Host "Done."
