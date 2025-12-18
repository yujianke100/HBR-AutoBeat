#!/usr/bin/env bash
# Create a project virtual environment in .venv, install dev tools and pre-commit hooks.

set -euo pipefail

python -m venv .venv
echo "Activating .venv and installing dev requirements..."
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
echo "Installing pre-commit hooks..."
pre-commit install
echo "Done. To activate venv: source .venv/bin/activate"