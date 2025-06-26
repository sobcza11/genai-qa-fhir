import json
from pathlib import Path
from datetime import datetime

log_path = Path("output/inference_logs/inference_log.json")

with open(log_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for entry in data:
    if "timestamp" not in entry:
        entry["timestamp"] = datetime.utcnow().isoformat()

with open(log_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✅ Missing timestamps patched.")