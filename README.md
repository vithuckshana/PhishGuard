# 🛡️ PhishGuard
### AI-Powered Phishing Website Detection System

PhishGuard is a machine learning-based cybersecurity tool that analyzes URL characteristics to detect phishing websites. Users enter a URL and receive an instant prediction, risk score, and breakdown of suspicious features detected.

---

## 🖥️ Demo

## 🖥️ Demo

**Dashboard:**

![Dashboard](https://raw.githubusercontent.com/vithuckshana/PhishGuard/main/screenshots/dashboard.png)

**Legitimate URL:**

![Legitimate Result 1](https://raw.githubusercontent.com/vithuckshana/PhishGuard/main/screenshots/legitimate%20eg1.png)

![Legitimate Result 2](https://raw.githubusercontent.com/vithuckshana/PhishGuard/main/screenshots/legitimate%20eg2.png)

**Phishing URL:**

![Phishing Result 1](https://raw.githubusercontent.com/vithuckshana/PhishGuard/main/screenshots/phishing%20eg1.png)

![Phishing Result 2](https://raw.githubusercontent.com/vithuckshana/PhishGuard/main/screenshots/phishing%20eg2.png)

## 🔍 How It Works

1. User enters a URL
2. 11 security features are extracted from the URL structure
3. A trained Random Forest model predicts: **Legitimate** or **Phishing**
4. A risk score (0–100%) and feature breakdown are displayed
5. Every scan is saved to a local SQLite database

---

## 🧠 Features Extracted

| Feature | Description |
|---|---|
| URL Length | Total character count |
| Number of Dots | Count of `.` in URL |
| Number of Hyphens | Count of `-` in URL |
| Contains IP Address | Whether a raw IPv4 address is used instead of a domain |
| Uses HTTPS | Whether the URL uses a secure connection |
| Special Characters | Count of `@`, `%`, `=`, `&`, `?` |
| Subdomains | Number of subdomains (excluding `www`) |
| URL Entropy | Shannon entropy — measures character randomness |
| Suspicious Keywords | Presence of words like `login`, `verify`, `secure` |
| Digit Count | Number of numeric characters |
| Path Depth | Number of path segments after the domain |

---

## 🤖 ML Model Comparison

All three models were trained on a balanced dataset of 48,812 URLs (50% phishing, 50% legitimate) from PhishTank, URLhaus, and Tranco.

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| Logistic Regression | 99.97% | 100% | 99.94% | 99.97% |
| Decision Tree | 99.97% | 100% | 99.94% | 99.97% |
| **Random Forest** | **99.97%** | **100%** | **99.94%** | **99.97%** |

**Random Forest** was selected as the final model.

> **Note:** The high accuracy reflects the structural clarity of the dataset — legitimate URLs are top-domain homepages (Tranco), while phishing URLs are from active threat feeds (URLhaus, OpenPhish). A more diverse dataset with real browsing traffic would produce more realistic metrics.

---

## ⚙️ Tech Stack

- **Python 3.13**
- **Flask** — web backend
- **scikit-learn** — ML models
- **pandas / numpy** — data processing
- **tldextract** — accurate domain parsing
- **SQLite** — scan history storage
- **HTML / CSS / JavaScript** — frontend

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/vithuckshana/PhishGuard.git
cd PhishGuard

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install flask scikit-learn pandas numpy tldextract joblib matplotlib

# 4. Download the dataset
# Get "Real-World Phishing URL Classification Data" from:
# https://www.kaggle.com/datasets/dhrubangtalukdar/real-world-phishing-url-classification-data
# Place it in data/phishing_url_dataset_unique.csv

# 5. Build the pipeline
python build_features.py
python prepare_data.py
python save_model.py

# 6. Run the app
python app.py
```

Then open `http://localhost:5000` in your browser.

---

## 📁 Project Structure

PhishGuard/
├── src/
│ └── feature_extractor.py # URL feature extraction module
├── templates/
│ └── index.html # Frontend UI
├── data/ # Dataset files (not tracked in git)
├── models/ # Saved ML model (not tracked in git)
├── app.py # Flask backend
├── database.py # SQLite scan history
├── build_features.py # Feature extraction pipeline
├── prepare_data.py # Train/test split
├── train_model.py # Single model training
├── compare_models.py # Model comparison
├── save_model.py # Save final model
└── explore_data.py # Dataset exploration

---

## ⚠️ Limitations

- URL structure analysis only — no domain reputation or page content analysis
- Known legitimate domains with login paths (e.g. `paypal.com/signin`) may trigger false positives due to suspicious keyword detection
- Not a replacement for dedicated security software — intended as a learning project and detection support tool

---

## 👨‍💻 Author

Built as a portfolio and learning project covering cybersecurity, machine learning, and web development.

