# Tests

This folder contains automated checks for repository integrity and code sanity.

## Run tests

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## Scope

Current tests are lightweight and avoid importing `DME.py` directly because it launches a GUI at import time.
They validate that core files exist and that `DME.py` is syntactically parseable.
