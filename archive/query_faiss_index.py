from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.docstore.document import Document
from pathlib import Path

# For terminal query interaction
import argparse

# --- CONFIG ---
INDEX_DIR = Path("../models/faiss_index")
TOP_K = 3  # Number of results to return
MODEL_NAME = "all-MiniLM-L6-v2"  # Same model used during indexing

# --- Load FAISS Index ---
def load_faiss_index(index_path: Path, model_name: str):
    embeddings = SentenceTransformerEmbeddings(model_name=model_name)
    return FAISS.load_local(
    folder_path=str(index_path),
    embeddings=embeddings,
    allow_dangerous_deserialization=True  # ✅ You created this index yourself
)

# --- Format Output ---
def format_results(docs):
    print("\n🔍 Top Results:")
    for i, doc in enumerate(docs, 1):
        print(f"\nResult #{i}")
        print("-" * 40)
        print(doc.page_content.strip())
        if doc.metadata:
            print("\n📎 Metadata:", doc.metadata)

# --- Main ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True, help="Your clinical question")
    args = parser.parse_args()

    print("🔁 Loading FAISS index...")
    db = load_faiss_index(INDEX_DIR, MODEL_NAME)

    print(f"❓ Searching for: {args.query}")
    results = db.similarity_search(args.query, k=TOP_K)

    format_results(results)

    