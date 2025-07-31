# AI MCP Server – Multi-Agent Cybersecurity with CVE Intelligence and Email Alerts

This project demonstrates a **Multi-Agent Control Plane (MCP)** server that runs two cybersecurity agents:

1. **LogSentinel AI Agent** – Machine learning for log anomaly detection.
2. **MDR Watchdog Agent** – Rule-based detection for suspicious Linux activity.

Both agents are enriched with:
- **Real-time CVE lookups** using NVD and RedHat APIs
- **Email notifications with risk score, impact, and resolution guidance**

---

## Features

### Multi-Agent MCP
- Runs multiple agents concurrently

### LogSentinel AI Agent
- Learns normal log patterns
- Uses **Isolation Forest** for anomaly detection
- Sends an email when an anomaly occurs, with:
  - Risk score
  - Impact
  - Suggested resolution

### MDR Watchdog Agent
- Detects:
  - `sudo` misuse
  - New/unauthorized users
  - Unknown software installs/launch
- Sends an email for each alert with CVE info

### CVE Intelligence
- Real-time lookups using:
  - [NVD API](https://services.nvd.nist.gov/rest/json/cves/2.0)
  - [RedHat API](https://access.redhat.com/labs/securitydataapi)

### Email Alerts
- Uses `yagmail` to send email notifications
- Requires Gmail app password or SMTP credentials

---

## Architecture

```text
+---------------------------------------------------------+
|                   AI MCP Server                         |
+----------------------------+----------------------------+
                             |
             +---------------+----------------+
             |                                |
             v                                v
+----------------------------+    +----------------------------+
| LogSentinel AI Agent       |    | MDR Watchdog Agent         |
| (Unsupervised ML)          |    | (Rule-based detection)     |
+----------------------------+    +----------------------------+
             |                                |
             +---- Extract tokens ------------+
                             |
                             v
          +-----------------------------------------------+
          | CVE Lookup + Email Notification               |
          +-----------------------------------------------+

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-mcp-server.git
cd ai-mcp-server
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
pip install yagmail

```
### 3. Set Env variables for email notifications
```bash
export ALERT_EMAIL_USER="your_email@gmail.com"
export ALERT_EMAIL_PASSWORD="your_app_password"
export ALERT_EMAIL_TO="recipient_email@gmail.com"

```


---

## Running the MCP Server
```bash
python mcp.py
```

---

## Testing
Append a suspicious line to the log file:
```bash
echo "Jul 29 11:45:22 localhost sudo apt install nmap" >> logs/sample_syslog.log
```

### Expected console output:
```bash
🚨 [LogSentinel] Anomaly detected: Jul 29 12:22:00 localhost sudo apt install nmap
⚠️ [CVE Alert] nmap has known CVEs: CVE-2023-12345
📧 Email alert sent to recipient_email@gmail.com
⚠️ [MDR] SUDO usage detected: Jul 29 12:22:00 localhost sudo apt install nmap
⚠️ [CVE Alert] nmap has known CVEs: CVE-2023-12345
📧 Email alert sent to recipient_email@gmail.com
```
---

## Project Structure
```bash
ai-mcp-server/
├── agents/
│   ├── logsentinel_agent.py
│   ├── mdr_agent.py
│   └── cve_lookup.py
├── logs/
│   └── sample_syslog.log
├── notify.py
└── mcp.py

```
## Tags
#AI #Cybersecurity #MCP #CVE #ThreatIntelligence #Python #EmailAlerts
---
### Thank you for vising my project. Feedback welcome!


