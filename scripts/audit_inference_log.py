import json
from pathlib import Path

log_path = Path("output/inference_logs/inference_log.json")

with open(log_path, "r") as f:
    logs = json.load(f)

issues = []
for i, entry in enumerate(logs):
    if entry.get("question") in [None, "", "[Missing question]"] or entry.get("answer") in [None, "", "[Missing answer]"]:
        issues.append((i, entry.get("patient_id", "unknown")))

print(f"🔎 Found {len(issues)} problematic entries:")
for idx, pid in issues:
    print(f" - Entry #{idx} | Patient ID: {pid}")