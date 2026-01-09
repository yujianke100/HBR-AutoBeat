# Contributing

Thanks for contributing! Please follow the guidelines below to keep the repository healthy.

## Pre-commit and CI requirements

- All commits pushed to remote branches MUST pass the project's checks before creating a PR or pushing to protected branches.
- Run the full local pre-commit checks before pushing:

```powershell
# install hooks (one-time):
pre-commit install --install-hooks
# ensure pre-push hook is installed:
pre-commit install -t pre-push
# run all checks locally:
pre-commit run --all-files
```

- If `pre-commit` auto-modifies files (formatters), re-run `git add` and commit the formatting changes.
- The CI pipeline also runs linters and type checks; ensure your branch CI is green before requesting reviews.

## Branch protection and PR process

- Protect `main` and release branches with required status checks (lint, mypy, tests).
- Open a PR and ensure CI passes; reviewers will not merge until required checks are green.

## Hook installation helper (Windows PowerShell)

Run the following once per machine to ensure the pre-push hook is active:

```powershell
# from project root
python -m pip install --upgrade pip
pip install pre-commit
pre-commit install --install-hooks
pre-commit install -t pre-push
```

If you prefer to use the provided project helper script, run `scripts\install-hooks.ps1` (Windows PowerShell).
