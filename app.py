import streamlit as st
import pandas as pd
import numpy as np
import requests

from DeepPurpose import DTI as models
from DeepPurpose.utils import data_process

# Initialize Blockchain
from blockchain import Blockchain
blockchain = Blockchain()

# -------------------------------
# Load Models (PyTorch DeepPurpose)
# -------------------------------

@st.cache_resource
def load_models():
    model1 = models.model_pretrained('./saved_model')
    model2 = models.model_pretrained('./saved_model2')
    model3 = models.model_pretrained('./saved_model3')
    return model1, model2, model3


model1_loaded, model2_loaded, model3_loaded = load_models()


# -------------------------------
# Fetch SMILES from PubChem
# -------------------------------

def get_smiles_from_pubchem(drug_name):
    drug_name = drug_name.strip()

    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{drug_name}/property/SMILES/JSON"

    try:
        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            return None

        data = response.json()

        props = data.get("PropertyTable", {}).get("Properties", [])

        if len(props) == 0:
            return None

        # ✅ Correct key from your JSON
        return props[0].get("SMILES", None)

    except Exception:
        return None

# -------------------------------
# Ensemble Prediction
# -------------------------------

def ensemble_predict(smiles, seq):
    df = data_process(
        X_drug=[smiles],
        X_target=[seq],
        y=[0],
        drug_encoding=model1_loaded.config['drug_encoding'],
        target_encoding=model1_loaded.config['target_encoding'],
        split_method='no_split'
    )

    pred1 = model1_loaded.predict(df)[0]
    pred2 = model2_loaded.predict(df)[0]
    pred3 = model3_loaded.predict(df)[0]

    return np.mean([pred1, pred2, pred3])


def predict_drug_disease(smiles, protein_list):
    scores = []
    for seq in protein_list:
        score = ensemble_predict(smiles, seq)
        scores.append(score)

    return max(scores)


# -------------------------------
# Load Required Data (CTD + UniProt Filtered)
# -------------------------------

@st.cache_data
def load_disease_proteins():
    # Load CTD file
    ctd_df = pd.read_csv(
        "data/CTD_curated_genes_diseases.tsv.gz",
        sep="\t",
        compression="gzip",
        comment="#",
        header=None
    )

    ctd_df.columns = [
        "GeneSymbol",
        "GeneID",
        "DiseaseName",
        "DiseaseID",
        "DirectEvidence",
        "InferenceScore",
        "PubMedIDs"
    ]

    # Load UniProt kinase dataset
    kinase_df = pd.read_csv(
        "data\\uniprotkb_organism_id_9606_AND_keyword_2026_02_25 (1).tsv.gz",
        sep="\t",
        compression="gzip"
    )

    kinase_df["PrimaryGene"] = kinase_df["Gene Names"].str.split().str[0]

    return ctd_df, kinase_df


ctd_df, kinase_df = load_disease_proteins()

# -------------------------------
# Prepare Dropdown Options
# -------------------------------
# -------------------------------
# Prepare Valid Disease Dropdown
# -------------------------------

valid_genes = set(kinase_df["PrimaryGene"])

valid_diseases = ctd_df[
    ctd_df["GeneSymbol"].isin(valid_genes)
]["DiseaseName"].dropna().unique()

disease_options = sorted(valid_diseases)


# Example drug list (safe, commonly found in PubChem)
drug_options = [
    "Aspirin",
    "Ibuprofen",
    "Metformin",
    "Atorvastatin",
    "Imatinib",
    "Paracetamol",
    "Dexamethasone",
    "Warfarin",
    "Cisplatin",
    "Paclitaxel"
]
# -------------------------------
# Streamlit UI
# -------------------------------

st.set_page_config(page_title="Drug Repurposing AI", layout="wide")

st.title("💊 AI-Based Drug Repurposing System")
st.markdown("Predict potential drug-disease interaction using Deep Learning Ensemble")

drug_name = st.selectbox(
    "Select Drug",
    drug_options
)

disease_name = st.selectbox(
    "Select Disease",
    disease_options
)
if st.button("Predict"):

    st.write("Searching Drug:", drug_name)

    with st.spinner("Fetching SMILES..."):
        smiles = get_smiles_from_pubchem(drug_name)

    if smiles is None:
        st.error("Drug not found in PubChem.")
        st.stop()

    st.success(f"SMILES Found: {smiles}")

    disease_genes = ctd_df[
        ctd_df["DiseaseName"].str.lower() == disease_name.lower()
    ]["GeneSymbol"].unique()

    disease_proteins = kinase_df[
        kinase_df["PrimaryGene"].isin(disease_genes)
    ]

    protein_list = disease_proteins["Sequence"].tolist()

    st.info(f"Running prediction on {len(protein_list)} proteins...")

    final_score = predict_drug_disease(smiles, protein_list)

    st.success(f"Final Drug-Disease Score: {final_score:.4f}")

    block_data = {
        "drug": drug_name,
        "disease": disease_name,
        "score": float(final_score)
    }

    block_hash = blockchain.add_block(block_data)

    st.success("Prediction stored securely in Blockchain ✅")
    st.write("Block Hash:", block_hash)


# Validate blockchain
if st.button("Validate Blockchain"):

    if blockchain.is_chain_valid():
        st.success("Blockchain is valid ✅")
    else:
        st.error("Blockchain integrity compromised ❌")


# View ledger
if st.button("View Blockchain Ledger"):
    for block in blockchain.chain:
        st.json(block.__dict__)