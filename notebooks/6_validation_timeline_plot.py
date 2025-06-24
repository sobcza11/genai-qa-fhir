import json
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import glob

# Load all patient logs
log_dir = Path("output/inference_logs")
log_files = sorted(log_dir.glob("qa_eval_patient_*.jsonl"))

data = []
for log_file in log_files:
    with open(log_file, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"⚠️ Skipping invalid JSON in: {log_file.name}")

if not data:
    print("❌ No valid data found.")
    exit()

# Parse and sort by timestamp
for d in data:
    d["dt"] = datetime.fromisoformat(d["timestamp"])

data.sort(key=lambda x: x["dt"])

# Color mapping by validation result
color_map = {"✔": "green", "❌": "red", "🔄": "orange"}
x_vals = [d["dt"] for d in data]
y_vals = list(range(len(data)))
colors = [color_map.get(d["validation_result"], "gray") for d in data]
labels = [f"{d['patient_id']} – {d['validation_result']}" for d in data]

# Plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(x_vals, y_vals, c=colors, s=100, alpha=0.8)

# Format x-axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=45)

plt.title("🩺 QA Validation Timeline")
plt.xlabel("Date")
plt.ylabel("Validation #")
plt.grid(True)

# Optional annotations (top-left of each point)
for x, y, label in zip(x_vals, y_vals, labels):
    plt.annotate(label, (x, y), textcoords="offset points", xytext=(5, 5), ha="left", fontsize=8)

# Save + Show
plot_path = log_dir / "qa_validation_timeline.png"
plt.tight_layout()
plt.savefig(plot_path)
plt.show()

print(f"✅ Plot saved: {plot_path.as_posix()}")