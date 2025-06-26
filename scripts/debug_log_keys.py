import json
from pathlib import Path

log_path = Path("output/inference_logs/inference_log.json")

with open(log_path, "r") as f:
    log_entries = json.load(f)

for i, entry in enumerate(log_entries, 1):
    print(f"\nEntry {i}:")
    for key in entry:
        print(f" - {key}")