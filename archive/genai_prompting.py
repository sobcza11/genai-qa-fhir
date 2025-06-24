import json
from pathlib import Path

# Directory setup
input_dir = Path("../1_data/processed/mimic/json")
output_dir = Path("../output/genai")
output_dir.mkdir(parents=True, exist_ok=True)

# Template for prompt
def build_prompt(patient):
    pid = patient["id"]
    gender = patient.get("gender", "unknown")
    birth = patient.get("birthDate", "unknown")

    prompt = f"""📘 Clinical QA Prompt for Patient {pid}

Patient Info:
- Gender: {gender}
- Birth Date: {birth}

This patient's ICU record contains structured data and SHAP-driven feature importance for a model predicting IV medication usage.

You are a clinical assistant. Please provide:
1. A summary of the patient's likely risk profile.
2. A narrative explanation of why the model may have flagged this patient.
3. Any ethical or fairness concerns based on feature usage (e.g. gender, age).
4. Suggested next steps for a clinician reviewing this case.

Respond concisely and in layman's terms where possible.
"""
    return prompt

# Process each JSON bundle
for file in input_dir.glob("case_*_bundle.json"):
    with open(file) as f:
        bundle = json.load(f)

    patient = next((e["resource"] for e in bundle["entry"] if e["resource"]["resourceType"] == "Patient"), None)
    if patient is None:
        print(f"⚠️ No patient info in {file.name}")
        continue

    prompt = build_prompt(patient)

    out_path = output_dir / f"{file.stem}_prompt.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(f"✅ Prompt saved: {out_path}")