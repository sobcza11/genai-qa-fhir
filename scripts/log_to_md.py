import json
from pathlib import Path

# File paths
log_path = Path("output/inference_logs/inference_log.json")
output_md = Path("inference_output.md")

# Load log
with open(log_path, "r") as f:
    log_entries = json.load(f)

# Sort entries by patient_id and timestamp (if needed)
log_entries.sort(key=lambda x: (x["patient_id"], x["timestamp"], x["question"]))

# Write to markdown
with open(output_md, "w", encoding="utf-8") as f:
    f.write("# 🧾 GenAI ICU Risk Summaries\n\n---\n\n")
    for entry in log_entries:
        f.write(
            f"> **Patient ID:** {entry['patient_id']}  \n"
            f"> **Question:** {entry['question']}  \n"
            f"> **Answer:** {entry['answer']}  \n"
            f"> **Model:** {entry['model']}  \n"
            f"> **Timestamp:** {entry['timestamp']}  \n\n"
        )

print("✅ Markdown file generated.")