"""
compare_models.py
------------------
Trains multiple ML models on the same dataset and compares their
performance so we can pick the best one for PhishGuard.

Models:
  - Logistic Regression  (simple baseline)
  - Decision Tree        (interpretable, single tree)
  - Random Forest        (ensemble, our current best)
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

# Load the prepared splits
X_train = pd.read_csv("data/X_train.csv")
X_test  = pd.read_csv("data/X_test.csv")
y_train = pd.read_csv("data/y_train.csv").squeeze()
y_test  = pd.read_csv("data/y_test.csv").squeeze()

# Define all models to compare
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Decision Tree":       DecisionTreeClassifier(random_state=42),
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
}

# Train and evaluate each one
results = []

for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    results.append({
        "Model":     name,
        "Accuracy":  round(accuracy_score(y_test, y_pred),  4),
        "Precision": round(precision_score(y_test, y_pred), 4),
        "Recall":    round(recall_score(y_test, y_pred),    4),
        "F1 Score":  round(f1_score(y_test, y_pred),        4),
    })
    print(f"  Done. F1: {results[-1]['F1 Score']}")

print()
print("=" * 65)
print("MODEL COMPARISON")
print("=" * 65)

results_df = pd.DataFrame(results).set_index("Model")
print(results_df.to_string())

print()
print(f"Best model by F1:      {results_df['F1 Score'].idxmax()}")
print(f"Best model by Recall:  {results_df['Recall'].idxmax()}")