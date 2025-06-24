import pandas as pd
import json
from pathlib import Path
from tqdm import tqdm

# 📁 Paths
base_dir = Path(__file__).resolve().parents[1]
csv_path = base_dir / "1_data" / "fhir" / "real" / "sampled_50000_patients.csv"
output_dir = base_dir / "1_data" / "fhir" / "real_fhir_json"
output_dir.mkdir(parents=True, exist_ok=True)

print("📦 Loading sampled_50000_patients.csv...")
df = pd.read_csv(csv_path)

print("🔁 Grouping by subject_id...")
grouped = df.groupby("subject_id")

print("📝 Writing FHIR Bundles...")
for subject_id, group in tqdm(grouped, total=len(grouped)):
    row = group.iloc[0]

    # 🧍 Patient resource
    patient = {
        "resourceType": "Patient",
        "id": f"patient-{subject_id}",
        "identifier": [{"system": "https://mimic.mit.edu/subject_id", "value": str(subject_id)}],
        "gender": row["gender"].lower(),
        "extension": [
            {"url": "http://hl7.org/fhir/StructureDefinition/anchor-age", "valueInteger": int(row["anchor_age"])},
            {"url": "http://hl7.org/fhir/StructureDefinition/anchor-year", "valueInteger": int(row["anchor_year"])},
            {"url": "http://hl7.org/fhir/StructureDefinition/anchor-year-group", "valueString": row["anchor_year_group"]},
        ]
    }

    # 💊 Condition resources (1 per ICD code row)
    conditions = []
    for _, r in group.iterrows():
        conditions.append({
            "resourceType": "Condition",
            "id": f"condition-{subject_id}-{r['icd_code']}",
            "subject": {"reference": f"Patient/patient-{subject_id}"},
            "code": {
                "coding": [{
                    "system": "http://hl7.org/fhir/sid/icd-9",
                    "code": r["icd_code"]
                }]
            },
            "encounter": {"identifier": {"value": str(r["hadm_id"])}}
        })

    # 📦 FHIR bundle
    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [{"resource": patient}] + [{"resource": c} for c in conditions]
    }

    # 💾 Save JSON
    out_path = output_dir / f"{subject_id}.json"
    with open(out_path, "w") as f:
        json.dump(bundle, f, indent=2)

print(f"✅ Export complete: {len(grouped)} FHIR bundles written to {output_dir}")