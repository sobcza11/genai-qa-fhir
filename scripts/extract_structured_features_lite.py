import pandas as pd
from pathlib import Path

print("👋 SCRIPT STARTED")

# Set paths
core_path = Path("1_data/raw/mimiciii2/core")
heavy_path = Path("1_data/raw/mimiciii2/heavy")
output_path = core_path / "structured_features.csv"

# Load CSVs
print("📂 Loading patients.csv...")
patients = pd.read_csv(core_path / "patients.csv")
print(f"✅ patients.csv loaded: {patients.shape}")

print("📂 Loading icustays.csv...")
icustays = pd.read_csv(core_path / "icustays.csv")
print(f"✅ icustays.csv loaded: {icustays.shape}")

print("📂 Loading labevents.csv...")
labevents = pd.read_csv(core_path / "labevents.csv")
print(f"✅ labevents.csv loaded: {labevents.shape}")

print("📂 Loading diagnoses_icd.csv...")
diagnoses = pd.read_csv(heavy_path / "diagnoses_icd.csv")
diagnoses.columns = diagnoses.columns.str.lower()
print(f"✅ diagnoses_icd.csv loaded: {diagnoses.shape}")

# Minimal feature engineering
features = icustays[['subject_id', 'stay_id', 'intime', 'los']].copy()

# Add lab count
features['num_labs'] = (
    labevents.groupby('subject_id')
    .size()
    .reindex(features['subject_id'])
    .fillna(0)
    .astype(int)
    .values
)

# Add diagnosis count (if subject_id exists)
if 'subject_id' in diagnoses.columns:
    features['num_diagnoses'] = (
        diagnoses.groupby('subject_id')
        .size()
        .reindex(features['subject_id'])
        .fillna(0)
        .astype(int)
        .values
    )
else:
    print("⚠️ 'subject_id' not found in diagnoses_icd.csv — skipping diagnosis count.")
    features['num_diagnoses'] = 0

# Merge demographics
patients_sub = patients[['subject_id', 'gender', 'anchor_age']]
features = features.merge(patients_sub, on='subject_id', how='left')

# Clean up
features = features.drop_duplicates(subset='subject_id').dropna()

# Save
output_path.parent.mkdir(parents=True, exist_ok=True)
features.to_csv(output_path, index=False)
print(f"✅ Saved structured features to: {output_path}")