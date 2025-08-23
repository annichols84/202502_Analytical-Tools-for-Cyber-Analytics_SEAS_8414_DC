# Installation Guide

## Prerequisites
- Python 3.10+
- pip
- Docker (optional for containerized deployment)
- Streamlit

## Setup Steps

### 1. Clone the Repository
```bash
git clone https://github.com/annichols84/202502_Analytical-Tools-for-Cyber-Analytics_SEAS_8414_DC.git
cd 202502_Analytical-Tools-for-Cyber-Analytics_SEAS_8414_DC/Assignment8_SOAR

### 2. Install Dependencies
```bash
pip install -r requirements.txt

### 3. Run the Streamlit App
```bash
streamlit run app.py

4. (Optional) Docker Deployment
```bash
docker-compose up --build
