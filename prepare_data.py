"""
prepare_data.py
----------------
Loads the feature dataset, and splits into training and
test sets ready for ML.
"""

import pandas as pd
from sklearn.model_selection import train_test_split

# Load the feature dataset
df = pd.read_csv("data/features.csv")

print("Loaded:", df.shape)
print()

# Labels are already 0/1 — no encoding needed
print("Label balance:")
print(df["label"].value_counts())
print()

# Separate features (X) from label (y)
X = df.drop("label", axis=1)
y = df["label"]

# Split into 80% training, 20% test
# stratify=y preserves the 50/50 class ratio in both splits
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Training set:", X_train.shape)
print("Test set:    ", X_test.shape)
print()
print("Training label balance:")
print(y_train.value_counts())
print()
print("Test label balance:")
print(y_test.value_counts())

# Save all four splits
X_train.to_csv("data/X_train.csv", index=False)
X_test.to_csv("data/X_test.csv", index=False)
y_train.to_csv("data/y_train.csv", index=False)
y_test.to_csv("data/y_test.csv", index=False)

print()
print("Saved X_train, X_test, y_train, y_test to data/")