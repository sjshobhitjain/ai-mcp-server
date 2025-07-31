import time
from agents.cve_lookup import check_cves_for_tokens, extract_tokens_from_line
from notify import send_email_alert

def run_agent():
    print("🛡️ MDR Watchdog agent with CVE API checks starting...")
    log_path = "logs/sample_syslog.log"
    approved_apps = ["vim", "nano", "ls"]

    with open(log_path, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            line_lower = line.lower()
            flagged = False

            if "sudo" in line_lower:
                print("⚠️ [MDR] SUDO usage detected:", line.strip())
                flagged = True
            if "useradd" in line_lower or "adduser" in line_lower:
                print("⚠️ [MDR] New user creation:", line.strip())
                flagged = True
            if "install" in line_lower:
                if not any(app in line_lower for app in approved_apps):
                    print("⚠️ [MDR] Unknown software install:", line.strip())
                    flagged = True
            if any(app in line_lower for app in ["nmap", "wireshark", "tcpdump"]):
                print("⚠️ [MDR] Unapproved app launched:", line.strip())
                flagged = True

            if flagged:
    tokens = extract_tokens_from_line(line)
    cve_results = check_cves_for_tokens(tokens)

    # Risk scoring
    base_risk = 70
    if "sudo" in line_lower:
        base_risk = 80
    risk_score = base_risk + (10 * len(cve_results))
    impact = "Potential privilege abuse or unauthorized system modification."
    resolution = "Review sudo activity, validate users, and block unapproved software."

    send_email_alert(
        agent="MDR Watchdog",
        event=line.strip(),
        risk_score=risk_score,
        impact=impact,
        resolution_steps=resolution
    )

    if cve_results:
        for software, cves in cve_results.items():
            print(f"⚠️ [CVE Alert] {software} has known CVEs: {', '.join(cves)}")
