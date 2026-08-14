"""
save_model.py
--------------
Trains the final Random Forest model on the full training set
and saves it to disk so Flask can load it for predictions.
"""

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load the prepared splits
X_train = pd.read_csv("data/X_train.csv")
y_train = pd.read_csv("data/y_train.csv").squeeze()

print("Training final Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)
print("Done.")

# Save to models/ folder
joblib.dump(model, "models/phishguard_model.pkl")
print("Model saved to models/phishguard_model.pkl")