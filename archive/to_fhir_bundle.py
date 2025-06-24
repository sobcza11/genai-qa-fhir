import pandas as pd
import uuid
import json
from fhir.resources.bundle import Bundle
from fhir.resources.bundle import BundleEntry
from fhir.resources.patient import Patient
from fhir.resources.encounter import Encounter
from fhir.resources.period import Period
from fhir.resources.fhirtypes import DateTime

# Load the sampled CSV
df = pd.read_csv(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\fhir\real\sampled_patients.csv")

# Loop through each unique subject_id
for subject_id in df['subject_id'].unique():
    patient_rows = df[df['subject_id'] == subject_id]
    patient_row = patient_rows.iloc[0]  # Assume first row has patient info

    # Build Patient resource
    patient = Patient(
        id=str(subject_id),
        gender=patient_row["gender"].lower(),
        birthDate=patient_row["dob"][:10]  # YYYY-MM-DD
    )

    # Build Encounter entries
    encounter_entries = []
    for _, row in patient_rows.iterrows():
        encounter_id = str(row["icustay_id"])

        # Clean datetime format for Period
        start_time = pd.to_datetime(row["intime"]).isoformat()
        end_time = pd.to_datetime(row["outtime"]).isoformat()

        encounter = Encounter(
        id=encounter_id,
        status="finished",
        class_fhir={
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "code": "IMP",
            "display": "inpatient encounter"
        },
        subject={"reference": f"Patient/{subject_id}"},
        period=Period(start=start_time, end=end_time),
        type=[{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/encounter-type",
                "code": "ACUTE",
                "display": "Inpatient Acute"
            }]
        }]
    )

        encounter_entry = BundleEntry(
            resource=encounter,
            fullUrl=f"Encounter/{encounter_id}"
        )
        encounter_entries.append(encounter_entry)

    # Create bundle
    bundle = Bundle(
        id=str(uuid.uuid4()),
        type="collection",
        entry=[
            BundleEntry(
                resource=patient,
                fullUrl=f"Patient/{subject_id}"
            )
        ] + encounter_entries
    )

    # Save bundle to JSON
    output_path = fr"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\fhir\real\bundle_{subject_id}.json"
    with open(output_path, "w") as f:
        f.write(bundle.json(indent=2))

    print(f"✅ FHIR bundle saved: {output_path}")