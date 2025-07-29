# AI MCP Server – LogSentinel AI & MDR Watchdog with CVE Intelligence

This project demonstrates a **Multi-Agent Control Plane (MCP)** server that runs **two cybersecurity AI agents**:

1. **LogSentinel AI Agent** – Uses machine learning (Isolation Forest) to detect anomalies in Linux system logs.
2. **MDR Watchdog Agent** – Uses rule-based detection to identify suspicious activities (sudo abuse, unauthorized user creation, unapproved application installs/launch).

Both agents are now enhanced with **real-time CVE intelligence** using public security APIs.

---

## **Key Features**

### **1. Multi-Agent MCP Server**
- Both agents run simultaneously
- Designed as a **portfolio project for AI & cybersecurity**

### **2. LogSentinel AI Agent**
- Learns normal log patterns
- Flags anomalies in `/logs/sample_syslog.log`
- **NEW:** Enriches anomalies with **CVE lookups** via:
  - [NVD API](https://services.nvd.nist.gov/rest/json/cves/2.0)
  - [RedHat Security Data API](https://access.redhat.com/labs/securitydataapi)

### **3. MDR Watchdog Agent**
- Detects:
  - `sudo` usage
  - New/unauthorized user creation
  - Unknown or unapproved app installs/launch
- **NEW:** For each alert, performs **real-time CVE lookups** for related software

### **4. CVE Intelligence**
- No local CVE files are stored
- Queries public APIs at runtime
- Prints:
[CVE Alert] nmap has known CVEs: CVE-2023-12345, CVE-2021-9876

---

## **How It Works**

            ┌────────────────────────────────┐
            │           MCP Server           │
            └────────────────────────────────┘
                │                      │
 ┌──────────────┘                      └───────────────┐
 ▼                                                 ▼
┌─────────────┐ ┌─────────────────┐
│ LogSentinel │ -- anomaly detection --------> │ MDR Watchdog │
└─────────────┘ └─────────────────┘
│                     │
▼                     ▼
Real-time CVE lookup via NVD & RedHat APIs for enriched security alerts


---

## **Setup**

### **1. Clone the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/ai-mcp-server.git
cd ai-mcp-server
Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
Running the MCP Server
bash
Copy
Edit
python mcp.py
The MCP will launch:

LogSentinel AI Agent

MDR Watchdog Agent

Testing
Append a suspicious line to logs/sample_syslog.log:

bash
Copy
Edit
echo "Jul 29 11:45:22 localhost sudo apt install nmap" >> logs/sample_syslog.log
Expected output:

less
Copy
Edit
🚨 [LogSentinel] Anomaly detected: Jul 29 11:45:22 localhost sudo apt install nmap
⚠️ [CVE Alert] nmap has known CVEs: CVE-2023-12345
⚠️ [MDR] SUDO usage detected: Jul 29 11:45:22 localhost sudo apt install nmap
⚠️ [CVE Alert] nmap has known CVEs: CVE-2023-12345
Project Structure
graphql
Copy
Edit
ai-mcp-server/
├── agents/
│   ├── logsentinel_agent.py
│   ├── mdr_agent.py
│   └── cve_lookup.py   # Shared CVE API logic
├── logs/
│   └── sample_syslog.log
└── mcp.py              # Starts both agents

