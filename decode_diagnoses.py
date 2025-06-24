import sys
from pathlib import Path
import pandas as pd
import time

# Add src/ to import path
sys.path.append(str(Path(__file__).resolve().parent / "src"))
from icd9_decode import load_icd9_map, decode_icd9

# Set base path
base_path = Path("1_data/raw/mimiciii2")
diagnoses_path = base_path / "heavy" / "diagnoses_icd.csv"

start = time.time()

print("📂 Reading diagnoses...")
diagnoses_df = pd.read_csv(diagnoses_path)
print(f"✅ Loaded diagnoses_icd.csv — shape: {diagnoses_df.shape} [{time.time() - start:.2f}s]")

print("📂 Reading ICD9 map...")
icd9_map = load_icd9_map(base_path)
print(f"✅ Loaded d_icd_diagnoses.csv — shape: {icd9_map.shape} [{time.time() - start:.2f}s]")

print("🔁 Decoding diagnoses...")
decoded_df = decode_icd9(diagnoses_df, icd9_map)
print(f"✅ Decoded — shape: {decoded_df.shape} [{time.time() - start:.2f}s]")

print("💾 Writing to CSV...")
Path("output").mkdir(exist_ok=True)
decoded_df.to_csv("output/decoded_diagnoses.csv", index=False)
print(f"✅ Saved to output/decoded_diagnoses.csv [{time.time() - start:.2f}s]")

print(f"⏱️ Total time: {time.time() - start:.2f}s")