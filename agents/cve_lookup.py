import requests
import re

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
        if len(t) < 3 or not t.isalnum():
            continue
        nvd_cves = query_nvd_api(t)
        redhat_cves = query_redhat_api(t)
        all_cves = list(set(nvd_cves + redhat_cves))
        if all_cves:
            cve_hits[t] = all_cves
    return cve_hits

def extract_tokens_from_line(line):
    return re.findall(r"[a-zA-Z0-9]+", line.lower())
  
