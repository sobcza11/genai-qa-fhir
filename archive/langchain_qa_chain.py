from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.documents import Document

from pathlib import Path
import argparse
import os

# --- CONFIG ---
EMBED_MODEL = "all-MiniLM-L6-v2"
CHROMA_DIR = Path("../models/chroma_index/")
TOP_K = 3
HF_MODEL = "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# --- LLM Setup ---
llm = HuggingFaceEndpoint(
    repo_id=HF_MODEL,
    temperature=0.5,
    max_new_tokens=512,
    huggingfacehub_api_token=HF_TOKEN,
)

# --- Vector Store ---
def load_vectorstore():
    embeddings = SentenceTransformerEmbeddings(model_name=EMBED_MODEL)
    return Chroma(persist_directory=str(CHROMA_DIR), embedding_function=embeddings)

# --- LangChain QA Pipeline ---
def build_qa_chain():
    retriever = load_vectorstore().as_retriever(search_kwargs={"k": TOP_K})
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

# --- CLI Entry Point ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True, help="Ask a clinical question")
    args = parser.parse_args()

    qa = build_qa_chain()
    print(f"❓ Question: {args.query}")
    result = qa(args.query)

    print("\n🧠 Answer:\n", result["result"])
    print("\n📎 Sources:\n")
    for doc in result["source_documents"]:
        print(doc.page_content[:300], "...\n---")