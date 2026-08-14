"""
build_features.py
------------------
Applies the feature extractor to the cleaned dataset and
saves a new CSV with numeric features + label, ready for ML training.
"""

import pandas as pd
from src.feature_extractor import extract_features

# Load new dataset
df = pd.read_csv("data/phishing_url_dataset_unique.csv")
print("Loaded:", df.shape)

# Apply feature extraction to every URL
feature_dicts = df["url"].apply(extract_features)

# Convert to DataFrame
features_df = pd.DataFrame(list(feature_dicts))

# Attach label (already 0/1, no encoding needed)
features_df["label"] = df["label"].values

print("Features shape:", features_df.shape)
print()
print(features_df.head())

# Save
features_df.to_csv("data/features.csv", index=False)
print()
print("Saved to data/features.csv")