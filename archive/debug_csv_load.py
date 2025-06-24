import pandas as pd
from pathlib import Path

# 📍 Location of CSV
csv_path = Path(__file__).resolve().parents[1] / "1_data" / "fhir" / "real" / "sampled_50000_patients.csv"

# 🔎 Attempt default read (comma-delimited)
df_default = pd.read_csv(csv_path)
print("🔍 Default read (comma-delimited):")
print("✅ Shape:", df_default.shape)
print("📌 Columns:", df_default.columns.tolist())
print(df_default.head(2))

# 🔎 Attempt tab-delimited read
df_tab = pd.read_csv(csv_path, sep="\t")
print("\n🔍 Tab-separated read:")
print("✅ Shape:", df_tab.shape)
print("📌 Columns:", df_tab.columns.tolist())
print(df_tab.head(2))
