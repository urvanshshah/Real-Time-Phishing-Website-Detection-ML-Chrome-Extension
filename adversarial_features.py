from bs4 import BeautifulSoup
import re
import pandas as pd

def detect_adversarial_patterns(html):
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(separator=" ", strip=True).lower()

    # 1. Hidden keyword detection
    has_hidden_keyword = any(
        "verify" in tag.text.lower() and "none" in (tag.get("style") or "")
        for tag in soup.find_all()
    )

    # 2. JS redirect detection
    has_javascript_redirect = bool(re.search(r'window\.location|window\.href', html.lower()))

    # 3. Mismatch: keywords without form/input
    keywords_present = re.search(r'login|account|secure|verify|update', text)
    has_inputs = bool(soup.find("input"))
    has_form_keyword_mismatch = bool(keywords_present and not has_inputs)

    # 4. Deceptive form names
    inputs = soup.find_all("input")
    deceptive_names = ["user", "pass", "email", "pwd"]
    has_deceptive_form_names = any(
        inp.get("name") in deceptive_names for inp in inputs if inp.get("name")
    )

    return {
        "has_hidden_keyword": int(has_hidden_keyword),
        "has_javascript_redirect": int(has_javascript_redirect),
        "has_form_keyword_mismatch": int(has_form_keyword_mismatch),
        "has_deceptive_form_names": int(has_deceptive_form_names),
    }

def add_adversarial_features(df):
    if "html_content" not in df.columns:
        print("⚠️ No html_content column found. Skipping adversarial feature extraction.")
        return df

    print("🛡️ Adding adversarial pattern features...")
    features = df["html_content"].fillna("").apply(detect_adversarial_patterns)
    return pd.concat([df, features.apply(pd.Series)], axis=1).drop(columns=["html_content"])