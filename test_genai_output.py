from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient("NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO", token=HF_TOKEN)

response = client.chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What are the symptoms of pneumonia?"}
    ],
    max_tokens=100,
)

print(response.choices[0].message["content"])