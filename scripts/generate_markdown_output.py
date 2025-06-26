import json
from pathlib import Path

# === Load GenAI Log File ===
log_path = Path("output/inference_logs/inference_log.json")
output_md = Path("output/inference_logs/inference_output.md")

with open(log_path, "r") as f:
    logs = json.load(f)

print("🔍 First few entries from inference log:")
for e in logs[:3]:
    print(json.dumps(e, indent=2))  # Pretty print entries

# === Generate Markdown ===
lines = ["# 🧾 GenAI ICU Risk Summaries", "\n---\n"]
for i, entry in enumerate(logs):
    pid = entry.get("patient_id", f"unknown_{i}")
    question = entry.get("question", "[Missing question]")
    # ✅ Updated to handle both "model_answer" and "answer"
    answer = entry.get("model_answer") or entry.get("answer", "[Missing answer]")
    timestamp = entry.get("timestamp", "[Missing timestamp]")

    lines.append(f"## 🧍 Patient ID: `{pid}`\n")
    lines.append(f"### 🕒 {timestamp}\n")
    lines.append(f"**Q:** {question}\n\n**A:** {answer}\n\n---\n")

# === Save Markdown File ===
with open(output_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ Markdown summary saved to: {output_md.resolve()}")
