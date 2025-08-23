# Cognitive SOAR: From Prediction to Attribution

This project enhances the Mini-SOAR tool by integrating threat actor attribution using unsupervised learning. It combines a classification model for malicious URL detection with a clustering model for actor profiling.

## Features
- Classification of URLs as MALICIOUS or BENIGN
- Attribution of malicious URLs to one of three threat actor profiles
- Streamlit UI with dual-model logic
- Dockerized deployment

## Technologies
Python, PyCaret, scikit-learn, Streamlit, Docker

## Usage
1. Clone the repo
2. Follow `INSTALL.md` for setup
3. Run the app with `streamlit run app.py`
