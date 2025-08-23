# Cognitive SOAR: From Prediction to Attribution

This project enhances the Mini-SOAR tool by integrating threat actor attribution using unsupervised learning. It combines a classification model for malicious URL detection with a clustering model for actor profiling. The workflow is modular, timestamped, and designed for reproducibility across environments.

## Features
-Classification of URLs as MALICIOUS or BENIGN using PyCaret

-Attribution of malicious URLs to one of three synthetic threat actor profiles via clustering

-Streamlit UI with dual-model logic and interactive outputs

-Dockerized Deployment for reproducible execution across platforms

-Timestamped Outputs and annotated code for forensic traceability

## Technologies
Python, PyCaret, scikit-learn, Streamlit, Docker, pandas, seaborn

## Usage
1. Clone the repo git clone https://github.com/annichols84/202502_Analytical-Tools-for-Cyber-Analytics_SEAS_8414_DC.git
2. Follow setup instructions See INSTALL.md for environment setup and dependency management.
3. Run the app streamlit run app.py

## Model Training
The classification model is trained using PyCaret’s supervised learning module. The train_model function handles preprocessing, feature selection, and model tuning. All training steps are timestamped and saved for reproducibility. The trained model is loaded during app runtime to ensure separation of training and inference.

Clustering logic is implemented using scikit-learn’s KMeans, with synthetic actor profiles mapped to cluster IDs. Attribution decisions are visualized in the Streamlit UI and documented for auditability.

## Documentation
1. Blog Post: Threat Actor Attribution Workflow Explains the analytic journey, model logic, and rubric alignment.
2. GitHub Repo: Assignment8_SOAR Contains all code, outputs, and documentation.
