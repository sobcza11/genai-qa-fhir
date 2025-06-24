# src/logger.py
import json
from datetime import datetime
from pathlib import Path

output_dir = Path("output/inference_logs")
output_dir.mkdir(parents=True, exist_ok=True)

def log_qa_validation(patient_id, question, answer, ground_truth, shap_summary, validation_result, comments):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "patient_id": patient_id,
        "question": question,
        "answer": answer,
        "ground_truth": ground_truth,
        "shap_summary": shap_summary,
        "validation_result": validation_result,
        "comments": comments
    }

    log_file = output_dir / f"qa_eval_patient_{patient_id}.jsonl"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    return f"✅ Logged QA validation for patient {patient_id}"