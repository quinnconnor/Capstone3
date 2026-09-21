from functools import lru_cache
from sentence_transformers import SentenceTransformer
from .config import settings

@lru_cache(maxsize=1)
def model():
    return SentenceTransformer(settings.embedding_model)

def embed_texts(texts):
    return model().encode(texts,normalize_embeddings=True,convert_to_numpy=True,show_progress_bar=False).tolist()

def embed_query(text):
    return embed_texts([text])[0]
