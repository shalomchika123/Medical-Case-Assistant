# 🏥 Medical Case Assistant (Local RAG)

A private, secure, and modular AI assistant for querying medical patient records using **Mistral-7B** and **Retrieval Augmented Generation (RAG)**.

## 🚀 Features
- **Privacy First:** Runs locally or on private cloud instances; patient data never leaves the secure environment.
- **Modular Architecture:** Professional engineering structure separating Ingest, Retrieval, and Generation layers.
- **Explainable AI:** Uses RAG to ground answers in specific patient PDF documents.

## 🛠 Tech Stack
- **LLM:** Mistral-7B-Instruct-v0.2 (Quantized to 4-bit)
- **Vector Store:** FAISS
- **Orchestration:** LangChain
- **UI:** Gradio

## 📂 Project Structure
- `ingest/`: PDF parsing and text cleaning.
- `retrieval/`: Vector database and semantic search logic.
- `generation/`: LLM integration and prompt engineering.
- `app/`: Gradio frontend.

## ⚡ Quick Start (Google Colab)
Check out the `run_demo.ipynb` file in this repository to launch a free GPU instance of this app in one click!
