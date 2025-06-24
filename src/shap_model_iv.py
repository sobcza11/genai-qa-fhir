import pandas as pd
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from pathlib import Path
import os

# Paths
input_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\raw\mimiciii2\core\structured_features.csv")
output_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\output\shap_values.csv")

# Load structured features
df = pd.read_csv(input_path)

# ✅ Prepare X and y
features = ['gender', 'anchor_age', 'los', 'num_labs']  # use only existing columns
df = df.fillna(0)
X = df[features]
y = df["target"]

# ✅ Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"✅ Final columns in X_test: {X_test.columns.tolist()}")

# ✅ Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# ✅ SHAP explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# ✅ Debug: Shape check
print(f"✅ SHAP shape: {shap_values[1].shape} vs X_test shape: {X_test.shape}")

# ✅ Save SHAP values for class 1
shap_df = pd.DataFrame(shap_values[1], columns=X_test.columns)
shap_df["subject_id"] = df.iloc[X_test.index]["subject_id"].values
shap_df.to_csv(output_path, index=False)
print(f"✅ SHAP values for class 1 saved to: {output_path}")