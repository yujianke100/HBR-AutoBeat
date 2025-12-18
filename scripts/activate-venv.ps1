<# Activate the project's virtual environment (.venv) on Windows PowerShell

Usage (from repo root):
  .\scripts\activate-venv.ps1

This script locates `.venv\Scripts\Activate.ps1` and invokes it in the current session.
If running in PowerShell Core (`pwsh`), it will try to source the correct Activate script.
#>

conda deactivate

Set-StrictMode -Version Latest

$venvPath = Join-Path $PSScriptRoot "..\.venv\Scripts\Activate.ps1"
if (-Not (Test-Path $venvPath)) {
    Write-Error "Virtual environment activation script not found at $venvPath. Ensure .venv exists and is created."
    exit 1
}

Write-Output "Sourcing virtual environment: $venvPath"
. $venvPath