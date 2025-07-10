import time

def run_agent():
    print("🛡️ MDR Watchdog agent running...")
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

            if "sudo" in line_lower:
                print("⚠️ [MDR] SUDO usage detected:", line.strip())
            if "useradd" in line_lower or "adduser" in line_lower:
                print("⚠️ [MDR] New user creation:", line.strip())
            if "install" in line_lower:
                if not any(app in line_lower for app in approved_apps):
                    print("⚠️ [MDR] Unknown software install:", line.strip())
            if any(app in line_lower for app in ["nmap", "wireshark", "tcpdump"]):
                print("⚠️ [MDR] Unapproved app launched:", line.strip())
