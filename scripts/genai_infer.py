import json
import hashlib
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from tqdm import tqdm

# 🔐 Load API token from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"

# 📂 Paths
input_dir = Path("1_data/fhir/")
output_dir = Path("output/inference_logs/")
output_dir.mkdir(parents=True, exist_ok=True)

log_file = output_dir / "inference_log.json"
if not log_file.exists():
    with open(log_file, "w") as f:
        json.dump([], f)

# ⚙️ Client
client = InferenceClient(model=MODEL_NAME, token=HF_TOKEN)

# ❓ Questions
questions = [
    "What are the patient's top clinical risks?",
    "Summarize the patient’s recent ICU history.",
    "Are there any abnormal lab results or concerning trends?"
]

# 🔧 Utilities
def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

def extract_context(patient_json):
    context_parts = []
    for entry in patient_json.get("entry", []):
        resource = entry.get("resource", {})
        if "text" in resource:
            context_parts.append(resource["text"].get("div", ""))
        elif "note" in resource:
            for note in resource["note"]:
                context_parts.append(note.get("text", ""))
    return "\n".join(context_parts).strip()

# 🚀 Main Loop
patient_files = list(input_dir.glob("*.json"))
print(f"🔍 Running GenAI QA on {len(patient_files)} FHIR bundles...")

for file in tqdm(patient_files, desc="Running GenAI QA"):
    try:
        with open(file) as f:
            patient_data = json.load(f)

        patient_id = patient_data.get("id", file.stem)
        context = extract_context(patient_data)
        if not context:
            continue

        context_hash = hash_text(context)
        timestamp = datetime.utcnow().isoformat()

        for question in questions:
            prompt = f"Context:\n{context}\n\nQuestion: {question}"
            answer = client.text_generation(prompt, max_new_tokens=400, temperature=0.3)

            log_entry = {
                "patient_id": patient_id,
                "timestamp": timestamp,
                "question": question,
                "model_answer": answer,
                "model_used": MODEL_NAME,
                "input_context_hash": context_hash
            }

            with open(log_file, "r+") as f:
                data = json.load(f)
                data.append(log_entry)
                f.seek(0)
                json.dump(data, f, indent=2)

    except Exception as e:
        print(f"❌ Error with {file.name}: {e}")