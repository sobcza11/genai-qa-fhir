import pandas as pd
import json
from pathlib import Path

print("🚀 Starting FHIR conversion...")

# Define input/output paths
input_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\processed\mimic")
output_path = input_path / "json"
output_path.mkdir(parents=True, exist_ok=True)

# Load sample data
patients = pd.read_csv(input_path / "patients_sample.csv")
admissions = pd.read_csv(input_path / "admissions_sample.csv")
icustays = pd.read_csv(input_path / "icustays_sample.csv")
labevents = pd.read_csv(input_path / "labevents_sample.csv")
inputevents = pd.read_csv(input_path / "inputevents_sample.csv")
prescriptions = pd.read_csv(input_path / "prescriptions_sample.csv")

# Normalize column names
for df in [patients, admissions, icustays, labevents, inputevents, prescriptions]:
    df.columns = df.columns.str.lower()

# Convert each patient to a FHIR bundle
for subject_id in patients["subject_id"].unique():
    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": []
    }

    # Get rows
    patient_row = patients[patients["subject_id"] == subject_id].iloc[0]
    adm_row = admissions[admissions["subject_id"] == subject_id].iloc[0]
    icu_row = icustays[icustays["subject_id"] == subject_id].iloc[0]

    # Add Patient resource
    bundle["entry"].append({
        "resource": {
            "resourceType": "Patient",
            "id": str(subject_id),
            "gender": patient_row["gender"].lower(),
            "birthDate": f"1900-{(100 - int(patient_row['anchor_age'])) % 12 + 1:02d}-01"
        }
    })

    # Add Hospital Admission Encounter
    bundle["entry"].append({
        "resource": {
            "resourceType": "Encounter",
            "id": f"adm-{adm_row['hadm_id']}",
            "status": "finished",
            "type": [{"text": "Hospital Admission"}],
            "subject": {"reference": f"Patient/{subject_id}"},
            "period": {
                "start": adm_row["admittime"],
                "end": adm_row["dischtime"]
            }
        }
    })

    # Add ICU Encounter
    bundle["entry"].append({
        "resource": {
            "resourceType": "Encounter",
            "id": f"icu-{icu_row['icustay_id']}",
            "status": "finished",
            "type": [{"text": "ICU Stay"}],
            "subject": {"reference": f"Patient/{subject_id}"},
            "period": {
                "start": icu_row["intime"],
                "end": icu_row["outtime"]
            }
        }
    })

    # Add Observations (labs)
    labs = labevents[labevents["hadm_id"] == adm_row["hadm_id"]]
    for _, row in labs.iterrows():
        bundle["entry"].append({
            "resource": {
                "resourceType": "Observation",
                "id": f"lab-{row.get('labevent_id', f'{row.name}')}",
                "subject": {"reference": f"Patient/{subject_id}"},
                "effectiveDateTime": row.get("charttime", ""),
                "valueQuantity": {"value": row.get("valuenum", None)},
                "code": {"text": f"Lab Item {row.get('itemid', '')}"}
            }
        })

    # Add IV Medications
    meds_iv = inputevents[inputevents["subject_id"] == subject_id]
    for _, row in meds_iv.iterrows():
        bundle["entry"].append({
            "resource": {
                "resourceType": "MedicationAdministration",
                "subject": {"reference": f"Patient/{subject_id}"},
                "effectiveDateTime": row.get("starttime", ""),
                "dosage": {
                    "text": f"{row.get('amount', '')} {row.get('amountuom', '')}",
                    "route": {"text": row.get("route", "unknown")}
                },
                "medicationCodeableConcept": {"text": f"IV Item {row.get('itemid', '')}"}
            }
        })

    # Add Prescriptions (PO)
    meds_po = prescriptions[prescriptions["subject_id"] == subject_id]
    for _, row in meds_po.iterrows():
        bundle["entry"].append({
            "resource": {
                "resourceType": "MedicationRequest",
                "subject": {"reference": f"Patient/{subject_id}"},
                "authoredOn": row.get("startdate", ""),
                "dosageInstruction": [{
                    "text": row.get("dosage", "see EHR")
                }],
                "medicationCodeableConcept": {"text": row.get("drug", "")}
            }
        })

    # Save JSON
    out_file = output_path / f"patient_{subject_id}.json"
    with open(out_file, "w") as f:
        json.dump(bundle, f, indent=2)

    print(f"✅ Wrote: {out_file}")
