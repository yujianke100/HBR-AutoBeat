<#
Creates a project virtual environment in `.venv`, installs development tools,
and installs pre-commit hooks. Run from the repo root in PowerShell.

Usage:
  .\scripts\setup-venv.ps1
#>
Param()

Write-Host "Creating virtual environment at .venv..."
python -m venv .venv
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to create venv. Ensure 'python' is on PATH and points to a compatible Python interpreter."
    exit 1
}

Write-Host "Activating venv and installing dev requirements..."
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt

Write-Host "Installing pre-commit hooks..."
pre-commit install

Write-Host "Done. To activate the venv later run: .\.venv\Scripts\Activate.ps1"