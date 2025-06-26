import json
from pathlib import Path

# Input paths
shap_path = Path("4_explainability/4_shap-explainability-cds.json")
patient_dir = Path("1_data/fhir/")
output_dir = Path("1_data/fhir_tagged/")
output_dir.mkdir(parents=True, exist_ok=True)

# Load SHAP results
with open(shap_path, "r") as f:
    shap_data = json.load(f)

# Loop through SHAP entries and update each patient
for patient_id, patient_shap in shap_data.items():
    # Get top 3 features by absolute SHAP value
    shap_values = patient_shap.get("shap_values", {})
    top_features = sorted(shap_values.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
    top_tags = [feat for feat, val in top_features]

    # Load patient JSON
    file_path = patient_dir / f"{patient_id}.json"
    if not file_path.exists():
        print(f"Missing: {file_path}")
        continue

    with open(file_path, "r") as f:
        patient_json = json.load(f)

    # Inject 'shap_tags'
    patient_json["shap_tags"] = top_tags

    # Write updated version
    with open(output_dir / f"{patient_id}.json", "w") as f:
        json.dump(patient_json, f, indent=2)

print("✅ SHAP tags injected into tagged patient files.")
