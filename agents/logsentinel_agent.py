import time
import hashlib

def hash_text(text):
    return int(hashlib.sha1(text.encode()).hexdigest(), 16) % (10**8)

def parse_log_line(line):
    parts = line.strip().split(": ", 1)
    if len(parts) != 2:
        return None
    raw_meta, message = parts
    try:
        timestamp, hostname, service_info = raw_meta.split(" ", 2)
        return {
            "timestamp": timestamp,
            "service": service_info.strip(),
            "message": message.strip()
        }
    except ValueError:
        return None

def extract_features(logs):
    features = []
    for log in logs:
        service_hash = hash_text(log["service"])
        message_len = len(log["message"])
        features.append([service_hash, message_len])
    return features

from sklearn.ensemble import IsolationForest

class LogAnomalyModel:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)

    def train(self, X):
        self.model.fit(X)

    def predict(self, X):
        return self.model.predict(X)

def run_agent():
    log_path = "logs/sample_syslog.log"
    with open(log_path, "r") as f:
        logs = [parse_log_line(line) for line in f if parse_log_line(line)]

    features = extract_features(logs)
    model = LogAnomalyModel()
    model.train(features)

    print("🔍 LogSentinel AI agent running...")

    with open(log_path, "r") as f:
        f.seek(0, 2)  # Go to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            parsed = parse_log_line(line)
            if not parsed:
                continue

            new_feat = extract_features([parsed])
            if model.predict(new_feat)[0] == -1:
                print("⚠️ [LogSentinel AI] Anomaly detected:", parsed)
