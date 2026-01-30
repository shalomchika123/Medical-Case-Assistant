from config import TOP_K_RETRIEVAL

class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query):
        return self.vector_store.search(query, TOP_K_RETRIEVAL)