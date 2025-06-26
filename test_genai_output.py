import json
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# === Load Env ===
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# === Init HuggingFace Client ===
client = InferenceClient("NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO", token=HF_TOKEN)

# === Load Risk Tags ===
risk_tags_path = r"C:\Users\Rand Sobczak Jr\_rts\mlops\genai-qa-fhir\7_exper explainability\risk_tags.json"
if os.path.exists(risk_tags_path):
    with open(risk_tags_path, "r") as f:
        risk_tags = json.load(f)
else:
    risk_tags = {}
    print("⚠️ No risk_tags.json found — continuing without LOS risk tags.")

# === Example Patient Input ===
subject_id = "13084265"  # 👈 Use any key from your risk_tags.json file
clinical_note = "Patient presents with shortness of breath and elevated WBC count."

# === Inject Risk Tag if Available ===
risk_note = risk_tags.get(subject_id, "")
if risk_note:
    clinical_note = f"[RISK ALERT] {risk_note}\n\n{clinical_note}"

# === Run Chat Completion
response = client.chat_completion(
    messages=[
        {"role": "system", "content": "You are a medical assistant that summarizes key risks and diagnostic patterns from clinical notes."},
        {"role": "user", "content": clinical_note}
    ],
    max_tokens=300,
)

# === Output Results
print("\n📤 Prompt Sent:\n")
print(clinical_note)

print("\n🧠 GenAI Response:\n")
print(response.choices[0].message["content"])