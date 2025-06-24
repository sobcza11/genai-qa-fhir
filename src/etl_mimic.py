import os
import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# ✅ Input folders
core_dir = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\raw\mimiciii2\core")
hvy_dir = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\raw\mimiciii2\heavy")
sample_file = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\fhir\real\sampled_patients_filtered.csv")

# ✅ Output folder
output_dir = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\fhir\real")
output_dir.mkdir(parents=True, exist_ok=True)

# ✅ Load CSVs with lowercase columns
patients = pd.read_csv(core_dir / "patients.csv", dtype=str)
patients.columns = patients.columns.str.lower()

admissions = pd.read_csv(core_dir / "admissions.csv", dtype=str)
admissions.columns = admissions.columns.str.lower()

diagnoses = pd.read_csv(hvy_dir / "diagnoses_icd.csv", dtype=str)
diagnoses.columns = diagnoses.columns.str.lower()

sampled = pd.read_csv(sample_file, dtype=str)
sampled.columns = sampled.columns.str.lower()

# ✅ Only use subjects from the sampled set
subject_ids = sampled["subject_id"].unique().tolist()
missing_ids = [sid for sid in subject_ids if sid not in set(patients["subject_id"])]
print(f"❗ {len(missing_ids)} subject_id(s) are missing from patients.csv")

# ✅ Generate FHIR Bundles
for subject_id in tqdm(subject_ids, desc="Generating Bundles"):
    match = patients[patients["subject_id"] == subject_id]
    if match.empty:
        print(f"⚠️ Skipping subject_id={subject_id} (not found in patients.csv)")
        continue
    patient_row = match.iloc[0]

    # Patient resource
    patient = {
        "resourceType": "Patient",
        "id": f"case_{subject_id}",
        "identifier": [{"system": "http://mimic.mit.edu/subject_id", "value": subject_id}],
        "gender": patient_row.get("gender", "").lower(),
        "birthDate": patient_row.get("dob", "")
    }

    # Encounter(s)
    patient_adms = admissions[admissions["subject_id"] == subject_id]
    adm_entries = []
    for _, adm in patient_adms.iterrows():
        adm_resource = {
            "resourceType": "Encounter",
            "id": f"encounter-{adm['hadm_id']}",
            "status": "finished",
            "subject": {"reference": f"Patient/case_{subject_id}"},
            "period": {
                "start": adm.get("admittime", ""),
                "end": adm.get("dischtime", "")
            },
            "reasonCode": [{
                "text": adm.get("hospital_expire_flag", "0")
            }]
        }
        adm_entries.append({"resource": adm_resource})

    # Diagnosis Condition(s)
    patient_dx = diagnoses[diagnoses["subject_id"] == subject_id]
    dx_entries = []
    for _, dx in patient_dx.iterrows():
        dx_resource = {
            "resourceType": "Condition",
            "id": f"condition-{dx['hadm_id']}-{dx['seq_num']}",
            "subject": {"reference": f"Patient/case_{subject_id}"},
            "code": {
                "coding": [{
                    "system": "http://hl7.org/fhir/sid/icd-9-cm",
                    "code": dx["icd9_code"]
                }]
            }
        }
        dx_entries.append({"resource": dx_resource})

    # Bundle output
    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [{"resource": patient}] + adm_entries + dx_entries
    }

    out_path = output_dir / f"case_{subject_id}_bundle.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2)

print("✅ All bundles generated.")
