3_explain_and_prescribe.py


# Step 1: Load Scoring Output 
import pandas as pd
results = pd.read_csv("model/scoring_output.csv")

# Step 2: Train Surrogate Model for SHAP 
from sklearn.ensemble import GradientBoostingClassifier
import shap

df = pd.read_csv("dga_dataset_train.csv")
X_train = df[['length', 'entropy']]
y_train = df['class']
surrogate_model = GradientBoostingClassifier().fit(X_train, y_train)

# Step 3: Explain Predictions 
explainer = shap.Explainer(surrogate_model, X_train)
X_test = results[['length', 'entropy']]
shap_values = explainer(X_test)

# Step 4: Summarize SHAP Contributions 
summaries = []
for i, row in results.iterrows():
    contribs = shap_values[i].values
    summary = f"{row['domain']} classified as {row['predict']} due to length={row['length']} and entropy={row['entropy']}. SHAP: length={contribs[0]:.2f}, entropy={contribs[1]:.2f}."
    summaries.append(summary)

# Step 5: GenAI Prompt (Pseudocode) 
for s in summaries:
    prompt = f"Given this domain classification summary:\n{s}\nGenerate a prescriptive incident response playbook for a SOC analyst."
    # response = genai.generate(prompt)  # Replace with actual GenAI call
    print(prompt)
    # print(response)