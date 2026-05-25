
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from Bio.SeqUtils.ProtParam import ProteinAnalysis

BASE_DIR = Path(__file__).resolve().parents[1]

model = joblib.load(BASE_DIR / "models" / "protein_localization_model.pkl")
encoder = joblib.load(BASE_DIR / "models" / "label_encoder.pkl")
feature_columns = joblib.load(BASE_DIR / "models" / "feature_columns.pkl")

STANDARD_AA = set("ACDEFGHIKLMNPQRSTVWY")

def clean_protein_sequence(sequence):
    sequence = str(sequence).upper()
    return "".join([aa for aa in sequence if aa in STANDARD_AA])

def extract_protein_features(sequence):
    sequence = clean_protein_sequence(sequence)

    if len(sequence) < 30:
        return None

    analysis = ProteinAnalysis(sequence)

    features = {
        "length": len(sequence),
        "molecular_weight": analysis.molecular_weight(),
        "aromaticity": analysis.aromaticity(),
        "instability_index": analysis.instability_index(),
        "isoelectric_point": analysis.isoelectric_point(),
        "gravy": analysis.gravy()
    }

    aa_counts = analysis.count_amino_acids()

    for aa, count in aa_counts.items():
        features[f"aa_{aa}"] = count / len(sequence)

    return features

st.title("BioProteinAI")
st.subheader("Protein Localization Prediction")

st.write("This app predicts whether a protein is likely to be Nuclear or Cytoplasmic based on sequence-derived features.")

sequence = st.text_area("Enter protein sequence:")

if st.button("Predict Localization"):
    features = extract_protein_features(sequence)

    if features is None:
        st.error("Please enter a valid protein sequence with at least 30 amino acids.")
    else:
        input_df = pd.DataFrame([features])
        input_df = input_df.reindex(columns=feature_columns, fill_value=0)

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]

        label = encoder.inverse_transform([prediction])[0]
        confidence = max(probability)

        st.success(f"Predicted Localization: {label}")
        st.metric("Confidence", f"{confidence:.2%}")
        st.dataframe(input_df)
