import json
import os
from pathlib import Path
import pandas as pd
from tqdm import tqdm

# 📂 INPUT paths
FHIR_BUNDLE_DIR = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\fhir\real")
SHAP_VALUES_FILE = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\output\shap_values.csv")

# 📂 OUTPUT path
INJECTED_BUNDLE_DIR = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\fhir\real_injected")
INJECTED_BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

# 🧠 Load SHAP values
with open(SHAP_VALUES_FILE, "r") as f:
    shap_values_dict = json.load(f)

# 🔁 Iterate through FHIR bundles
for bundle_file in tqdm(list(FHIR_BUNDLE_DIR.glob("bundle_*.json")), desc="🔄 Injecting SHAP"):
    with open(bundle_file, "r") as f:
        bundle = json.load(f)

    # 🔑 Get patient_id from file name
    patient_id = bundle_file.stem.replace("bundle_", "")
    shap_entry = shap_values_dict.get(patient_id)

    if shap_entry:
        # 📎 Attach SHAP explanations under a new Bundle.entry
        explanation_entry = {
            "resource": {
                "resourceType": "Basic",
                "id": f"shap-{patient_id}",
                "code": {
                    "text": "SHAP explanation of structured features"
                },
                "extension": [
                    {"url": f"feature:{k}", "valueDecimal": v}
                    for k, v in shap_entry.items()
                ]
            }
        }
        bundle.setdefault("entry", []).append(explanation_entry)

    # 💾 Save updated bundle
    out_path = INJECTED_BUNDLE_DIR / bundle_file.name
    with open(out_path, "w") as f:
        json.dump(bundle, f, indent=2)

print(f"✅ Injected bundles saved to: {INJECTED_BUNDLE_DIR}")