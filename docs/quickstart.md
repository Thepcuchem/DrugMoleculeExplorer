# Quickstart

## 1) Create and activate environment (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2) Install dependencies

```powershell
pip install -r requirements.txt
```

## 3) Run the app

```powershell
python DME.py
```

## 4) Basic usage

1. Enter a molecule name or PubChem CID in the search field.
2. Open the `Similar Molecules` and `Comparison` tabs after a successful query.
3. Export structure data using built-in save actions where available.

## Notes

- Keep `startup.png` in the repository root for splash/About graphics.
- Internet access is required for PubChem lookups.
