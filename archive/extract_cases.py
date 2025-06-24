import pandas as pd
from pathlib import Path

print("🚀 Script started")

# --- Define Paths ---
base_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\raw\mimi\core")
output_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\processed\mimic")
output_path.mkdir(parents=True, exist_ok=True)

# --- Load CSVs ---
def load_csv(filename):
    path = base_path / filename
    print(f"📁 Loading {filename}")
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()  # normalize column names
    return df

patients = load_csv("patients.csv")
admissions = load_csv("admissions.csv")
icustays = load_csv("icustays.csv")
labevents = load_csv("labevents.csv")
inputevents = load_csv("inputevents.csv")
prescriptions = pd.read_csv(base_path / "prescriptions.csv", low_memory=False)
prescriptions.columns = prescriptions.columns.str.lower()
print("✅ prescriptions.csv loaded")

# --- Rename stay_id → icustay_id ---
icustays.rename(columns={"stay_id": "icustay_id"}, inplace=True)

# --- Merge Core Tables ---
print("🚀 Merging tables...")
merged = (
    icustays[["subject_id", "hadm_id", "icustay_id"]]
    .merge(admissions[["subject_id", "hadm_id", "admittime", "dischtime"]], on=["subject_id", "hadm_id"], how="inner")
    .merge(patients[["subject_id", "gender", "anchor_age", "anchor_year"]], on="subject_id", how="inner")
)
print("✅ Merged. Columns:", merged.columns.tolist())

# --- Identify Valid ICU Stays ---
valid_labs = labevents["hadm_id"].dropna().unique()
valid_inputs = inputevents["hadm_id"].dropna().unique()
valid_meds = prescriptions["hadm_id"].dropna().unique()

merged["has_lab"] = merged["hadm_id"].isin(valid_labs)
merged["has_input"] = merged["hadm_id"].isin(valid_inputs)
merged["has_meds"] = merged["hadm_id"].isin(valid_meds)

filtered = merged[
    merged["has_lab"] &
    (merged["has_input"] | merged["has_meds"])
]

# --- Error if No Matches ---
if filtered.empty:
    raise ValueError("❌ No ICU stays found with labs and either inputs or meds.")

# --- Sample Cases ---
sample_cases = filtered.dropna(subset=["icustay_id", "hadm_id", "subject_id"]).sample(3, random_state=42)
case_ids = sample_cases[["subject_id", "hadm_id", "icustay_id"]]
print("🧪 Sampled subject_ids:", case_ids["subject_id"].tolist())

# --- Filter Source Tables ---
pt_subset = patients[patients["subject_id"].isin(case_ids["subject_id"])]
adm_subset = admissions[admissions["hadm_id"].isin(case_ids["hadm_id"])]
icu_subset = icustays[icustays["icustay_id"].isin(case_ids["icustay_id"])]
lab_subset = labevents[labevents["hadm_id"].isin(case_ids["hadm_id"])]
input_subset = inputevents[inputevents["hadm_id"].isin(case_ids["hadm_id"])]
presc_subset = prescriptions[prescriptions["hadm_id"].isin(case_ids["hadm_id"])]

# --- Save Output ---
pt_subset.to_csv(output_path / "patients_sample.csv", index=False)
adm_subset.to_csv(output_path / "admissions_sample.csv", index=False)
icu_subset.to_csv(output_path / "icustays_sample.csv", index=False)
lab_subset.to_csv(output_path / "labevents_sample.csv", index=False)
input_subset.to_csv(output_path / "inputevents_sample.csv", index=False)
presc_subset.to_csv(output_path / "prescriptions_sample.csv", index=False)

print(f"✅ Extraction complete. Files saved to: {output_path}")

