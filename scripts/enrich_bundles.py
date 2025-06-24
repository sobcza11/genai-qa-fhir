import os
import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# Paths
root_dir = Path(__file__).resolve().parents[1]
fhir_real_dir = root_dir / "1_data" / "fhir" / "real"
fhir_enriched_dir = root_dir / "1_data" / "fhir" / "enriched"
mimic_core_dir = root_dir / "1_data" / "raw" / "mimiciii" / "core"

# Create output folder if it doesn't exist
fhir_enriched_dir.mkdir(parents=True, exist_ok=True)

# Load core MIMIC tables
diag = pd.read_csv(mimic_core_dir / "diagnoses_icd.csv")
labs = pd.read_csv(mimic_core_dir / "labevents.csv")
pres = pd.read_csv(mimic_core_dir / "prescriptions.csv")

# Minimal ICD-9 descriptions (manual)
ICD9_LOOKUP = {
    "25000": "Diabetes mellitus without complication",
    "4019": "Essential hypertension",
    "42731": "Atrial fibrillation",
    "486": "Pneumonia",
    "41401": "Coronary atherosclerosis",
    "2724": "Hyperlipidemia",
    "51881": "Acute respiratory failure",
    "4280": "Congestive heart failure",
    "99592": "Severe sepsis",
    "99591": "SIRS",
    "5845": "Acute kidney failure",
}

unmapped_codes = set()

# Process bundles
for bundle_path in tqdm(sorted(fhir_real_dir.glob("bundle_*.json")), desc="🔄 Enriching Bundles"):
    with open(bundle_path, "r") as f:
        bundle = json.load(f)

    patient_id = bundle["entry"][0]["resource"]["id"]
    hadm_ids = {
        ident.get("value")
        for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Encounter"
        for ident in e["resource"].get("identifier", [])
        if ident.get("system", "").endswith("admission")
    }

    def make_condition(row):
        code = str(row["icd9_code"])
        desc = ICD9_LOOKUP.get(code, f"Diagnosis {code}")
        if code not in ICD9_LOOKUP:
            unmapped_codes.add(code)
        return {
            "resource": {
                "resourceType": "Condition",
                "id": f"cond-{row['seq_num']}",
                "subject": {"reference": f"Patient/{patient_id}"},
                "code": {
                    "coding": [{
                        "system": "http://hl7.org/fhir/sid/icd-9-cm",
                        "code": code,
                        "display": desc
                    }]
                },
                "clinicalStatus": {"text": "active"}
            }
        }

    def make_observation(row):
        val_num = row.get("valuenum")
        val_str = row.get("value")
        charttime = row.get("charttime")
        unit = row.get("valueuom", "")
        obs_id = f"obs-{row['row_id']}"

        if pd.notna(val_num):
            return {
                "resource": {
                    "resourceType": "Observation",
                    "id": obs_id,
                    "subject": {"reference": f"Patient/{patient_id}"},
                    "code": {"text": f"Lab {row['itemid']}"},
                    "valueQuantity": {"value": float(val_num), "unit": unit},
                    "effectiveDateTime": charttime
                }
            }
        elif isinstance(val_str, str) and val_str.strip():
            return {
                "resource": {
                    "resourceType": "Observation",
                    "id": obs_id,
                    "subject": {"reference": f"Patient/{patient_id}"},
                    "code": {"text": f"Lab {row['itemid']}"},
                    "valueString": val_str.strip(),
                    "effectiveDateTime": charttime
                }
            }
        return None

    def make_medication(row):
        return {
            "resource": {
                "resourceType": "MedicationStatement",
                "id": f"med-{row['row_id']}",
                "subject": {"reference": f"Patient/{patient_id}"},
                "medicationCodeableConcept": {"text": row["drug"]},
                "effectivePeriod": {
                    "start": row.get("STARTDATE"),
                    "end": row.get("ENDDATE")
                }
            }
        }

    # Match patient rows
    pid = int(patient_id)
    diag_rows = diag[diag["subject_id"] == pid]
    lab_rows = labs[labs["subject_id"] == pid]
    pres_rows = pres[pres["subject_id"] == pid]

    if hadm_ids:
        hadm_ids_int = set(map(int, hadm_ids))
        lab_rows = lab_rows[lab_rows["hadm_id"].isin(hadm_ids_int)]
        pres_rows = pres_rows[pres_rows["hadm_id"].isin(hadm_ids_int)]

    # Convert to FHIR
    condition_entries = [make_condition(row) for _, row in diag_rows.iterrows()]
    observation_entries = [obs for _, row in lab_rows.iterrows() if (obs := make_observation(row))]
    medication_entries = [make_medication(row) for _, row in pres_rows.iterrows()]

    # Append to bundle
    bundle["entry"].extend(condition_entries + observation_entries + medication_entries)

    # Save enriched bundle
    out_path = fhir_enriched_dir / bundle_path.name
    with open(out_path, "w") as f:
        json.dump(bundle, f, indent=2)

# Print unmapped codes (optional)
if unmapped_codes:
    print("\n⚠️ Unmapped ICD-9 codes:")
    for code in sorted(unmapped_codes):
        print(f"- {code}")