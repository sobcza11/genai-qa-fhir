import pandas as pd
import shap
import joblib
from pathlib import Path

# Define paths
model_path = Path("../models/random_forest.pkl")
features_path = Path("../output/X_test.csv")  # Adjust if needed
output_csv = Path("../output/shap_values.csv")

# Load model and test features
model = joblib.load(model_path)
X_test = pd.read_csv(features_path)

# Initialize SHAP explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Save SHAP values for class 1 (positive class)
shap_df = pd.DataFrame(shap_values[1], columns=X_test.columns)
shap_df["subject_id"] = X_test.index  # Add subject_id if index matches

# Save to CSV
output_csv.parent.mkdir(parents=True, exist_ok=True)
shap_df.to_csv(output_csv, index=False)

print(f"✅ SHAP values saved to: {output_csv}")