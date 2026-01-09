# PowerShell helper to install pre-commit hooks for this repo
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)
Write-Host "Installing pre-commit and hooks..."

# If running inside a virtualenv, do NOT use --user. Detect virtualenv via $VIRTUAL_ENV or presence of Scripts/activate.
if ((($env:VIRTUAL_ENV -ne $null) -and ($env:VIRTUAL_ENV -ne "")) -or (Test-Path (Join-Path $PSScriptRoot '.venv')) -or (Test-Path (Join-Path $PSScriptROOT 'venv'))) {
	Write-Host "Detected virtual environment. Installing into the active environment..."
	python -m pip install --upgrade pip
	python -m pip install pre-commit
} else {
	Write-Host "No virtual environment detected. Installing for current user..."
	python -m pip install --user --upgrade pip
	python -m pip install --user pre-commit
	# Add user Scripts to PATH for current session if needed
	$userScripts = Join-Path $env:USERPROFILE "AppData\Roaming\Python\Python$((Get-Command python).FileVersionInfo.FileVersion.Split('.')[0])\Scripts"
	if (Test-Path $userScripts) { $env:PATH += ";$userScripts" }
}

# Install hooks
pre-commit install --install-hooks
pre-commit install -t pre-push
Write-Host "Hooks installed. Run 'pre-commit run --all-files' to verify."