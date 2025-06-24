# scripts/create_patient_json.py
import json
from pathlib import Path

# Define a simplified FHIR-like patient record
patient_example = {
    "resourceType": "Bundle",
    "type": "collection",
    "entry": [
        {
            "resource": {
                "resourceType": "Patient",
                "id": "001",
                "name": [{"family": "Smith", "given": ["John"]}],
                "gender": "male",
                "birthDate": "1962-03-25"
            }
        },
        {
            "resource": {
                "resourceType": "Encounter",
                "id": "enc-001",
                "status": "finished",
                "class": {"code": "IMP"},
                "period": {"start": "2023-04-10T08:00:00Z", "end": "2023-04-15T14:00:00Z"}
            }
        },
        {
            "resource": {
                "resourceType": "Condition",
                "id": "cond-001",
                "code": {"coding": [{"system": "ICD-10", "code": "N18.5", "display": "Chronic kidney disease, stage 5"}]},
                "subject": {"reference": "Patient/001"},
                "clinicalStatus": {"coding": [{"code": "active"}]}
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "obs-001",
                "code": {"text": "Serum creatinine"},
                "valueQuantity": {"value": 6.4, "unit": "mg/dL"},
                "effectiveDateTime": "2023-04-09T10:00:00Z"
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "obs-002",
                "code": {"text": "Blood urea nitrogen"},
                "valueQuantity": {"value": 78, "unit": "mg/dL"},
                "effectiveDateTime": "2023-04-09T10:00:00Z"
            }
        },
        {
            "resource": {
                "resourceType": "MedicationStatement",
                "id": "med-001",
                "medicationCodeableConcept": {"text": "Furosemide"},
                "status": "active",
                "effectivePeriod": {"start": "2023-04-01T00:00:00Z"}
            }
        }
    ]
}

# ✅ Save to this location
output_path = Path("1_data/fhir/1_patient-example.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(patient_example, f, indent=2)

print(f"✅ Saved patient bundle to: {output_path.resolve()}")