# app.py

import streamlit as st
import pandas as pd
from pycaret.classification import load_model as load_classification_model, predict_model as predict_classification
from pycaret.clustering import load_model as load_clustering_model, predict_model as predict_clustering
import os

# Step 1: Configure Streamlit Page
st.set_page_config(page_title="GenAI-Powered Phishing SOAR", layout="wide")

# Step 2: Load Models and Optional Feature Plot
@st.cache_resource
def load_assets():
    clf_path = 'models/phishing_url_detector'
    cluster_path = 'models/threat_actor_profiler'
    plot_path = 'models/feature_importance.png'

    clf_model = load_classification_model(clf_path) if os.path.exists(clf_path + '.pkl') else None
    cluster_model = load_clustering_model(cluster_path) if os.path.exists(cluster_path + '.pkl') else None
    plot = plot_path if os.path.exists(plot_path) else None

    return clf_model, plot, cluster_model

model, feature_plot, cluster_model = load_assets()

if not model:
    st.error("Classification model not found. Please run training first or check logs.")
    st.stop()

# Step 3: Collect User Inputs via Sidebar
with st.sidebar:
    st.title("URL Feature Input")
    st.write("Describe the characteristics of a suspicious URL below.")

    test_case = st.selectbox("Load a Test Case", options=["None", "Benign", "Cybercrime", "State-Sponsored", "Hacktivist"])

    preset_inputs = {
        "Benign": {
            'url_length': 'Normal', 'ssl_state': 'Trusted', 'sub_domain': 'One',
            'prefix_suffix': False, 'has_ip': False, 'short_service': False,
            'at_symbol': False, 'double_slash': False, 'anchor': 'Trusted',
            'links_in_tags': 'Trusted', 'sfh': 'Trusted', 'abnormal_url': False,
            'political_keyword': False
        },
        "Cybercrime": {
            'url_length': 'Long', 'ssl_state': 'None', 'sub_domain': 'Many',
            'prefix_suffix': True, 'has_ip': True, 'short_service': True,
            'at_symbol': True, 'double_slash': True, 'anchor': 'Suspicious',
            'links_in_tags': 'Suspicious', 'sfh': 'Suspicious', 'abnormal_url': True,
            'political_keyword': False
        },
        "State-Sponsored": {
            'url_length': 'Normal', 'ssl_state': 'Trusted', 'sub_domain': 'One',
            'prefix_suffix': True, 'has_ip': False, 'short_service': False,
            'at_symbol': False, 'double_slash': False, 'anchor': 'Neutral',
            'links_in_tags': 'Neutral', 'sfh': 'Neutral', 'abnormal_url': False,
            'political_keyword': False
        },
        "Hacktivist": {
            'url_length': 'Long', 'ssl_state': 'Suspicious', 'sub_domain': 'Many',
            'prefix_suffix': True, 'has_ip': True, 'short_service': False,
            'at_symbol': True, 'double_slash': True, 'anchor': 'Suspicious',
            'links_in_tags': 'Neutral', 'sfh': 'Suspicious', 'abnormal_url': True,
            'political_keyword': True
        }
    }

    if test_case != "None":
        form_values = preset_inputs[test_case]
    else:
        form_values = {
        'url_length': st.select_slider("URL Length", options=['Short', 'Normal', 'Long']),
        'ssl_state': st.select_slider("SSL Certificate Status", options=['Trusted', 'Suspicious', 'None']),
        'sub_domain': st.select_slider("Sub-domain Complexity", options=['None', 'One', 'Many']),
        'prefix_suffix': st.checkbox("URL has a Prefix/Suffix (e.g., '-')"),
        'has_ip': st.checkbox("URL uses an IP Address"),
        'short_service': st.checkbox("Is it a shortened URL"),
        'at_symbol': st.checkbox("URL contains '@' symbol"),
        'double_slash': st.checkbox("URL contains '//' after protocol"),
        'anchor': st.select_slider("Anchor Tag Behavior", options=['Trusted', 'Neutral', 'Suspicious']),
        'links_in_tags': st.select_slider("Links in Tags", options=['Trusted', 'Neutral', 'Suspicious']),
        'sfh': st.select_slider("Server Form Handler (SFH)", options=['Trusted', 'Neutral', 'Suspicious']),
        'abnormal_url': st.checkbox("URL is Abnormal (e.g., doesn't match domain)"),
        'political_keyword': st.checkbox("Contains Political Keywords")
    }


# Step 4: Display Feature Importance Plot
if feature_plot:
    st.image(feature_plot, caption="Feature Importance", use_column_width=True)

# Step 5: Run Predictions
if st.button("Run Attribution"):
    input_df = pd.DataFrame([form_values])

    # Classification
    clf_result = predict_classification(model, data=input_df)
    predicted_label = clf_result.loc[0, 'Label']
    prediction_score = clf_result.loc[0, 'Score']

    st.subheader("🛡️ Phishing Classification Result")
    st.markdown(f"- **Predicted Label:** `{predicted_label}`")
    st.markdown(f"- **Confidence Score:** `{prediction_score:.2f}`")

    # Clustering
    if cluster_model:
        cluster_result = predict_clustering(cluster_model, data=input_df)
        cluster_label = cluster_result.loc[0, 'Cluster']

        st.subheader("🎯 Threat Actor Attribution")
        st.markdown(f"- **Assigned Cluster:** `{cluster_label}`")

        cluster_map = {
            0: "Benign",
            1: "Cybercrime",
            2: "State-Sponsored",
            3: "Hacktivist"
        }
        actor_type = cluster_map.get(cluster_label, "Unknown")
        st.markdown(f"- **Likely Actor Type:** `{actor_type}`")

        st.info("This attribution is based on clustering of behavioral URL features. Please validate against known threat actor profiles and campaign metadata.")

    # Step 6: Optional Export
    if st.checkbox("Save Prediction to CSV"):
        output_df = pd.DataFrame({
            "Predicted Label": [predicted_label],
            "Confidence Score": [prediction_score],
            "Assigned Cluster": [cluster_label],
            "Actor Type": [actor_type]
        })
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outputs/prediction_{timestamp}.csv"
        output_df.to_csv(filename, index=False)
        st.success(f"Prediction saved as {filename}")

    # Step 7: Justification Block
    with st.expander("📄 Attribution Justification"):
        st.markdown("""
        The classification model predicts phishing likelihood based on behavioral URL features.
        The clustering model assigns threat actor types using unsupervised profiling.

        - **Benign**: Low-risk, trusted indicators  
        - **Cybercrime**: High-risk, evasive patterns  
        - **State-Sponsored**: Neutral but strategic indicators  
        - **Hacktivist**: Politically charged and disruptive traits  

        Please validate results against campaign metadata and known actor profiles.
        """)
