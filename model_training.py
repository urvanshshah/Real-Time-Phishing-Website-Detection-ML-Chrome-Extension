import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from adversarial_features import detect_adversarial_patterns

# 🌍 Multilingual keyword matcher
def has_multilingual_keywords(text):
    multilingual_keywords = [
        "login", "iniciar sesión", "connexion", "anmelden", "ورود", "ログイン",
        "verify", "verificar", "vérifier", "überprüfen", "تحقق", "確認",
        "account", "cuenta", "compte", "konto", "الحساب", "アカウント",
        "secure", "seguro", "sécurisé", "sicher", "آمن", "安全",
        "update", "actualizar", "mettre à jour", "aktualisieren", "تحديث", "アップデート"
    ]
    text = str(text).lower()
    return int(any(keyword in text for keyword in multilingual_keywords))

# === Load and prepare dataset === #
print("📦 Loading PhiUSIIL dataset...")
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

# Drop rows missing essential info
df = df.dropna(subset=["URL", "label"])
df = df.reset_index(drop=True)

# Simulate HTML with Title (used for adversarial + multilingual analysis)
df["html_content"] = df["Title"].fillna("")

# === Adversarial + Multilingual Feature Extraction === #
print("🛡️ Adding adversarial features...")
adversarial_features = df["html_content"].apply(detect_adversarial_patterns).apply(pd.Series)

print("🌐 Adding multilingual keyword feature...")
df["has_multilingual_keywords"] = df["html_content"].apply(has_multilingual_keywords)

# Combine features
df = pd.concat([df.drop(columns=["html_content"]), adversarial_features], axis=1)

# === Prepare X and y === #
X = df.drop(columns=["URL", "Domain", "Title", "label"], errors="ignore")
y = df["label"]

# Filter numeric features only
X = X.select_dtypes(include=["number"])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print("🧠 Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
print("📊 Evaluation Report:")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "best_model.pkl")
print("✅ Model saved as best_model.pkl")
