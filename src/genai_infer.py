import os
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from tqdm import tqdm
from datetime import datetime
from pathlib import Path

# === Step 1: Setup ===
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
    token=HF_TOKEN
)

input_dir = r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\fhir_bundles"
output_dir = r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\output\genai_augmented"
log_path = r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\output\inference_logs\inference_log.json"

os.makedirs(output_dir, exist_ok=True)
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# === Step 2: Define questions ===
questions = [
    "What is this patient's primary condition and any complications?",
    "Are there any urgent risks or red flags in the patient’s chart?",
    "What are possible treatment or care options relevant to this patient?"
]

log_entries = []

# === Step 3: Iterate through files ===
files = list(Path(input_dir).glob("*.json"))
print(f"🔍 Running GenAI QA on {len(files)} FHIR bundles...")

for file in tqdm(files, desc="Running GenAI QA"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            fhir_data = json.load(f)

        context = json.dumps(fhir_data, indent=2)
        patient_id = file.stem
        all_answers = []

        for question in questions:
            prompt = f"Context:\n{context}\n\nQuestion: {question}"

            response_text = client.text_generation(
                prompt=prompt,
                max_new_tokens=400,
                temperature=0.3
            ).strip()

            all_answers.append({
                "question": question,
                "answer": response_text
            })

        # === Step 4: Inject into FHIR bundle ===
        fhir_data["genai_summary"] = all_answers

        with open(os.path.join(output_dir, file.name), "w", encoding="utf-8") as outf:
            json.dump(fhir_data, outf, indent=2)

        # === Step 5: Logging ===
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "patient_id": patient_id,
            "model": "Nous-Hermes-2-Mixtral-8x7B-DPO",
            "questions": questions,
            "answers": all_answers,
            "status": "success"
        }
        log_entries.append(log_entry)

    except Exception as e:
        log_entries.append({
            "timestamp": datetime.utcnow().isoformat(),
            "patient_id": file.stem,
            "model": "Nous-Hermes-2-Mixtral-8x7B-DPO",
            "error": str(e),
            "status": "error"
        })

# === Write log ===
with open(log_path, "w", encoding="utf-8") as logf:
    json.dump(log_entries, logf, indent=2)

print("✅ GenAI inference and logging complete.")