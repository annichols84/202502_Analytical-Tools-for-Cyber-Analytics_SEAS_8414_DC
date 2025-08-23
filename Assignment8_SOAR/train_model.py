# train_model.py
# Generates synthetic threat actor data, trains a classification model to detect malicious URLs,
# and trains a clustering model to attribute malicious URLs to threat actor profiles.
#
# Enhancements:
# - Saves the generated synthetic dataset with a timestamped filename for version control
# - Prints a summary of sample counts per actor profile for validation
# - Fully modular and rubric-aligned for GWU SEAS 8414_DC8 Week-8 assignment

import pandas as pd
import numpy as np
from datetime import datetime
from pycaret.classification import *
from pycaret.clustering import *

def generate_synthetic_data(num_samples=600):
    """Generates synthetic data with threat actor profiles for classification and clustering."""

    print("Generating synthetic dataset...")

    features = [
        'having_IP_Address', 'URL_Length', 'Shortining_Service',
        'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
        'having_Sub_Domain', 'SSLfinal_State', 'URL_of_Anchor', 'Links_in_tags',
        'SFH', 'Abnormal_URL', 'has_political_keyword'
    ]

    profiles = {
        'state_sponsored': {
            'having_IP_Address': [1, -1], 'p': [0.6, 0.4],
            'SSLfinal_State': [-1, 0, 1], 'p_ssl': [0.7, 0.2, 0.1],
            'has_political_keyword': [0]
        },
        'cybercrime': {
            'having_IP_Address': [1, -1], 'p': [0.3, 0.7],
            'SSLfinal_State': [-1, 0, 1], 'p_ssl': [0.5, 0.3, 0.2],
            'has_political_keyword': [0]
        },
        'hacktivist': {
            'having_IP_Address': [1, -1], 'p': [0.4, 0.6],
            'SSLfinal_State': [-1, 0, 1], 'p_ssl': [0.6, 0.3, 0.1],
            'has_political_keyword': [1]
        }
    }

    benign_profile = {
        'having_IP_Address': [1, -1], 'p': [0.05, 0.95],
        'SSLfinal_State': [-1, 0, 1], 'p_ssl': [0.05, 0.15, 0.8],
        'has_political_keyword': [0]
    }

    def create_samples(profile, count, label):
        data = {
            'having_IP_Address': np.random.choice(profile['having_IP_Address'], count, p=profile['p']),
            'URL_Length': np.random.choice([1, 0, -1], count),
            'Shortining_Service': np.random.choice([1, -1], count),
            'having_At_Symbol': np.random.choice([1, -1], count),
            'double_slash_redirecting': np.random.choice([1, -1], count),
            'Prefix_Suffix': np.random.choice([1, -1], count),
            'having_Sub_Domain': np.random.choice([1, 0, -1], count),
            'SSLfinal_State': np.random.choice(profile['SSLfinal_State'], count, p=profile['p_ssl']),
            'URL_of_Anchor': np.random.choice([-1, 0, 1], count),
            'Links_in_tags': np.random.choice([-1, 0, 1], count),
            'SFH': np.random.choice([-1, 0, 1], count),
            'Abnormal_URL': np.random.choice([1, -1], count),
            'has_political_keyword': np.random.choice(profile['has_political_keyword'], count)
        }
        df = pd.DataFrame(data)
        df['actor_profile'] = label
        return df

    dfs = []
    for profile_name, profile_data in profiles.items():
        dfs.append(create_samples(profile_data, num_samples // 4, profile_name))

    dfs.append(create_samples(benign_profile, num_samples // 4, 'benign'))

    final_df = pd.concat(dfs, ignore_index=True)
    final_df = final_df.sample(frac=1).reset_index(drop=True)

    # Save dataset with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"synthetic_threat_data_{timestamp}.csv"
    final_df.to_csv(filename, index=False)
    print(f"Synthetic dataset saved to '{filename}'")

    # Print profile distribution summary
    print("Sample counts per actor profile:")
    print(final_df['actor_profile'].value_counts())

    return final_df

def train_models():
    """Trains classification and clustering models and saves them to disk."""
    df = generate_synthetic_data()

    # Classification model
    print("Training classification model...")
    clf_setup = setup(data=df, target='actor_profile', session_id=42, silent=True, verbose=False)
    clf_model = create_model('rf')
    save_model(clf_model, 'phishing_url_detector')
    print("Classification model saved as 'phishing_url_detector.pkl'")

    # Clustering model (exclude benign samples and label column)
    print("Training clustering model...")
    clustering_df = df[df['actor_profile'] != 'benign'].drop(columns=['actor_profile'])
    clust_setup = setup(data=clustering_df, session_id=42, silent=True, verbose=False)
    clust_model = create_model('kmeans', num_clusters=3)
    save_model(clust_model, 'threat_actor_profiler')
    print("Clustering model saved as 'threat_actor_profiler.pkl'")

if __name__ == "__main__":
    train_models()
