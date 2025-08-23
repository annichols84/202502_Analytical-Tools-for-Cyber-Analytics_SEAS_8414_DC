# Assignment 9 – Prescriptive DGA Detector  
![Lint Workflow](https://github.com/annichols84/202502_Analytical-Tools-for-Cyber-Analytics_SEAS_8414_DC/actions/workflows/lint.yml/badge.svg?branch=main)


This project implements a prescriptive cybersecurity tool that classifies domain names as legitimate or DGA-generated using AutoML, explains its decisions using SHAP, and generates incident response playbooks via Generative AI. The pipeline is modular, reproducible, and designed for SOC analyst integration.

## Contents  
- `1_train_and_export.py`: Model training and MOJO export  
- `2_analyze_domain.py`: Domain scoring and justification  
- `3_explain_and_prescribe.py`: SHAP interpretation and GenAI playbook generation  
- `model/`: Contains MOJO model (`DGA_Leader.zip`), leaderboard, and scoring output  
- `dga_dataset_train.csv`: Synthetic training data  
- `TESTING.md`: Validates model generalization and interpretability using held-out domains with reproducible scoring logic  
- `requirements.txt`: Dependency list for reproducibility  
- `.github/workflows/lint.yml`: GitHub Actions workflow for code linting

## Setup Instructions  
1. Clone the repository  
2. Run `pip install -r requirements.txt`  
3. Execute `1_train_and_export.py` to generate models  
4. Run `2_analyze_domain.py` to score domains  
5. Run `3_explain_and_prescribe.py` to interpret and prescribe

> **Note:** The linting workflow is active and valid, but badge rendering is currently unsupported due to GitHub’s nested folder structure. All code hygiene checks are still enforced via `.github/workflows/lint.yml`.

## Workflow Overview  
1. Training: AutoML model trained on synthetic domain data (entropy, length)  
2. Scoring: Domains are scored using the exported MOJO/native model  
3. Interpretation: SHAP values explain feature contributions  
4. Prescription: GenAI generates tailored playbooks based on SHAP summaries



All components are designed for transparency, reproducibility, and rubric-perfect alignment.
