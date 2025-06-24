# 🏥 MIMIC-CDS

### *An Ethical, Modular Clinical Decision Support Pipeline for ICU Patient Summarization*

<p align="center">
  <img src="synthetic/assets/tagline_pht.png" alt="MIMIC-CDS Logo" width="420"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/MIMIC--IV-v3.1-lightgrey" />
  <img src="https://img.shields.io/badge/FHIR-compliant-success" />
  <img src="https://img.shields.io/badge/Explainability-SHAP_%26_Permutation-blueviolet" />
  <img src="https://img.shields.io/badge/GenAI-HuggingFace_%26_ClinicalBERT-yellowgreen" />
  <img src="https://img.shields.io/badge/Python-3.10-blue" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" />
</p>

---

## 📌 Overview

**MIMIC-CDS** is a modular, end-to-end **Clinical Decision Support (CDS)** pipeline built on real ICU data from the MIMIC-IV database. It combines **explainable ML**, **FHIR compatibility**, and **GenAI-based clinical summarization** to simulate how modern, ethical, and transparent CDS systems can function in real-world hospital environments.

This system is designed to:
- ✅ Ingest & normalize patient data as FHIR Bundles
- 🔍 Predict risks using structured ML models (e.g., Random Forest)
- 🧠 Provide explainability via SHAP + Permutation Importance
- 🩺 Summarize patient status using ClinicalBERT QA
- 📜 Log all model inferences & expose results for audit

> Built with fairness, traceability, and modularity at its core.

---

## 📂 Core Pipeline Modules

| Stage | Module | Description |
|-------|--------|-------------|
| 1 | `src/etl_mimic.py` | Converts MIMIC-IV raw data into clean, structured FHIR-like JSON Bundles |
| 2 | `src/shap_model_iv.py` | Trains ML model (e.g. RF) and outputs SHAP-based feature attributions |
| 3 | `src/genai_infer.py` | Prompts a HuggingFace LLM over patient Bundles for clinical summarization |
| 4 | `scripts/enrich_bundles.py` | Injects SHAP explanations into JSON for downstream QA transparency |
| 5 | `output/inference_logs/` | Stores structured logs of GenAI outputs for analysis & verification |

---

## 🧠 Explainability by Design

- ✅ **SHAP**: Feature-wise importance on individual patients
- ✅ **Permutation Importance**: Robust, model-agnostic interpretability
- ✅ **Injection**: Model explanations are written *into* each patient bundle
- ✅ **FHIR Alignment**: Explanations embedded without breaking resource structure

---

## 🤖 GenAI Summarization

- 🧬 Uses `emilyalsentzer/Bio_ClinicalBERT` for embeddings
- 💬 Prompts `NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO` via Hugging Face Inference API
- 🛡️ Clinical reasoning prompts written for **precision + interpretability**

```text
"You are a clinical reasoning assistant. Given the patient bundle, summarize risks and reasoning."
