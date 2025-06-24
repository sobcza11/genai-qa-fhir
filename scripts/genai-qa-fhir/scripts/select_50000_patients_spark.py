
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pathlib import Path

print("🚀 Starting Spark job...")

# Initialize Spark
spark = SparkSession.builder.appName("Select50kPatients").getOrCreate()
print("✅ Spark session started")

# Input directories
base_path = "../1_data/raw/mimi"
core_path = f"{base_path}/core"
heavy_path = f"{base_path}/heavy"
output_dir = "../1_data/fhir/real"
Path(output_dir).mkdir(parents=True, exist_ok=True)

print("📦 Loading datasets...")

# Load core CSVs
patients = spark.read.csv(f"{core_path}/patients.csv", header=True, inferSchema=True)
admissions = spark.read.csv(f"{core_path}/admissions.csv", header=True, inferSchema=True).select("subject_id", "hadm_id", "admittime", "admission_type")
icustays = spark.read.csv(f"{core_path}/icustays.csv", header=True, inferSchema=True).select("subject_id", "hadm_id", "stay_id", "intime", "los")
diagnoses_all = spark.read.csv(f"{heavy_path}/diagnoses_icd.csv", header=True, inferSchema=True).select("subject_id", "hadm_id", "icd_code")

# Merge core tables
icu_adm = admissions.join(icustays, on=["subject_id", "hadm_id"], how="inner")
icu_adm_dx = icu_adm.join(diagnoses_all, on=["subject_id", "hadm_id"], how="inner")
merged = patients.join(icu_adm_dx, on="subject_id", how="inner")

# Deduplicate and sample 50k earliest
sampled = (merged
           .dropDuplicates(["subject_id"])
           .orderBy("admittime")
           .limit(50000))

# Filter diagnoses only for sampled patients
filtered_dx = diagnoses_all.join(
    sampled.select("subject_id", "hadm_id").dropDuplicates(),
    on=["subject_id", "hadm_id"],
    how="inner"
)

# Write outputs
sampled.toPandas().to_csv(f"{output_dir}/sampled_50000_patients.csv", index=False)
filtered_dx.toPandas().to_csv(f"{output_dir}/diagnoses_50000.csv", index=False)

print("✅ Saved 50,000 real patients and diagnoses subset to:", output_dir)
