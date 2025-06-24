import pandas as pd
from pathlib import Path

# Input file paths
base = Path("../1_data/raw/mimi/core")
patients_path = base / "patients.csv"
admissions_path = base / "admissions.csv"
icustays_path = base / "icustays.csv"

# Output path
output_path = Path("../1_data/fhir/real")
output_path.mkdir(parents=True, exist_ok=True)

# Load & sanitize data
patients = pd.read_csv(patients_path)
admissions = pd.read_csv(admissions_path)
icustays = pd.read_csv(icustays_path)

# Strip column names
patients.columns = patients.columns.str.strip()
admissions.columns = admissions.columns.str.strip()
icustays.columns = icustays.columns.str.strip()

# Merge core tables
df = (patients
      .merge(admissions, on="subject_id")
      .merge(icustays, on=["subject_id", "hadm_id"]))

# Drop duplicates and sort by admission time
df = df.sort_values("admittime").drop_duplicates("subject_id")

# Select 100 earliest patients
df = df.head(100)

# Save
df.to_csv(output_path / "sampled_100_patients.csv", index=False)

print("✅ Saved 100 real patients to:", output_path / "sampled_100_patients.csv")