import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import shap

print("🚨 Training using structured_features.csv")

# Paths
data_path = Path("1_data/raw/mimiciii2/core/structured_features.csv")
model_out = Path("models/los_rf_model.pkl")
shap_out = Path("output/shap_values.pkl")
shap_csv = Path("output/shap_values.csv")

# Load data
df = pd.read_csv(data_path)

# Drop rows with missing values
df = df.dropna(subset=["los", "anchor_age", "gender", "num_labs", "num_diagnoses"])

# Binary gender
df["gender"] = df["gender"].map({"F": 0, "M": 1})

# Target: long stay
df["target"] = (df["los"] > 5).astype(int)

# Features
features = ["anchor_age", "num_labs", "num_diagnoses", "gender"]
X = df[features]
y = df["target"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# SHAP
explainer = shap.TreeExplainer(model)
# Use smaller test sample for SHAP
X_shap = X_test.sample(n=2000, random_state=42)
shap_vals = explainer.shap_values(X_shap)

# Save model & SHAP
model_out.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, model_out)
joblib.dump(shap_vals, shap_out)

# Save SHAP values (class 1 only)
shap_df = pd.DataFrame(shap_vals[1], columns=X_shap.columns)
shap_df["subject_id"] = X_shap.index.map(df["subject_id"].iloc.__getitem__).values
shap_df.to_csv(shap_csv, index=False)

print("✅ Model + SHAP values saved")