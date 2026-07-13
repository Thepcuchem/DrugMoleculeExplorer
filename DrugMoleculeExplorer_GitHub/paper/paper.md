**Drug Molecule Explorer: A User-Friendly Desktop Application for
Interactive Small-Molecule Exploration**

Jiyeon Hong^1,2^, Pisit Lerttanakit^1^, Pornthep Sompornpisut^1,^\*

^1^Center of Excellence in Computational Chemistry, Department of
Chemistry, Faculty of Science, Chulalongkorn University, Bangkok 10330,
Thailand

^2^NIST International School, Bangkok 10110, Thailand

\*To whom correspondence should be addressed:

Pornthep Sompornpisut: pornthep.s@chula.ac.th, 662-2187707

**Summary**

Drug Molecule Explorer (DME) is an open-source, cross-platform desktop
application for interactive exploration of small-molecule compounds
through an intuitive graphical user interface (GUI). The software
enables users to search the PubChem database using compound names or
PubChem Compound Identifiers (CIDs), retrieve molecular information,
visualize chemical structures in two-dimensional (2D) and interactive
three-dimensional (3D) representations, calculate physicochemical and
drug-likeness descriptors, compare structurally related compounds, and
export molecular structures in SDF or Protein Data Bank (PDB) format for
further analysis. By integrating these commonly used molecular
exploration functions into a single application, DME provides a
streamlined workflow that requires no programming experience. DME is
implemented in Python using the Tkinter GUI framework and integrates
several widely used open-source libraries, including PubChemPy for
compound retrieval, RDKit for molecular representation, descriptor
calculation, fingerprint generation, similarity analysis, and
three-dimensional coordinate generation, and Pillow for image
processing. The lightweight desktop application is intended for chemical
education and routine molecular exploration by students, educators, and
researchers in chemistry-related disciplines, providing an accessible
platform for rapid preliminary characterization and visualization of
small molecules.

**Statement of need**

Exploration of small-molecule compounds is a fundamental task in
chemistry, medicinal chemistry, pharmacology, biochemistry, and chemical
education. Common activities include retrieving molecular information
from public databases, visualizing chemical structures, calculating
physicochemical descriptors, evaluating drug-likeness, and comparing
structurally related compounds. Although these tasks can be performed
using open-source cheminformatics libraries such as RDKit (Landrum
2006), public chemical databases such as PubChem (Kim, Chen et al. 2025,
Mahato 2025), or commercial molecular modeling software, they often
require programming expertise, multiple software packages, or commercial
licenses that may limit accessibility for many users. Drug Molecule
Explorer (DME) addresses this gap by providing a lightweight,
cross-platform desktop application that integrates compound retrieval,
molecular visualization, physicochemical descriptor calculation,
drug-likeness evaluation (Lipinski, Lombardo et al. 2001, Veber, Johnson
et al. 2002), similarity analysis, and molecular structure export within
a single graphical user interface. By combining these commonly used
functions into an intuitive desktop application, DME enables students,
educators, and researchers to perform routine molecular exploration
without programming experience. The software is particularly well suited
for chemical education, classroom demonstrations, and rapid preliminary
characterization of small molecules.

**State of the field**

Open-source cheminformatics software provides powerful tools for
molecular representation, property calculation, and chemical data
analysis. RDKit (Landrum 2006) is a widely used cheminformatics library
that supports molecular manipulation, descriptor calculation,
fingerprint generation, and similarity analysis, while PubChem (Kim,
Chen et al. 2025, Mahato 2025) offers one of the largest publicly
accessible repositories of chemical structures and associated biological
information. Molecular visualization programs such as Avogadro (Hanwell,
Curtis et al. 2012) provide interactive inspection and editing of
three-dimensional molecular structures. These resources are widely
adopted within the cheminformatics community but are primarily designed
as programming libraries or specialized visualization tools. DME
complements these established resources by integrating compound
retrieval, molecular visualization, physicochemical descriptor
calculation, drug-likeness evaluation, similarity analysis, and
molecular structure export within a single graphical desktop
application. Rather than replacing existing cheminformatics software,
DME provides an accessible interface that enables students, educators,
and researchers to perform routine molecular exploration without
programming experience while leveraging the capabilities of mature
open-source libraries.

**Software architecture and functionality**

DME is implemented in Python as a lightweight, cross-platform desktop
application with a graphical user interface (GUI) developed using
Tkinter. The software integrates molecular retrieval, visualization,
descriptor calculation, similarity analysis, and molecular comparison
within a unified workflow (Figure 1). It leverages several widely
adopted open-source libraries, including PubChemPy for retrieving
compound information from PubChem, RDKit for molecular representation,
physicochemical descriptor calculation, molecular fingerprinting,
similarity analysis, and three-dimensional coordinate generation, and
Pillow for image processing.

The **Explorer** tab (Figure 1A) serves as the primary interface for
molecular exploration. Users can search for compounds using either a
chemical name or a PubChem Compound Identifier (CID). Retrieved
compounds are displayed together with two-dimensional (2D) and
interactive three-dimensional (3D) molecular representations, molecular
metadata (e.g., molecular formula, SMILES (Weininger 1988), and InChI
(IUPAC 2007)), physicochemical descriptors, and drug-likeness properties
based on Lipinski\'s Rule of Five and Veber\'s criteria (Lipinski,
Lombardo et al. 2001, Veber, Johnson et al. 2002). Molecular structures
can also be exported in SDF or Protein Data Bank (PDB) format for
subsequent analysis using external molecular visualization software.

The **Similar Molecules** tab (Figure 1B) retrieves structurally related
compounds from PubChem and ranks them according to molecular fingerprint
similarity. The **Comparison** tab (Figure 1C) enables side-by-side
comparison of two compounds by displaying their molecular structures,
physicochemical descriptors, and similarity scores, facilitating rapid
evaluation of structural and property differences.

By integrating these commonly used functions into a single desktop
application, DME provides an efficient workflow for molecular
exploration, making it suitable for chemical education, classroom
demonstrations, and preliminary analysis of small-molecule compounds.

![](media/image1.png){width="6.0in" height="3.0833333333333335in"}

**Figure 1.** Graphical user interface of **Drug Molecule Explorer**.
**(A)** Explorer tab for compound retrieval, molecular visualization,
descriptor calculation, and structure export. **(B)** Similar Molecules
tab for fingerprint-based similarity search. **(C)** Comparison tab for
side-by-side comparison of molecular structures and physicochemical
descriptors.

**Software Availability**

DME is freely available as an open-source software package through the
project repository. The repository provides the source code,
documentation, installation instructions, and example files. DME is
developed in Python and builds upon several widely adopted open-source
libraries, including PubChemPy, RDKit, Pillow, and Tkinter.

**Acknowledgements**

This project was funded by Thailand Science research and Innovation Fund
Chulalongkorn University (HEA_FF_69_244_2300_055).

**References**

Hanwell, M. D., D. E. Curtis, D. C. Lonie, T. Vandermeersch, E. Zurek
and G. R. Hutchison (2012). \"Avogadro: an advanced semantic chemical
editor, visualization, and analysis platform.\" [J
Cheminform]{.underline} **4**(1): 17.DOI: 10.1186/1758-2946-4-17

IUPAC (2007). \"The IUPAC International Chemical Identifier (InChI).\"
[J. Cheminform.]{.underline}

Kim, S., J. Chen, T. Cheng, A. Gindulyte, J. He, S. He, Q. Li, B. A.
Shoemaker, P. A. Thiessen, B. Yu, L. Zaslavsky, J. Zhang and E. E.
Bolton (2025). \"PubChem 2025 update.\" [Nucleic Acids Res]{.underline}
**53**(D1): D1516-D1525.DOI: 10.1093/nar/gkae1059

Landrum, G. (2006). \"RDKit: Open-source cheminformatics.
<https://www.rdkit.org>.\"

Lipinski, C. A., F. Lombardo, B. W. Dominy and P. J. Feeney (2001).
\"Experimental and computational approaches to estimate solubility and
permeability in drug discovery and development settings.\" [Adv Drug
Deliv Rev]{.underline} **46**(1-3): 3-26.DOI:
10.1016/s0169-409x(00)00129-0

Mahato, S. (2025). \"A Python-Based Workflow for Computing and
Extracting Drug-Like Compounds from PubChem.\" [Methods Mol
Biol]{.underline} **2927**: 287-306.DOI: 10.1007/978-1-0716-4546-8_16

Veber, D. F., S. R. Johnson, H. Y. Cheng, B. R. Smith, K. W. Ward and K.
D. Kopple (2002). \"Molecular properties that influence the oral
bioavailability of drug candidates.\" [J Med Chem]{.underline}
**45**(12): 2615-2623.DOI: 10.1021/jm020017n

Weininger, D. (1988). \"SMILES, a chemical language and information
system. 1. Introduction to methodology and encoding rules.\" [J. Chem.
Inf. Comput. Sci.]{.underline} **28**(1): 31--36.DOI:
<https://doi.org/10.1021/ci00057a005>
