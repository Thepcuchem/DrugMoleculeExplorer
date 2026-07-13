# Contributing Guide

Thank you for your interest in contributing to this project.

## How to Contribute

1. Fork the repository.
2. Create a feature branch from `main`.
3. Make your changes in small, focused commits.
4. Run checks and tests locally.
5. Open a pull request with a clear description.

## Local Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the main script:

```bash
python DME.py
```

## Coding Style

- Follow PEP 8 style conventions.
- Keep functions small and focused.
- Add docstrings for non-trivial functions.
- Avoid introducing unnecessary dependencies.

## Testing

- Add or update tests in the `tests/` folder for code changes.
- Ensure existing behavior remains backward compatible unless a breaking change is intentional and documented.

## Pull Request Checklist

- [ ] Code runs locally.
- [ ] Documentation is updated (README, MANUAL, or docs when needed).
- [ ] Tests are added or updated.
- [ ] Changelog entry is added under `Unreleased` when applicable.

## Reporting Issues

When creating an issue, include:

- Operating system and Python version.
- Clear reproduction steps.
- Expected behavior and actual behavior.
- Logs or traceback text if available.
