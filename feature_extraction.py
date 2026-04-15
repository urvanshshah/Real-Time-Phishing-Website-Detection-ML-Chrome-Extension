import pandas as pd
import re
from urllib.parse import urlparse
from difflib import SequenceMatcher
import tldextract

# === Adversarial Feature Functions === #

def has_obfuscated_chars(url):
    """Detects % encodings, @ signs, hex codes in the URL."""
    return int(bool(re.search(r"%[0-9A-Fa-f]{2}|@|0x[0-9A-Fa-f]+", url)))

def is_lookalike_domain(domain):
    known_brands = ["paypal", "google", "facebook", "amazon", "apple", "microsoft", "netflix", "instagram"]
    main = domain.split('.')[0]
    for brand in known_brands:
        similarity = SequenceMatcher(None, main, brand).ratio()
        if 0.8 < similarity < 1.0:
            return 1
    return 0

def is_punycode_domain(domain):
    try:
        encoded = domain.encode("idna").decode("ascii")
        return int('xn--' in encoded)
    except Exception:
        return 0

# === Multilingual Keyword Detection === #

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

# === Main Feature Extractor for PhiUSIIL CSV === #

def add_adversarial_features(df, url_column="URL", html_column="html_content"):
    print("🔍 Adding adversarial robustness features...")

    df = df.copy()
    df["has_obfuscated_chars"] = df[url_column].apply(has_obfuscated_chars)
    df["is_lookalike_domain"] = df["Domain"].apply(is_lookalike_domain)
    df["is_punycode_domain"] = df["Domain"].apply(is_punycode_domain)

    # 🌍 Multilingual phishing keyword detection from HTML/text
    if html_column in df.columns:
        print("🌐 Adding multilingual phishing keyword detection...")
        df["has_multilingual_keywords"] = df[html_column].fillna("").apply(has_multilingual_keywords)
    else:
        df["has_multilingual_keywords"] = 0  # fallback if html_content not present

    return df
