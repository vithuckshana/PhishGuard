"""
train_model.py
---------------
Trains a Random Forest classifier on the prepared feature dataset
and evaluates it on the held-out test set.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# Load the prepared splits
X_train = pd.read_csv("data/X_train.csv")
X_test  = pd.read_csv("data/X_test.csv")
y_train = pd.read_csv("data/y_train.csv").squeeze()
y_test  = pd.read_csv("data/y_test.csv").squeeze()

print("Training Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,   # 100 decision trees in the forest
    random_state=42,    # reproducible results
    n_jobs=-1,          # use all CPU cores to speed up training
)

model.fit(X_train, y_train)
print("Done.")
print()

# Evaluate on test set
y_pred = model.predict(X_test)

print("=" * 50)
print("RESULTS — Random Forest")
print("=" * 50)
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred):.4f}")
print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
print(f"F1 Score:  {f1_score(y_test, y_pred):.4f}")
print()
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print()
print("Full Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Legitimate", "Phishing"]))

# Feature importance
print("=" * 50)
print("FEATURE IMPORTANCE")
print("=" * 50)
importance = pd.Series(
    model.feature_importances_,
    index=X_train.columns
).sort_values(ascending=False)
print(importance)