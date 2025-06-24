import json
import pandas as pd
from pathlib import Path

# === Paths ===
json_dir = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\processed\mimic\json")
shap_csv = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\output\shap_values.csv")
output_dir = json_dir.parent / "json_with_shap"
output_dir.mkdir(exist_ok=True)

# === Load SHAP values ===
shap_df = pd.read_csv(shap_csv)

# === Process Each FHIR Bundle ===
for file in json_dir.glob("case_*_bundle.json"):
    subject_id = int(file.stem.split("_")[1])
    shap_row = shap_df[shap_df["subject_id"] == subject_id]

    if shap_row.empty:
        print(f"⚠️ No SHAP values for subject_id {subject_id}")
        continue

    with open(file, "r") as f:
        bundle = json.load(f)

    # Inject SHAP explanation as Observation
    explanation = {
        "resource": {
            "resourceType": "Observation",
            "id": f"shap-{subject_id}",
            "status": "final",
            "code": {
                "text": "SHAP Explanation Scores"
            },
            "subject": {
                "reference": f"Patient/{subject_id}"
            },
            "component": [
                {
                    "code": {"text": col},
                    "valueQuantity": {"value": shap_row.iloc[0][col]}
                }
                for col in shap_row.columns if col != "subject_id"
            ]
        }
    }

    bundle["entry"].append(explanation)

    # Save updated bundle
    output_path = output_dir / file.name
    with open(output_path, "w") as f:
        json.dump(bundle, f, indent=2)

    print(f"✅ SHAP injected: {output_path.name}")