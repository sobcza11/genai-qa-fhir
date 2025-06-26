import json
from pathlib import Path

log_path = Path("output/inference_logs/inference_log.json")

with open(log_path, "r") as f:
    logs = json.load(f)

# Filter out entries with missing question or answer
cleaned_logs = [
    entry for entry in logs
    if entry.get("question") not in [None, "", "[Missing question]"]
    and entry.get("answer") not in [None, "", "[Missing answer]"]
]

removed = len(logs) - len(cleaned_logs)

# Overwrite the original log
with open(log_path, "w") as f:
    json.dump(cleaned_logs, f, indent=2)

print(f"🧹 Removed {removed} invalid entries. Remaining: {len(cleaned_logs)}")