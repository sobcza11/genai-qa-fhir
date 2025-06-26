import json
from pathlib import Path

# === Paths ===
patient_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\fhir\1_patient-example.json")
ruleset_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\2_embeddings\2_cds-ruleset-sheep.json")
output_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\output\cds_matches\cds_results.json")

# === Load Data ===
with patient_path.open("r", encoding="utf-8") as f:
    patient = json.load(f)

with ruleset_path.open("r", encoding="utf-8") as f:
    rules = json.load(f)

# === Extract Patient Features ===
icd_codes = {entry["code"] for entry in patient.get("conditions", [])}
med_names = {entry["name"].lower() for entry in patient.get("medications", [])}

# === Check Rule Matches ===
matched_rules = []

for rule in rules:
    condition = rule.get("condition", {})
    code_match = condition.get("icd_code") in icd_codes
    med_match = all(med not in medications for med in condition.get("medications_exclude", []))

    if code_match and med_match:
        matched.append({
            "rule_id": rule["id"],
            "description": rule["description"],
            "recommendation": rule["recommendation"]
        })
    med_match = any(med.lower() in med_names for med in rule.get("medications", []))

    if condition_match or med_match:
        matched_rules.append({
            "rule_name": rule["name"],
            "matched_conditions": list(set(rule.get("conditions", [])) & icd_codes),
            "matched_medications": list(set([m.lower() for m in rule.get("medications", [])]) & med_names),
            "note": rule.get("note", "")
        })

# === Save Output ===
output_path.parent.mkdir(parents=True, exist_ok=True)
with output_path.open("w", encoding="utf-8") as f:
    json.dump(matched_rules, f, indent=2)

print(f"[✓] {len(matched_rules)} CDS rules matched. Results saved to {output_path}")