from sentence_transformers import SentenceTransformer
import numpy as np

# Modèle gratuit Hugging Face
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed(text):
    return embed_model.encode(text, convert_to_numpy=True)

def build_vector_index(correction_text, bareme_text):
    docs = {
        "correction": correction_text,
        "bareme": bareme_text
    }
    index = {k: embed(v) for k, v in docs.items()}
    return docs, index

def similarity(vec1, vec2):
    # cosine similarity
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
