# BioProteinAI

BioProteinAI is a bioinformatics machine learning project that predicts protein subcellular localization from amino acid sequences.

## Goal

The model predicts whether a protein is likely to be localized in the nucleus or cytoplasm.

## Methods

- Protein sequence feature extraction
- Amino acid composition analysis
- Molecular weight
- Isoelectric point
- GRAVY score
- Instability index
- Random Forest classifier
- Streamlit dashboard

## Technologies

- Python
- Biopython
- Pandas
- Scikit-learn
- Streamlit

## How to Run

pip install -r requirements.txt

streamlit run app/streamlit_app.py
