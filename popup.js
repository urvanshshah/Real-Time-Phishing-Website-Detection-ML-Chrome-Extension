function storeReport(type) {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const url = tabs[0].url;
      chrome.storage.local.get({ reports: [] }, function (data) {
        const reports = data.reports.filter(r => r.url !== url); // Remove duplicates
        reports.push({ url, type });
        chrome.storage.local.set({ reports }, function () {
          alert(`Reported as ${type === 'false_negative' ? 'phishing' : 'safe'}!`);
        });
      });
    });
  }
  
  document.getElementById("report-phishing").addEventListener("click", () => {
    storeReport("false_negative");
  });
  
  document.getElementById("report-safe").addEventListener("click", () => {
    storeReport("false_positive");
  });
  