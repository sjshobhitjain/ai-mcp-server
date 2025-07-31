from notify import send_email_alert

import time
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import CountVectorizer
from agents.cve_lookup import check_cves_for_tokens, extract_tokens_from_line

def run_agent():
    print("🔍 LogSentinel AI agent with CVE API checks starting...")
    log_path = "logs/sample_syslog.log"

    # Train baseline anomaly model
    with open(log_path, "r") as f:
        baseline_logs = f.readlines()

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(baseline_logs)
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)

    # Monitor logs
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
    tokens = extract_tokens_from_line(line)
    cve_results = check_cves_for_tokens(tokens)

    # Risk scoring
    base_risk = 60
    risk_score = base_risk + (10 * len(cve_results))
    impact = "Potential system misbehavior or compromise."
    resolution = "Investigate the log entry and patch software if CVEs exist."

    # Send email
    send_email_alert(
        agent="LogSentinel AI",
        event=line.strip(),
        risk_score=risk_score,
        impact=impact,
        resolution_steps=resolution
    )

    if cve_results:
        for software, cves in cve_results.items():
            print(f"⚠️ [CVE Alert] {software} has known CVEs: {', '.join(cves)}")
