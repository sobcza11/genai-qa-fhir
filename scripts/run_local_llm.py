from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_id = "mistralai/Mistral-7B-Instruct-v0.2"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

prompt = "You are a medical assistant. What does it mean if a patient has low sodium and high creatinine?"

response = pipe(prompt, max_new_tokens=100, do_sample=True, temperature=0.7)
print(response[0]['generated_text'])