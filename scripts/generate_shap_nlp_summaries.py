import pandas as pd
from pathlib import Path

print("🧠 Generating SHAP NLP summaries...")

# Paths
shap_path = Path("output/shap_values.csv")
summary_out = Path("output/shap_nlp_summaries.csv")

# Load SHAP values
shap_df = pd.read_csv(shap_path)
feature_cols = [col for col in shap_df.columns if col != "subject_id"]

# Define readable feature names
readable_names = {
    "anchor_age": "age",
    "gender": "gender",
    "num_diagnoses": "number of diagnoses",
    "num_labs": "number of lab tests",
}

# Generate summary rows
summaries = []

for _, row in shap_df.iterrows():
    subject_id = int(row["subject_id"])
    shap_vals = row[feature_cols]

    # Sort top features by absolute importance
    top_feats = shap_vals.abs().sort_values(ascending=False).head(2).index.tolist()
    readable = [readable_names.get(f, f.replace("_", " ")) for f in top_feats]

    # Format sentence
    summary = f"Patient {subject_id}'s long ICU stay risk is primarily influenced by {readable[0]} and {readable[1]}."
    
    summaries.append({
        "subject_id": subject_id,
        "shap_summary": summary
    })

# Save to CSV
summary_df = pd.DataFrame(summaries)
summary_out.parent.mkdir(parents=True, exist_ok=True)
summary_df.to_csv(summary_out, index=False)

print(f"✅ Saved NLP summaries to: {summary_out}")