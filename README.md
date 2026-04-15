# Real-Time-Phishing-Website-Detection-ML-Chrome-Extension
Real-Time Phishing Website Detection : ML + Chrome Extension

Built an end-to-end real-time phishing website detection system combining machine learning, adversarial robustness testing, and a deployed Chrome browser extension.

• Trained and benchmarked 5 classifiers (Random Forest, SVM, KNN, Naive Bayes, Decision Tree) on PhishTank + Tranco List datasets; Random Forest achieved 99% accuracy and F1-score with a false positive rate under 4.3%, outperforming traditional blacklist-based approaches.
• Engineered HTML-based features using BeautifulSoup extracting form fields, script tags, hidden elements, external link counts, SSL indicators, and domain attributes converting raw page content into numerical feature vectors for real-time classification.
• Deployed a Chrome browser extension with the trained Random Forest model embedded for live in-browser phishing detection, alerting users instantly with 3-option feedback UI (proceed, go back, report false positive) validated by an 87% user satisfaction rate.
• Built a public-facing Streamlit URL verification interface and a phishing simulation site for adversarial testing; implemented a continuous retraining pipeline fed by user-submitted false positives/negatives to improve model accuracy over time.
• Conducted multilingual phishing testing (Spanish, French, German) and adversarial robustness evaluation against URL obfuscation, domain spoofing, and JavaScript injection attacks.

Tech: Python · scikit-learn · Random Forest · SVM · BeautifulSoup · Streamlit · JavaScript · Chrome Extension API · PhishTank · Pandas · matplotlib
