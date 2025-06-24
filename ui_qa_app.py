import streamlit as st
st.set_page_config(page_title="Inference Trace QA", layout="wide")  # ✅ MUST come immediately after import

from dotenv import load_dotenv
load_dotenv()

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import chromadb
from huggingface_hub import InferenceClient

import os

# --- CONFIG ---
CHROMA_DIR = "models/chroma_index/"
HF_MODEL = "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
TOP_K = 3

# --- DEBUG (Optional) ---
if not HF_TOKEN:
    st.error("❌ Hugging Face token not found. Check .env or set manually.")
else:
    st.info(f"🔐 Token starts with: {HF_TOKEN[:6]}...")

# --- Load Chroma Vector DB ---
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection(
    name="langchain",
    embedding_function=SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
)

# --- Hugging Face LLM ---
hf = InferenceClient(HF_MODEL, token=HF_TOKEN)

# --- Streamlit UI ---
st.set_page_config(page_title="Inference Trace QA", layout="wide")
st.title("🧠 Inference Trace: Clinical QA Assistant")
st.caption("Ask about ICU risk, ethics, or model behavior")

query = st.text_input("💬 Ask a question about ICU patients:")

if query:
    with st.spinner("Retrieving & thinking..."):
        try:
            # Step 1: Retrieve from Chroma
            results = collection.query(query_texts=[query], n_results=TOP_K)
            docs = results["documents"][0]

            # Step 2: Build prompt
            context = "\n\n".join(docs)
            prompt = f"""Answer the question below using only the context.

Context:
{context}

Question:
{query}
"""

            # Step 3: Generate with HF
            answer = hf.text_generation(prompt, max_new_tokens=512, temperature=0.5)

            # Display
            st.subheader("🧠 Answer")
            st.write(answer.strip())

            st.subheader("📎 Source Snippets")
            for i, doc in enumerate(docs, 1):
                st.markdown(f"**Result #{i}**")
                st.code(doc[:500] + "...", language="markdown")

        except Exception as e:
            st.error(f"❌ Hugging Face error: {e}")