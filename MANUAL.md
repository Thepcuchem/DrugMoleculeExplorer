# Drug Molecule Explorer Manual

## Overview
Drug Molecule Explorer is a Tkinter-based desktop app for exploring drug-like small molecules using PubChem, RDKit, and interactive visualization.

## Main Features

### Explorer Tab
- Search by drug name or PubChem CID
- View molecular formula, SMILES, InChI, and identifiers
- Evaluate drug-likeness and property descriptors

### Similar Molecules
- Find related compounds using PubChem similarity search
- Compare fingerprints and chemical similarity scores

### Comparison
- Compare two molecules side-by-side
- See descriptor differences and structural features

### About
- Shows the application startup graphic
- Provides a short app description and attribution

## Running the App
1. Activate the virtual environment
2. Run `python DME.py`
3. Wait for the splash screen to close, then use the application tabs

## Dependencies
- `tkinter`
- `pubchempy`
- `rdkit-pypi`
- `Pillow`

## Troubleshooting
- If the splash image does not appear, ensure `startup.png` is in the same folder as `DME.py`.
- If PubChem lookup fails, check your internet connection.
- If RDKit import fails, reinstall using a supported wheel or conda package.

## File Export
- Use the `Save PDB` button to export the current 3D molecule structure to a `.pdb` file.

## Tips
- Enter molecule names or CIDs directly in the search field.
- Use the `About` menu to revisit the startup graphic and app description.
