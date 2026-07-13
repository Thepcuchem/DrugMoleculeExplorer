# Drug Molecule Explorer
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21336829.svg)](https://doi.org/10.5281/zenodo.21336829)

A User-Friendly Desktop Application for Interactive Small-Molecule Exploration

## Contents
- `DME.py` — main application source code
- `startup.png` — splash/startup graphic shown on launch and in the About tab
- `requirements.txt` — Python package dependencies
- `MANUAL.md` — user guide and feature reference

## Prerequisites
- Python 3.10 or newer
- `tkinter` (usually included with Python on Windows)
- `rdkit-pypi` for cheminformatics and molecular rendering
- `pubchempy` for PubChem data lookup
- `Pillow` for image loading and splash screen handling

## Installation
1. Open a terminal in the project folder:
   ```powershell
   cd c:\DrugExplorer\DrugMoleculeExplorer_GitHub
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Running the app
```powershell
python DME.py
```

## Running tests
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## Continuous Integration
This repository includes a GitHub Actions workflow at `.github/workflows/ci.yml`.
It runs on pushes and pull requests to `main`, installs dependencies from `requirements.txt`, and executes the test suite.

## Citation
If you use this software in research or teaching, please cite this repository using the metadata in `CITATION.cff`.

## Notes
- Make sure `startup.png` is present in the project root so the splash screen and About tab display correctly.
- If RDKit installation fails on Windows, try using `conda` or the `rdkit-pypi` wheel build.

## Packaging
For distribution, include:
- `DME.py`
- `startup.png`
- `requirements.txt`
- `MANUAL.md`
- any custom startup assets or sample files needed by the app
