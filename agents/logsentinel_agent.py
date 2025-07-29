import time
import re
import requests
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import CountVectorizer

# === API query functions ===
def query_nvd_api(software):
    """Query NVD for CVEs related to the given software name."""
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={software}&resultsPerPage=2"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            vulnerabilities = data.get("vulnerabilities", [])
            if vulnerabilities:
                ids = [v["cve"]["id"] for v in vulnerabilities]
                return ids
    except Exception as e:
        print(f"❌ NVD API failed for {software}: {e}")
    return []

def query_redhat_api(software):
    """Query RedHat Security API for CVEs related to the given software name."""
    url = f"https://access.redhat.com/labs/securitydataapi/cve.json?package={software}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                ids = [item.get("CVE") for item in data if "CVE" in item]
                return ids
    except Exception as e:
        print(f"❌ RedHat API failed for {software}: {e}")
    return []

def check_cves_for_tokens(tokens):
    """
    Given a list of tokens from a log line, query CVE APIs for each token.
    Returns a dict: {token: [cve_ids]}
    """
    cve_hits = {}
    for t in tokens:
        # Only check simple alphanumeric tokens (software names)
        if len(t) < 3 or not t.isalnum():
            continue
        # Query both APIs
        nvd_cves = query_nvd_api(t)
        redhat_cves = query_redhat_api(t)
        all_cves = list(set(nvd_cves + redhat_cves))
        if all_cves:
            cve_hits[t] = all_cves
    return cve_hits

def run_agent():
    print("🔍 LogSentinel AI agent with real-time CVE API checks starting...")
    log_path = "logs/sample_syslog.log"

    # === Train initial anomaly detection model ===
    with open(log_path, "r") as f:
        baseline_logs = f.readlines()

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(baseline_logs)
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)

    # === Monitor logs in real-time ===
    with open(log_path, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            X_new = vectorizer.transform([line])
            pred = model.predict(X_new)[0]

            if pred == -1:  # anomaly detected
                print("🚨 [LogSentinel] Anomaly detected:", line.strip())

                # Extract tokens (words) from the line
                tokens = re.findall(r"[a-zA-Z0-9]+", line.lower())

                # Check CVEs live using APIs
                cve_results = check_cves_for_tokens(tokens)
                if cve_results:
                    for software, cves in cve_results.items():
                        print(f"⚠️ [CVE Alert] {software} has known CVEs: {', '.join(cves)
