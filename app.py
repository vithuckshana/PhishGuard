"""
app.py
-------
PhishGuard Flask backend.
Handles URL submissions, runs feature extraction,
loads the saved model, and returns predictions.
"""

import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify

from src.feature_extractor import extract_features
from database import init_db, save_scan, get_recent_scans, get_stats

app = Flask(__name__)

# Load the trained model once when the server starts
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
    features = extract_features(url)
    features_df = pd.DataFrame([features])[FEATURE_COLUMNS]

    prediction = model.predict(features_df)[0]
    probabilities = model.predict_proba(features_df)[0]
    risk_score = round(probabilities[1] * 100, 1)

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
    """Serve the main page with recent scans and stats."""
    recent_scans = get_recent_scans(limit=10)
    stats = get_stats()
    return render_template("index.html", recent_scans=recent_scans, stats=stats)


@app.route("/scan", methods=["POST"])
def scan():
    """
    Receives a URL from the frontend, runs prediction,
    saves to database, and returns the result as JSON.
    """
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = predict_url(url)

    # Save to database
    save_scan(
        url=result["url"],
        prediction=result["prediction"],
        risk_score=result["risk_score"],
        confidence=result["confidence"],
    )

    return jsonify(result)


@app.route("/history")
def history():
    """Returns full scan history as JSON."""
    scans = get_recent_scans(limit=50)
    return jsonify(scans)


if __name__ == "__main__":
    init_db()  # Create DB/table if not exists
    app.run(debug=True)