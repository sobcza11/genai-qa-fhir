import json
import os
from pathlib import Path

# === Load SHAP Explanations ===
shap_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\7_exper explainability\4_shap-explainability-cds.json")

if not shap_path.exists():
    raise FileNotFoundError(f"Missing SHAP file at: {shap_path}")

with open(shap_path, "r") as f:
    shap_data = json.load(f)

# === Generate Simple Risk Tags ===
risk_tags = {}

for patient_id, explanation in shap_data.items():
    top_features = sorted(
        explanation.get("feature_importance", {}).items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:3]
    feature_phrases = [f"{feat} ({round(val, 2)})" for feat, val in top_features]
    reason = ", ".join(feature_phrases)
    risk_tags[patient_id] = f"High predicted LOS risk due to {reason}"

# === Save to Disk ===
output_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\7_exper explainability\risk_tags.json")
with open(output_path, "w") as f:
    json.dump(risk_tags, f, indent=2)

print(f"✅ Risk tags saved to: {output_path}")