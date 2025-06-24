from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StringType
from pathlib import Path
import pandas as pd

# ✅ Paths
root_path = Path(__file__).resolve().parents[1]
core_path = root_path / "1_data" / "raw" / "mimiciii" / "core"
heavy_path = root_path / "1_data" / "raw" / "mimiciii" / "heavy" / "diagnoses_icd"
out_path = root_path / "1_data" / "fhir" / "real"
out_path.mkdir(parents=True, exist_ok=True)

print("🚀 Starting Spark job...")
spark = SparkSession.builder \
    .appName("SelectMIMICIII") \
    .config("spark.driver.memory", "6g") \
    .getOrCreate()

print("✅ Spark session started")
print("📦 Loading datasets...")

# ✅ Load & select required columns
patients = spark.read.csv(str(core_path / "patients.csv"), header=True, inferSchema=True).select(
    "subject_id", "gender", "dob", "dod", "expire_flag"
)
admissions = spark.read.csv(str(core_path / "admissions.csv"), header=True, inferSchema=True)
icustays = spark.read.csv(str(core_path / "icustays.csv"), header=True, inferSchema=True)
diagnoses = spark.read.csv(str(heavy_path / "diagnoses_icd.csv"), header=True, inferSchema=True)

print("👉 All files loaded")
print("🔗 Merging...")

# Join tables
icu_adm = icustays.join(admissions, on=["subject_id", "hadm_id"], how="inner")
icu_adm_dx = icu_adm.join(diagnoses, on=["subject_id", "hadm_id"], how="inner")
merged = patients.join(icu_adm_dx, on="subject_id", how="inner")

# Filter non-null ICDs
merged = merged.filter(col("icd9_code").isNotNull())

# Sample (limit) result
sampled = merged.limit(50000)

print(f"🧮 Sampled row count: {sampled.count()}")
sampled.show(5)

# ✅ Drop duplicate row_id columns (if any)
sampled = sampled.drop("row_id")

# ✅ Cast all timestamp columns to StringType to avoid datetime errors
for colname, dtype in sampled.dtypes:
    if dtype == 'timestamp':
        sampled = sampled.withColumn(colname, col(colname).cast(StringType()))

# ✅ Export via Pandas
print("💾 Writing to CSV via Pandas...")
sampled_df = sampled.toPandas()
sampled_df.to_csv(out_path / "sampled_patients.csv", index=False)

print(f"✅ Done! CSV saved to: {out_path / 'sampled_patients.csv'}")