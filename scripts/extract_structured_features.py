import pandas as pd
from pathlib import Path

# ✅ Paths
base = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\raw\mimiciii2")
core = base / "core"
heavy = base / "heavy"
out_path = base / "core\structured_features.csv"

# ✅ Load data
patients = pd.read_csv(core / "patients.csv")
admissions = pd.read_csv(core / "admissions.csv")
icustays = pd.read_csv(core / "icustays.csv")
labevents = pd.read_csv(core / "labevents.csv")
diag = pd.read_csv(heavy / "diagnoses_icd.csv")
diag_dict = pd.read_csv(heavy / "d_icd_diagnoses.csv")

# ✅ Derive features

# Gender + Age
features = patients[["subject_id", "gender", "anchor_age"]].copy()
features["gender"] = features["gender"].map({"M": 1, "F": 0})

# LOS (Length of Stay)
los = icustays[["subject_id", "los"]].groupby("subject_id").mean().reset_index()
features = features.merge(los, on="subject_id", how="left")

# Number of Labs
num_labs = labevents.groupby("subject_id")["labevent_id"].count().reset_index()
num_labs.columns = ["subject_id", "num_labs"]
features = features.merge(num_labs, on="subject_id", how="left")

# Target: Sepsis or related ICD9 codes
sepsis_codes = {"99591", "99592", "78552", "0380", "0389", "03811", "03812", "03842"}  # Add more if desired
diag["ICD9_CODE"] = diag["ICD9_CODE"].astype(str).str.replace(".", "", regex=False)
diag["target"] = diag["ICD9_CODE"].apply(lambda x: 1 if x in sepsis_codes else 0)
target = diag.groupby("SUBJECT_ID")["target"].max().reset_index()
target.columns = ["subject_id", "target"]
features = features.merge(target, on="subject_id", how="left")

# ✅ Fill NaNs
features = features.fillna(0)

# ✅ Save
features.to_csv(out_path, index=False)
print(f"✅ Saved structured features to: {out_path}")