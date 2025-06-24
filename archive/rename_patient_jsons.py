from pathlib import Path

# Target directory
json_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\processed\mimic\json")

# Rename logic
for file in json_path.glob("patient_*.json"):
    sid = file.stem.split("_")[1]
    new_name = json_path / f"case_{sid}_bundle.json"
    file.rename(new_name)
    print(f"✅ Renamed to: {new_name.name}")