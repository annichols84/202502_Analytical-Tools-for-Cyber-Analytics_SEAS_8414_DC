# 1_train_and_export.py

# Import required libraries

import csv
import random
import math
import os

# Ensure H2O is installed before importing
!pip install -q h2o

import h2o
from h2o.automl import H2OAutoML

# Step 1: Generate Synthetic DGA Dataset

def get_entropy(s):
    p, lns = {}, float(len(s))
    for c in s:
        p[c] = p.get(c, 0) + 1
    return -sum(count/lns * math.log(count/lns, 2) for count in p.values())

header = ['domain', 'length', 'entropy', 'class']
data = []

legit_domains = ['google', 'facebook', 'amazon', 'github', 'wikipedia', 'microsoft']
for _ in range(300):
    domain = random.choice(legit_domains) + ".com"
    data.append([domain, len(domain), get_entropy(domain), 'legit'])

for _ in range(300):
    length = random.randint(15, 25)
    domain = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(length)) + ".com"
    data.append([domain, len(domain), get_entropy(domain), 'dga'])

with open('dga_dataset_train.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
print(" Dataset saved as dga_dataset_train.csv")

# Step 2: Train Model Using H2O AutoML 

h2o.init()
train = h2o.import_file("dga_dataset_train.csv")
x = ['length', 'entropy']
y = 'class'
train[y] = train[y].asfactor()

aml = H2OAutoML(max_models=20, max_runtime_secs=120, seed=1)
aml.train(x=x, y=y, training_frame=train)

print(" AutoML training complete")
print(" Leaderboard (Top Models):")
print(aml.leaderboard.head())

# Step 3: Export Leaderboard for Auditability 

os.makedirs("model", exist_ok=True)
aml.leaderboard.as_data_frame().to_csv("model/leaderboard.csv", index=False)
print(" Leaderboard exported to model/leaderboard.csv")

# Step 4: Export and Rename MOJO Model 

mojo_path = aml.leader.download_mojo(path="./model/")
print(f" MOJO model saved to: {mojo_path}")

# Rename to rubric-aligned filename
renamed_path = "model/DGA_Leader.zip"
if os.path.exists(mojo_path):
    os.rename(mojo_path, renamed_path)
    print(" Renamed model to DGA_Leader.zip")
else:
    print(" MOJO file not found. Rename skipped.")

# Also export native H2O model for Python-based scoring
native_path = h2o.save_model(model=aml.leader, path="./model", force=True)
print(f" Native model saved to: {native_path}")
