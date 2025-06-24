import pandas as pd
from pathlib import Path

def load_icd9_map(base_path):
    """
    Loads ICD9 to long_title mapping from d_icd_diagnoses.csv
    """
    path = Path(base_path) / "heavy" / "d_icd_diagnoses.csv"
    df = pd.read_csv(path, dtype={"icd_code": str})
    return df[["icd_code", "long_title"]].drop_duplicates()

def decode_icd9(df, icd9_map):
    """
    Merges diagnosis DataFrame with ICD9 descriptions
    """
    df["ICD9_CODE"] = df["ICD9_CODE"].astype(str)
    icd9_map = icd9_map.rename(columns={"icd_code": "ICD9_CODE"})
    return df.merge(icd9_map, on="ICD9_CODE", how="left")
