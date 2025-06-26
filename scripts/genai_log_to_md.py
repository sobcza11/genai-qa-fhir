import json
from pathlib import Path

# 🔧 FILE LOCATIONS
LOG_PATH = Path("output/inference_logs/inference_log.json")
MD_PATH = Path("inference_output.md")

# 🧾 HEADER FOR MARKDOWN FILE
HEADER = """# 💾 GenAI ICU Risk Summaries

---
"""

# ✅ Load log
with open(LOG_PATH, "r", encoding="utf-8") as f:
    logs = json.load(f)

# ✍️ Open Markdown and overwrite with new content
with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(HEADER)
    for entry in logs:
        patient_id = entry.get("patient_id", "Unknown")
        timestamp = entry.get("timestamp", "")
        f.write(f"\n## 🧑‍⚕️ Patient ID: {patient_id}\n")
        f.write(f"**Timestamp:** `{timestamp}`\n\n")

        for q in entry.get("qa_pairs", []):
            question = q.get("question", "")
            answer = q.get("answer", "")
            f.write(f"**Q:** {question}\n\n")
            f.write(f"> {answer.strip()}\n\n")
        f.write("---\n")

print("✅ Markdown output saved to inference_output.md")
