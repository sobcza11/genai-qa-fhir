import pandas as pd
from pathlib import Path

# ✅ Step 1: Set the input & output paths
patients_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\raw\mimiciii2\core\patients.csv")
output_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\fhir\real\sampled_patients_filtered.csv")

# ✅ Step 2: Load the patients file
patients = pd.read_csv(patients_path, dtype=str)

# ✅ Step 3: Randomly sample 100 valid subject_ids
sampled = patients.sample(n=100, random_state=42)

# ✅ Step 4: Save the sample to disk
sampled.to_csv(output_path, index=False)

print(f"✅ Sampled {len(sampled)} patients saved to:\n{output_path}")