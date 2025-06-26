import pandas as pd
import shap
import json
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier

# Load patient features
df = pd.read_json("output/cleaned_patient_conditions/cleaned_features.json", orient="records")

# TEMP FIX: Use first 3 rows only to match dummy labels
X = df.head(3)

# Create dummy target labels (must match 3 rows above)
y = pd.Series([1, 0, 1], name="target")

# Train model
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X, y)

# Run SHAP explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)[1]  # Class 1 SHAP values

# Format output by patient ID
shap_output = {}
for i, row in X.iterrows():
    patient_id = f"{i+1:03d}"  # 001, 002, etc.
    shap_dict = dict(zip(X.columns, shap_values[i]))
    shap_output[patient_id] = {"shap_values": shap_dict}

# Save results
output_path = Path("4_explainability/4_shap-explainability-cds.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w") as f:
    json.dump(shap_output, f, indent=2)

print("✅ Saved SHAP values to 4_explainability/4_shap-explainability-cds.json")