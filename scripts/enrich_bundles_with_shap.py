import json
import pandas as pd
from pathlib import Path

print("💡 Enriching FHIR bundles with SHAP summaries...")

# Paths
bundle_dir = Path("1_data/fhir/real")
shap_summaries = pd.read_csv("output/shap_nlp_summaries.csv")
out_dir = Path("output/enriched_bundles")
out_dir.mkdir(parents=True, exist_ok=True)

# Convert to lookup dictionary
summary_lookup = dict(zip(shap_summaries.subject_id, shap_summaries.shap_summary))

# Loop over bundles
for bundle_path in bundle_dir.glob("*.json"):
    with open(bundle_path, "r", encoding="utf-8") as f:
        bundle = json.load(f)
    
    # Locate Patient resource
    patient_entry = next((entry for entry in bundle.get("entry", []) 
                          if entry.get("resource", {}).get("resourceType") == "Patient"), None)
    
    if not patient_entry:
        continue

    patient = patient_entry["resource"]
    
    try:
        subject_id = int(patient["id"])
    except (KeyError, ValueError, TypeError):
        print(f"⚠️ Skipping bundle {bundle_path.name} — invalid or missing subject ID")
        continue

    # Add SHAP summary if available
    summary = summary_lookup.get(subject_id)
    if summary:
        patient["shap_summary"] = summary

        # Save enriched bundle
        out_path = out_dir / bundle_path.name
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(bundle, f, indent=2)
        
        print(f"✅ Enriched: {bundle_path.name}")

print("🏁 All bundles processed.")