import gradio as gr
import sys
import os
import traceback

# Ensure Python can find your folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingest.pdf_loader import load_pdfs
from ingest.text_cleaner import clean_text
from ingest.chunker import chunk_documents
from embeddings.embedder import load_embedding_model
from retrieval.vector_store import VectorStore
from retrieval.retriever import Retriever
from generation.generator import Generator
from config import DATA_DIR

# Global variables
system_retriever = None
system_generator = None

def start_system():
    """Initializes the system with error catching"""
    global system_retriever, system_generator
    
    try:
        yield "📂 Step 1/3: Loading PDFs..."
        docs = load_pdfs(DATA_DIR)
        docs = clean_text(docs)
        chunks = chunk_documents(docs)

        yield "🧠 Step 2/3: Building Search Index..."
        embedder = load_embedding_model()
        store = VectorStore(embedder)
        store.build(chunks)
        system_retriever = Retriever(store)

        yield "🤖 Step 3/3: Loading AI Model (Please wait, this uses CPU)..."
        # This is where it was crashing before
        system_generator = Generator()

        yield "✅ System Ready! Ask a question."
        
    except Exception as e:
        # If it crashes, print the error to the UI and Terminal
        error_msg = f"❌ Error detected: {str(e)}"
        print(f"\nCRITICAL ERROR:\n{traceback.format_exc()}")
        yield error_msg

def chat(message, history):
    """Safely handles the chat interaction"""
    if system_retriever is None:
        return "⚠️ System is still loading (or failed). Check the Status Box."
    
    if system_generator is None:
        return "⚠️ The AI Model failed to load. You can only search for documents, not generate answers."

    try:
        # 1. Retrieve Docs
        retrieved_docs = system_retriever.retrieve(message)
        
        # 2. Generate Answer
        answer = system_generator.generate(message, retrieved_docs)
        return answer
        
    except Exception as e:
        return f"❌ An error occurred during generation: {str(e)}"

# --- Build the UI ---
with gr.Blocks(title="Medical Case Assistant") as app:
    gr.Markdown("# 🏥 Medical Case Assistant")
    
    # Status box to show us exactly what is happening
    status_box = gr.Textbox(label="System Status", value="Initializing...", interactive=False)
    
    chatbot = gr.ChatInterface(
        fn=chat,
        chatbot=gr.Chatbot(height=400),
        textbox=gr.Textbox(placeholder="Ask about the patient case...", container=False, scale=7),
    )

    # Start the system automatically
    app.load(start_system, outputs=status_box)

if __name__ == "__main__":
    # share=True fixes the 'localhost' error you saw earlier
    app.launch(share=True)