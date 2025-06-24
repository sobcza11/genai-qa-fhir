from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pathlib import Path
import argparse

INDEX_DIR = Path("../models/chroma_index/")
TOP_K = 3
MODEL_NAME = "all-MiniLM-L6-v2"

def load_index(index_path: Path, model_name: str):
    embeddings = SentenceTransformerEmbeddings(model_name=model_name)
    return Chroma(persist_directory=str(index_path), embedding_function=embeddings)

def format_results(docs):
    print("\n🔍 Top Results:")
    for i, doc in enumerate(docs, 1):
        print(f"\nResult #{i}")
        print("-" * 40)
        print(doc.page_content.strip())
        if doc.metadata:
            print("\n📎 Metadata:", doc.metadata)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True, help="Your clinical question")
    args = parser.parse_args()

    print("🔁 Loading Chroma index...")
    db = load_index(INDEX_DIR, MODEL_NAME)
    print(f"❓ Searching for: {args.query}")
    results = db.similarity_search(args.query, k=TOP_K)
    format_results(results)