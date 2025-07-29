# AI MCP Server – Multi-Agent Cybersecurity with CVE Intelligence

This project demonstrates a **Multi-Agent Control Plane (MCP)** server that runs two cybersecurity AI agents:

1. **LogSentinel AI Agent** – Machine learning for log anomaly detection.
2. **MDR Watchdog Agent** – Rule-based detection for suspicious Linux activity.

Both agents are **enriched with real-time CVE (Common Vulnerabilities and Exposures) lookups** using public APIs (NVD and RedHat).

---

## Features

### 1. Multi-Agent MCP Server
- Runs multiple security agents in parallel
- Simple Python orchestration

### 2. LogSentinel AI Agent
- Learns normal log behavior from `logs/sample_syslog.log`
- Uses **Isolation Forest** to detect anomalies
- **CVE Enrichment:** When an anomaly is detected, it looks up CVEs for any software mentioned in the log

### 3. MDR Watchdog Agent
- Detects suspicious activity:
  - `sudo` usage
  - Unauthorized user creation
  - Installation or execution of unapproved software
- **CVE Enrichment:** For each alert, looks up CVEs for any software mentioned

### 4. CVE Intelligence
- No local CVE databases
- Uses **real-time public APIs**:
  - [NVD API](https://services.nvd.nist.gov/rest/json/cves/2.0)
  - [RedHat Security Data API](https://access.redhat.com/labs/securitydataapi)
- Example output:

[CVE Alert] nmap has known CVEs: CVE-2023-12345, CVE-2021-9876

--

## Architecture
```bash
+-------------------------+
| MCP Server |
+-------------------------+
| |
| |
v v
+-----------------+ +------------------+
| LogSentinel AI | | MDR Watchdog |
| (Anomaly-based) | | (Rule-based) |
+-----------------+ +------------------+
| |
| |
v v

Real-time CVE lookups using NVD & RedHat APIs
```
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
```

## Running the MCP Server
python mcp.py


## Testing
Append a suspicious line to the log file:
```bash
echo "Jul 29 11:45:22 localhost sudo apt install nmap" >> logs/sample_syslog.log
```

### Expected console output:
🚨 [LogSentinel] Anomaly detected: Jul 29 11:45:22 localhost sudo apt install nmap
⚠️ [CVE Alert] nmap has known CVEs: CVE-2023-12345
⚠️ [MDR] SUDO usage detected: Jul 29 11:45:22 localhost sudo apt install nmap
⚠️ [CVE Alert] nmap has known CVEs: CVE-2023-12345


## Project Structure
ai-mcp-server/
├── agents/
│   ├── logsentinel_agent.py  # Anomaly detection agent
│   ├── mdr_agent.py          # Rule-based detection agent
│   └── cve_lookup.py         # Shared module for CVE API lookups
├── logs/
│   └── sample_syslog.log
└── mcp.py                    # Main script that runs both agents




