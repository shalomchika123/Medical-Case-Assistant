import faiss
import numpy as np

class VectorStore:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.index = None
        self.documents = []

    def build(self, documents):
        if not documents:
            print("No documents to index!")
            return

        texts = [doc.page_content for doc in documents]
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)

        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        self.documents = documents

    def search(self, query, top_k):
        if not self.index:
            return []
            
        query_embedding = self.embedding_model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)

        # Return the actual document objects
        return [self.documents[i] for i in indices[0]]