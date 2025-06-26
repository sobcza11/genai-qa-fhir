import json
import os
from datetime import datetime
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from pathlib import Path
from tqdm import tqdm

# === Load Env ===
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient("NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO", token=HF_TOKEN)

# === Paths ===
input_dir = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\1_data\fhir")
risk_tag_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\7_exper explainability\risk_tags.json")
log_path = Path(r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\output\inference_logs\inference_log.json")
log_path.parent.mkdir(parents=True, exist_ok=True)

if not log_path.exists():
    with open(log_path, "w") as f:
        json.dump([], f)

# === Load Risk Tags ===
if risk_tag_path.exists():
    with open(risk_tag_path) as f:
        risk_tags = json.load(f)
else:
    risk_tags = {}
    print("\u26a0\ufe0f No risk_tags.json found.")

# === Extract Context ===
def extract_context(patient_json):
    lines = []
    for entry in patient_json.get("entry", []):
        resource = entry.get("resource", {})
        lines.append(json.dumps(resource, indent=2))
    return "\n".join(lines)

# === Clinical Questions ===
questions = [
    "What is this patient's primary condition and any comorbidities?",
    "What are the patient's top clinical risks?",
    "Are there any abnormal lab results or concerning trends?"
]

# === Process Each File ===
patient_files = list(input_dir.glob("*.json"))
print(f"\U0001f50d Found {len(patient_files)} patient files.")

for file in tqdm(patient_files, desc="Running GenAI QA"):
    with open(file) as f:
        data = json.load(f)

    subject_id = data.get("id") or file.stem
    context = extract_context(data)
    if not context:
        continue

    if subject_id in risk_tags:
        context = f"[RISK ALERT] {risk_tags[subject_id]}\n\n{context}"

    for question in questions:
        try:
            prompt = [
                {"role": "system", "content": "You are a medical assistant that summarizes key risks and diagnostic patterns from FHIR clinical data."},
                {"role": "user", "content": f"FHIR Data:\n{context}\n\nQuestion: {question}"}
            ]

            response = client.chat_completion(messages=prompt, max_tokens=512, temperature=0.3)
            result = {
                "patient_id": subject_id,
                "timestamp": datetime.utcnow().isoformat(),
                "question": question,
                "model_answer": response.choices[0].message["content"],
                "model_used": "Nous-Hermes-2-Mixtral-8x7B-DPO"
            }

            with open(log_path, "r+", encoding="utf-8") as f:
                log_data = json.load(f)
                log_data.append(result)
                f.seek(0)
                json.dump(log_data, f, indent=2)

        except Exception as e:
            print(f"\u274c Error with patient {subject_id}: {e}")
