from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME

def load_embedding_model():
    # Downloads model to local cache if not present
    return SentenceTransformer(EMBEDDING_MODEL_NAME)