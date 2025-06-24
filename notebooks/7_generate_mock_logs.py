import json
from datetime import datetime, timedelta
from pathlib import Path
import random

# Output directory
output_dir = Path("../output/inference_logs")
output_dir.mkdir(parents=True, exist_ok=True)

# Sample pool
questions = [
    "What conditions required ICU care?",
    "What medications are relevant to the patient's renal function?",
    "Is the patient a candidate for dialysis?",
    "What lab findings are concerning?",
    "What diagnoses support the use of diuretics?"
]
answers = [
    "Patient shows signs of end-stage renal disease with poor response to meds.",
    "Furosemide prescribed for fluid overload in CKD.",
    "Creatinine and BUN suggest dialysis evaluation needed.",
    "Elevated labs warrant close monitoring.",
    "CKD Stage 5 supports aggressive intervention."
]
ground_truths = [
    "ICD-10 confirms CKD5, HTN. BUN and Cr elevated.",
    "Medication list includes furosemide. Labs confirm renal impairment.",
    "Dialysis consideration appropriate. Labs match nephrologist note.",
    "Confirmed high creatinine and uremia symptoms.",
    "Furosemide supported by BUN > 70."
]
shaps = [
    "Creatinine, BUN, BP",
    "BUN, age, meds",
    "SHAP: labs, meds",
    "Top: BUN, creatinine",
    "Diuretic usage, labs"
]
results = ["✔", "❌", "🔄"]
comments = [
    "Accurate based on labs.",
    "LLM missed med interaction.",
    "Partially valid, needs review."
]

# Generate 10 patients over time
base_time = datetime(2025, 5, 25)
for i in range(2, 12):
    log = {
        "timestamp": (base_time + timedelta(days=i * 3)).isoformat(),
        "patient_id": f"{i:03}",
        "question": random.choice(questions),
        "answer": random.choice(answers),
        "ground_truth": random.choice(ground_truths),
        "shap_summary": random.choice(shaps),
        "validation_result": random.choice(results),
        "comments": random.choice(comments)
    }

    log_file = output_dir / f"qa_eval_patient_{log['patient_id']}.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log) + "\n")

print("✅ Mock logs generated.")