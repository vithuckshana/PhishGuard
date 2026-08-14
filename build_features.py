"""
build_features.py
------------------
Applies the feature extractor to the full cleaned dataset and
saves a new CSV with numeric features + label, ready for ML training.
"""

import pandas as pd
from src.feature_extractor import extract_features

# Load cleaned dataset
df = pd.read_csv("data/phishing_urls_clean.csv")
print("Loaded:", df.shape)

# Apply feature extraction to every URL
# This returns a list of dicts, one per row
feature_dicts = df["URL"].apply(extract_features)

# Convert list of dicts into a proper DataFrame
features_df = pd.DataFrame(list(feature_dicts))

# Attach the label column back on
features_df["label"] = df["Label"].values

print("Features shape:", features_df.shape)
print()
print(features_df.head())

# Save it
features_df.to_csv("data/features.csv", index=False)
print()
print("Saved to data/features.csv")