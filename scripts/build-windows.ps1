<#
Build script for Windows: produces a single EXE using PyInstaller.

Usage (PowerShell, repo root):
  .\scripts\build-windows.ps1 -Clean -OneFile -Windowed -Name AutoBeat.exe

Notes:
- Run inside your development venv where dependencies from `requirements-dev.txt` are installed
- Adjust `--add-data` entries if your app bundles external resources (icons, templates)
#>

[CmdletBinding()]
param(
    [switch]$Clean,
    [switch]$OneFile = $true,
    [switch]$Windowed = $false,
    [string]$Name = "AutoBeat.exe",
    [string]$Entry = "main.py"
)

Set-StrictMode -Version Latest

function Ensure-Module {
    param($module)
    try {
        python -c "import $module" 2>$null
    } catch {
        Write-Output "Installing $module into current Python environment..."
        python -m pip install $module
    }
}

Ensure-Module pyinstaller

$pyArgs = @()
if ($OneFile) { $pyArgs += "--onefile" }
if ($Windowed) { $pyArgs += "--windowed" } else { $pyArgs += "--console" }

# Example: include additional data files if needed
# $pyArgs += "--add-data","\"path\to\data;data\""

if ($Clean) {
    Write-Output "Cleaning previous build/dist and spec files..."
    $pathsToRemove = @('.\build', '.\dist', '.\__pycache__')
    foreach ($p in $pathsToRemove) {
        if (Test-Path $p) {
            Remove-Item -LiteralPath $p -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
    Get-ChildItem -Path . -Filter '*.spec' -File -ErrorAction SilentlyContinue | ForEach-Object {
        Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue
    }
}

$pyArgs += "--name"; $pyArgs += ([IO.Path]::GetFileNameWithoutExtension($Name))
$pyArgs += $Entry

# If icon folder contains an .ico, use it
$iconDir = Join-Path $PSScriptRoot "..\icon"
if (Test-Path $iconDir) {
    $ico = Get-ChildItem -Path $iconDir -Filter *.ico -File -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($ico) {
        $pyArgs += "--icon"
        $pyArgs += $ico.FullName
    }
}

Write-Output "Running PyInstaller with args: $pyArgs"
python -m PyInstaller @($pyArgs)

if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Output "Build completed. Output is in .\dist\$([IO.Path]::GetFileNameWithoutExtension($Name))"