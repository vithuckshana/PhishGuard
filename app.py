"""
app.py
-------
PhishGuard Flask backend.
Handles URL submissions, runs feature extraction,
loads the saved model, and returns predictions.
"""

import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify

from src.feature_extractor import extract_features

app = Flask(__name__)

# Load the trained model once when the server starts
# (not on every request — that would be slow)
MODEL_PATH = "models/phishguard_model.pkl"
model = joblib.load(MODEL_PATH)

# Feature column order must match exactly what the model was trained on
FEATURE_COLUMNS = [
    "url_length",
    "num_dots",
    "num_hyphens",
    "has_ip",
    "has_https",
    "num_special_chars",
    "num_subdomains",
    "url_entropy",
    "has_suspicious_words",
    "num_digits",
    "path_depth",
]


def predict_url(url: str) -> dict:
    """
    Takes a raw URL string, extracts features, runs the model,
    and returns a result dictionary with prediction and risk score.
    """
    # Extract features
    features = extract_features(url)

    # Convert to DataFrame with correct column order
    features_df = pd.DataFrame([features])[FEATURE_COLUMNS]

    # Get prediction: 0 = legitimate, 1 = phishing
    prediction = model.predict(features_df)[0]

    # Get probability scores [prob_legitimate, prob_phishing]
    probabilities = model.predict_proba(features_df)[0]
    risk_score = round(probabilities[1] * 100, 1)  # phishing probability as %

    # Build result
    result = {
        "url": url,
        "prediction": "phishing" if prediction == 1 else "legitimate",
        "risk_score": risk_score,
        "confidence": round(max(probabilities) * 100, 1),
        "features": features,
    }

    return result


@app.route("/")
def index():
    """Serve the main page."""
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    """
    Receives a URL from the frontend, runs prediction,
    and returns the result as JSON.
    """
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = predict_url(url)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)