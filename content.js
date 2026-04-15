console.log("✅ Phishing Detector script active");

const suspicious_phrases = ["blocked", "malicious", "phishing", "restricted", "contact security"];
const multilingualKeywords = [
  "login", "iniciar sesión", "connexion", "anmelden", "ورود", "ログイン",
  "verify", "verificar", "vérifier", "überprüfen", "تحقق", "確認",
  "account", "cuenta", "compte", "konto", "الحساب", "アカウント",
  "secure", "seguro", "sécurisé", "sicher", "آمن", "安全",
  "update", "actualizar", "mettre à jour", "aktualisieren", "تحديث", "アップデート"
];

const currentUrl = window.location.href;
const pageText = document.body.innerText.toLowerCase();
const hasMultilingualKeyword = multilingualKeywords.some(word => pageText.includes(word)) ? 1 : 0;

// 🔐 Show Modal
function showPhishingWarningModal(allowOverride = false) {
  if (document.getElementById("phishing-warning-modal")) return;

  const modal = document.createElement("div");
  modal.id = "phishing-warning-modal";
  modal.innerHTML = `
    <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.6); z-index: 9999; display: flex; align-items: center; justify-content: center;">
      <div style="background: #1e293b; color: white; border-radius: 14px; padding: 30px; text-align: center; max-width: 400px; box-shadow: 0 8px 20px rgba(0,0,0,0.4);">
        <h2>🔒 <span style="color: #ffffff;">Phishing Detector</span></h2>
        <p style="color: #f8fafc;">Our system has detected potential phishing threats on this website.</p>
        <div style="margin: 15px 0; padding: 10px; background: #ef4444; color: white; border-radius: 8px; font-weight: bold;">
          ⚠️ Caution: Proceed with care!
        </div>

        <button id="proceedBtn" style="background: #3b82f6; color: white; padding: 10px 20px; border-radius: 6px; border: none; margin-right: 10px; cursor: pointer;">Proceed</button>
        <button id="goBackBtn" style="background: #ef4444; color: white; padding: 10px 20px; border-radius: 6px; border: none; cursor: pointer;">Go Back</button>

        ${allowOverride ? `
          <div style="margin-top: 15px;">
            <button id="reportSafeBtn" style="background: #10b981; color: white; padding: 8px 14px; border-radius: 6px; border: none; cursor: pointer; margin-top: 10px;">
              ✅ Report as Safe (False Positive)
            </button>
          </div>
        ` : ""}
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  document.getElementById("proceedBtn").onclick = () => modal.remove();
  document.getElementById("goBackBtn").onclick = () => history.back();

  if (allowOverride) {
    document.getElementById("reportSafeBtn").onclick = () => {
      chrome.storage.local.get({ reports: [] }, (data) => {
        const newReports = data.reports.filter(r => r.url !== currentUrl);
        newReports.push({ url: currentUrl, type: "false_positive" });
        chrome.storage.local.set({ reports: newReports }, () => {
          alert("✅ This site has been reported as SAFE. You will no longer see this warning.");
          modal.remove();
        });
      });
    };
  }
}

// 🚫 Suspicious Text Heuristics (e.g., blocked message)
function detectFirewallPattern() {
  const match = suspicious_phrases.some(phrase => pageText.includes(phrase));

  if (match) {
    chrome.storage.local.get({ reports: [] }, storage => {
      const override = storage.reports.find(r => r.url === currentUrl && r.type === "false_positive");
      if (!override) showPhishingWarningModal(true);
    });
  }
}

// 🧠 Run ML Detection + Apply User Overrides
function runPhishingPrediction() {
  chrome.storage.local.get({ reports: [] }, storage => {
    const overriddenPhishing = storage.reports.find(r => r.url === currentUrl && r.type === "false_negative");
    const overriddenSafe = storage.reports.find(r => r.url === currentUrl && r.type === "false_positive");

    if (overriddenPhishing) {
      console.log("🚨 User override: site reported as phishing");
      showPhishingWarningModal(true);
      return;
    }

    // ✅ Add multilingual feature to request
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ URL: currentUrl, has_multilingual_keywords: hasMultilingualKeyword })
    })
      .then(res => res.json())
      .then(data => {
        if (data.prediction === 1 && !overriddenSafe) {
          console.log("⚠️ ML model flagged this as phishing");
          showPhishingWarningModal(true);
        }
      })
      .catch(err => console.error("❌ Prediction error:", err));
  });
}

// 🔁 Run all detections
runPhishingPrediction();
detectFirewallPattern();
