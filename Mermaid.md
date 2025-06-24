```mermaid
flowchart TD
    A[MIMIC-IV ICU Patient Data] --> B[FHIR-Compatible JSON Bundles]
    B --> C[Structured Feature Extraction]
    C --> D[Random Forest Classifier]
    D --> E[Prediction Label]
    D --> F[SHAP Explanations]
    E --> G[Enhanced FHIR Bundles]
    F --> G
    G --> H[LangChain RAG Pipeline]
    H --> H1[ClinicalBERT Embeddings]
    H --> H2[FAISS Vector Store]
    H --> H3[HuggingFace LLM (Nous-Hermes 2 Mixtral)]
    I[Clinician Question] --> H
    H --> J[GenAI Answer + SHAP Overlay]
```