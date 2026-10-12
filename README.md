# Blockchain–AI Drug Repurposing

## Overview

An AI-based drug repurposing system that uses an ensemble of three pretrained DeepPurpose models to predict drug–target interaction scores and records drug–disease prediction results in a custom blockchain ledger.

The project combines deep learning, biological datasets, external APIs, and blockchain-based integrity verification in an interactive Streamlit application.

## Key Features

- **Drug Information Retrieval:** Retrieves drug SMILES representations using the PubChem REST API.
- **Disease–Protein Mapping:** Filters disease-associated genes and proteins using CTD and UniProt datasets.
- **Ensemble Prediction:** Combines predictions from three pretrained DeepPurpose/PyTorch models.
- **Blockchain-Based Recordkeeping:** Stores prediction results in a custom blockchain ledger using SHA-256 hashing.
- **Integrity Validation:** Supports blockchain integrity checking and ledger inspection.
- **Interactive Interface:** Provides a Streamlit interface for selecting drugs and diseases and viewing prediction results.

## Technology Stack

- **Programming Language:** Python
- **Frontend:** Streamlit
- **Machine Learning:** PyTorch, DeepPurpose
- **Data Processing:** Pandas, NumPy
- **External APIs:** PubChem REST API
- **Biological Data Sources:** CTD, UniProt
- **Blockchain:** Custom Python implementation, SHA-256
- **Environment Management:** Anaconda/Conda

## Project Structure

```text
blockchain-ai-drug-repurposing/
├── app.py
├── blockchain.py
├── requirements.txt
├── Drug_Repurposing_Ensemble.ipynb
├── README.md
├── data/
│   ├── CTD dataset
│   └── UniProt dataset
├── saved_model/
├── saved_model2/
└── saved_model3/
```

The dataset and model filenames may differ from the simplified structure shown above. The application expects the required resources at the paths configured in `app.py`.

## Prerequisites

- Python 3.10
- Anaconda or Miniconda
- Git
- The required biological datasets
- The three pretrained model directories

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sravyarachuri/blockchain-ai-drug-repurposing.git
cd blockchain-ai-drug-repurposing
```

### 2. Create and Activate the Conda Environment

```bash
conda create -n drug_env python=3.10 -y
conda activate drug_env
```

### 3. Install RDKit

Install RDKit through Conda:

```bash
conda install -c conda-forge rdkit
```

### 4. Install Python Dependencies

Install the dependencies listed in `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

**Compatibility note:** The project uses DeepPurpose, PyTorch, TensorFlow, and RDKit. Compatible package versions may be required. The installation instructions should be tested in a fresh environment before being treated as a fully reproducible setup.

### 5. Prepare the Datasets and Model Files

Ensure the following resources are available locally:

- `saved_model/` — first pretrained model
- `saved_model2/` — second pretrained model
- `saved_model3/` — third pretrained model
- CTD disease-associated gene dataset
- UniProt protein dataset

The exact filenames and paths must match the references in `app.py`.

If these resources are not available after cloning, obtain them separately before running predictions.

### 6. Run the Application

From the project root directory, execute:

```bash
streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to access the application.

## How to Use

1. Open the Streamlit application.
2. Select a drug from the available options.
3. Select a disease from the available options.
4. Click **Predict**.
5. Review the resulting drug–disease prediction score.
6. Check the blockchain confirmation and use the ledger inspection or validation functionality if available.

The application depends on the configured datasets and pretrained models being available and loadable.

## Project Files

| File                                             | Description                                           |
| ------------------------------------------------ | ----------------------------------------------------- |
| `app.py`                                         | Streamlit interface and prediction workflow           |
| `blockchain.py`                                  | Custom blockchain and integrity-related functionality |
| `Drug_Repurposing_Ensemble.ipynb`                | Model development and evaluation notebook             |
| `requirements.txt`                               | Python dependency list                                |
| `data/`                                          | Biological datasets used by the application           |
| `saved_model/`, `saved_model2/`, `saved_model3/` | Pretrained model resources                            |

## Role and Contribution

**B.Tech Mini Project — Team Lead**

## Disclaimer

This project is intended for educational and research purposes only. The prediction scores are computational estimates and must not be interpreted as medical advice, proof of drug effectiveness, or evidence of clinical safety. Any potential drug repurposing candidate requires appropriate scientific and clinical validation.

## Repository

GitHub: [https://github.com/sravyarachuri/blockchain-ai-drug-repurposing](https://github.com/sravyarachuri/blockchain-ai-drug-repurposing)
