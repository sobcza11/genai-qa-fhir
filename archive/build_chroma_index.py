from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.docstore.document import Document
from pathlib import Path
import os

EMBED_MODEL = "all-MiniLM-L6-v2"
DATA_DIR = Path("../output/genai/")
CHROMA_DIR = Path("../models/chroma_index/")

def load_docs():
    docs = []
    for f in DATA_DIR.glob("*_bundle_prompt.txt"):
        answer_file = f.with_name(f.name.replace("_prompt.txt", "_answer.txt"))
        if not answer_file.exists():
            continue
        with open(f, "r") as pf, open(answer_file, "r") as af:
            prompt = pf.read().strip()
            answer = af.read().strip()
        full_text = f"Prompt:\n{prompt}\n\nAnswer:\n{answer}"
        docs.append(Document(page_content=full_text))
    return docs

if __name__ == "__main__":
    embeddings = SentenceTransformerEmbeddings(model_name=EMBED_MODEL)
    documents = load_docs()
    print(f"📄 Loaded {len(documents)} prompt-answer pairs.")
    if CHROMA_DIR.exists():
        for f in os.listdir(CHROMA_DIR):
            os.remove(CHROMA_DIR / f)
    Chroma.from_documents(documents, embedding=embeddings, persist_directory=str(CHROMA_DIR))
    print("✅ Chroma index saved.")