# Sample blacklist (expand as needed or load from CSV)
phishing_url_blacklist = [
    "https://bncr.com-puntos.bond/pounts/home.html",
    "http://example-phish.com/login",
    "https://paypal.security-update.io",
    # Add more URLs here
]

from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS

# Load the trained model
model = joblib.load("best_model.pkl")

# Create Flask app
app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Check if the URL is in blacklist
        url = data.get("URL") or data.get("url") or ""
        if url in phishing_url_blacklist:
            print("🚨 Blacklisted phishing URL detected:", url)
            return jsonify({"prediction": 1, "reason": "blacklist"})

        # Else, predict using ML model
        df = pd.DataFrame([data])
        df = df.select_dtypes(include=["int64", "float64"])
        prediction = model.predict(df)[0]
        return jsonify({"prediction": int(prediction), "reason": "model"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)

