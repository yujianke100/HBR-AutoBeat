# HOWTO — Contributors

This short HOWTO explains common tasks for contributors.

## Run

1. Create and activate virtualenv (Windows PowerShell):

```powershell
.\scripts\activate-venv.ps1
```

2. Install development dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

3. Run the app:

```powershell
python .\main.py
```

## Run linters & type checks

    flake8 .
    mypy . --install-types

## Run tests

Unit tests live in `tests/`. Use pytest:

    python -m pytest -q

## Build

Build distributable artifacts (see `build.bat` / `scripts/build-windows.ps1`).
