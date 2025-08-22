2_analyze_domain.py

# === Optional: Install Performance Dependencies ===
# Enables multi-threaded H2OFrame → pandas conversion
!pip install -q polars pyarrow

# Import Required Libraries
import math
import pandas as pd
import h2o

# Step 1: Define Entropy Calculation 
def get_entropy(s):
    p, lns = {}, float(len(s))
    for c in s:
        p[c] = p.get(c, 0) + 1
    return -sum((count / lns) * math.log(count / lns, 2) for count in p.values())

# Step 2: Feature Extraction Function 
def extract_features(domains):
    return pd.DataFrame([{
        'domain': d,
        'length': len(d),
        'entropy': get_entropy(d)
    } for d in domains])

# Step 3: Initialize H2O and Load Native Model 
h2o.init()
model_path = "./model/GBM_5_AutoML_7_20250822_182627"  # Update if needed
model = h2o.load_model(model_path)

# Step 4: Input Domains 
input_domains = [
    "securelogin.microsoft.com",
    "xj29q8v2k3l0z9a.com",
    "github.com",
    "a8b7c6d5e4f3g2h1.com"
]

# Step 5: Feature Extraction 
features_df = extract_features(input_domains)
h2o_frame = h2o.H2OFrame(features_df[['length', 'entropy']])

# Step 6: Prediction with Multi-Threaded Conversion
preds = model.predict(h2o_frame).as_data_frame(use_multi_thread=True)
results = pd.concat([features_df, preds], axis=1)

# Step 7: Output Results
print(" Domain Classification Results:")
print(results[['domain', 'length', 'entropy', 'predict']])

