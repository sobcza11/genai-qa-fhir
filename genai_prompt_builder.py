import json
from pathlib import Path

# === File Paths ===
patient_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\fhir\real\1_patient-example.json")
cds_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\output\cds_matches\cds_results.json")
prompt_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\output\prompts\prompt_for_llm.json")

# === Load Files ===
with patient_path.open("r", encoding="utf-8") as f:
    patient = json.load(f)

with cds_path.open("r", encoding="utf-8") as f:
    matches = json.load(f)

# === Build Prompt ===
prompt = {
    "system_instruction": (
        "You are a clinical decision support assistant. Summarize the following patient data and explain any clinical rule matches "
        "in plain English. Include helpful context and possible recommendations if appropriate."
    ),
    "patient_summary": {
        "gender": patient.get("gender", "unknown"),
        "age": patient.get("age", "unknown"),
        "conditions": [entry.get("description", "") for entry in patient.get("conditions", [])],
        "medications": [entry.get("name", "") for entry in patient.get("medications", [])],
    },
    "matched_rules": matches
}

# === Save Prompt ===
prompt_path.parent.mkdir(parents=True, exist_ok=True)
with prompt_path.open("w", encoding="utf-8") as f:
    json.dump(prompt, f, indent=2)

print(f"[✓] Prompt saved to {prompt_path}")