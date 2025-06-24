import json
from pathlib import Path
from collections import Counter

INPUT_DIR = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\fhir\real")
resource_counter = Counter()

for file in sorted(INPUT_DIR.glob("*.json")):
    try:
        bundle = json.loads(file.read_text())
        for entry in bundle.get("entry", []):
            resource = entry.get("resource", {})
            r_type = resource.get("resourceType", "Unknown")
            resource_counter[r_type] += 1
    except Exception as e:
        print(f"⚠️ Skipped {file.name}: {e}")

print("\n📦 Resource Type Counts:")
for r_type, count in resource_counter.items():
    print(f"- {r_type}: {count}")