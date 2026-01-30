from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def load_pdfs(data_dir):
    documents = []
    # Convert string path to Path object and look for PDFs
    for pdf_path in Path(data_dir).glob("*.pdf"):
        print(f"Loading: {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        # Add filename to metadata so we can cite sources later
        for page in pages:
            page.metadata["source"] = pdf_path.name
        documents.extend(pages)
    return documents