# Blockchain–AI Drug Repurposing

## Overview
An AI-based drug repurposing project that uses an ensemble of three pretrained DeepPurpose models to predict drug–target interaction scores and records drug–disease prediction results in a custom blockchain ledger.

## Key Features
- Drug SMILES retrieval through the PubChem REST API
- Disease-associated gene and protein filtering using CTD and UniProt datasets
- Ensemble prediction using three pretrained DeepPurpose/PyTorch models
- SHA-256-based blockchain ledger for recording prediction results
- Blockchain integrity validation and ledger inspection
- Interactive Streamlit user interface

## Technology Stack
Python, Streamlit, PyTorch, DeepPurpose, Pandas, NumPy, Requests, JSON, SHA-256

## Project Files
- `app.py` — application interface and prediction workflow
- `blockchain.py` — custom blockchain implementation
- `Drug_Repurposing_Ensemble.ipynb` — model development and evaluation notebook

## Requirements
The application requires three pretrained model directories (`saved_model`, `saved_model2`, and `saved_model3`) and the CTD and UniProt datasets under the expected paths. These resources are not currently included in this repository.

## Run the Application
After setting up the required Python environment, datasets, and model files, run:

```bash
streamlit run app.py
```

## Disclaimer
This project is for educational and research purposes. Model predictions are not medical advice and do not establish clinical efficacy.

## Role
B.Tech mini project — Team Lead. Coordinated task distribution and supported integration and testing.
