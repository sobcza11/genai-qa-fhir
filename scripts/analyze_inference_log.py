import json
from pathlib import Path
from collections import Counter
from rich import print

# Load log file
log_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\output\inference_logs\inference_log.json")
with open(log_path, "r") as f:
    log = json.load(f)

results = []

# Basic Stats
total = len(log)
no_answer = sum(1 for entry in log if entry["answer"].strip() in ["", "[No answer]"])
short_answers = [entry for entry in log if len(entry["answer"].split()) < 8]

# Print Summary
print(f"\n[bold cyan]📊 GenAI QA Inference Log Summary[/bold cyan]")
print(f"Total patients evaluated: {total}")
print(f"Empty or '[No answer]' entries: {no_answer}")
print(f"Answers < 8 words: {len(short_answers)}")

# Optional: Show top 5 short or blank answers
print("\n[bold yellow]🕵️ Examples of potential QA issues:[/bold yellow]")
for entry in short_answers[:5]:
    print(f"• [Patient {entry['patient_id']}] Answer: {entry['answer']}")

# Optional: Keyword frequency (top 10)
keywords = Counter()
for entry in log:
    for word in entry["answer"].lower().split():
        if word.isalpha() and len(word) > 4:
            keywords[word] += 1

print("\n[bold green]🧠 Top keywords in answers:[/bold green]")
for word, count in keywords.most_common(10):
    print(f"  - {word}: {count}")

