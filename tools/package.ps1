# Package Modern Control Map (The Witcher 3) for testing:
#   1. tools\build_map.py --check  (map.json is what the map builds)
#   2. copy dist\ and the banners to <stage>\Witcher 3 - Modern Control Map\Modern Control Map <VERSION>\
#   3. stamp the version into the package README (rule 6: the version at the top of the README)
# The version comes from VERSION, which only version-gate.ps1 writes. The stage folder comes from the project's resolver
# (distro-names.ps1 Resolve-PackageRoot), never a hand-joined path.
param(
    [string]$ProjectRoot = 'D:\Claude output',
    [string]$Stage = '7. current test builds',
    # an optional file (build_map.py VARIANTS): alt1 = Witcher Senses on LB in exploration (the owner, 2026-10-07)
    [ValidateSet('', 'alt1')][string]$Variant = ''
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$version = (Get-Content -LiteralPath (Join-Path $repo 'VERSION') -Raw).Trim()
if ($version -notmatch '^\d+\.\d+\.\d+$' -or $version -eq '0.0.0') { throw "VERSION is '$version' - issue a number with version-gate.ps1 -Action bump first" }

& python -I (Join-Path $PSScriptRoot 'build_map.py') --check
if ($LASTEXITCODE -ne 0) { throw 'build_map.py --check failed - the package is not built' }

. (Join-Path $ProjectRoot '.MD\scripts\distro-names.ps1')
$root = Resolve-PackageRoot -Root (Join-Path $ProjectRoot $Stage) -ModName 'Modern Control Map' -Game 'Witcher 3' -ProjectRoot $ProjectRoot
$suffix = if ($Variant) { ' ' + ($Variant -replace '^alt(\d+)$', 'alt $1') } else { '' }
$pkg = Join-Path $root "Modern Control Map $version$suffix"
if (Test-Path -LiteralPath $pkg) { throw "$pkg already exists - a version is packaged once" }
New-Item -ItemType Directory -Force -Path $pkg | Out-Null
Copy-Item -Path (Join-Path $repo 'dist\*') -Destination $pkg -Recurse
Copy-Item -LiteralPath (Join-Path $repo 'LICENSE') -Destination $pkg
if ($Variant) {
    $mapOut = Join-Path $pkg 'Modern Control Map Installer\map.json'
    & python -I (Join-Path $PSScriptRoot 'build_map.py') --variant $Variant --out $mapOut
    if ($LASTEXITCODE -ne 0) { throw "build_map.py --variant $Variant failed" }
}

$readme = Join-Path $pkg 'README.txt'
$text = [System.IO.File]::ReadAllText($readme)
$text = [regex]::Replace($text, '(?m)^Version \d+\.\d+\.\d+', "Version $version", 1)
if ($Variant -eq 'alt1') {
    # the README's own lines for the one binding Alt 1 moves; each must be found, or the package stops
    # the middle dot is written by its code: Windows PowerShell reads this file as ANSI, not UTF-8
    $dot = [string][char]0x00B7
    # regex patterns (any line break / indent between words), each replaced once
    $pairs = @(
        @("Exploration   LT cast sign $dot L-Stick hold Witcher Senses, press twice call Roach $dot D-pad Up quick item",
          "Exploration   LT cast sign $dot LB hold Witcher Senses $dot L-Stick press twice call Roach $dot D-pad Up quick item"),
        @('which the map gives to Witcher(\s+)Senses, Roach and the quick item\.',
          'which the map gives to Roach and$1the quick item.')
    )
    foreach ($p in $pairs) {
        $pattern = if ($p[0].Contains($dot)) { [regex]::Escape($p[0]) } else { $p[0] }
        if (-not [regex]::IsMatch($text, $pattern)) { throw "README text not found for Alt 1: $($p[0])" }
        $text = ([regex]$pattern).Replace($text, $p[1], 1)
    }
    $text = [regex]::Replace($text, '(?m)^(Version \d+\.\d+\.\d+)', '$1 - Alt 1: Witcher Senses on LB (exploration) instead of holding the left stick', 1)
}
[System.IO.File]::WriteAllText($readme, $text, (New-Object System.Text.UTF8Encoding($false)))

Write-Output "packaged $pkg"
