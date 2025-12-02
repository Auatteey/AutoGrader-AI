from sentence_transformers import SentenceTransformer, util
import torch

# Chargement unique du modèle (singleton)
# Le modèle est chargé UNE SEULE FOIS au démarrage.
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model


def compute_similarity(a: str, b: str) -> float:
    """
    Calcule une similarité cosinus entre deux textes.
    Retourne un float entre 0 et 1.
    Gère les cas de chaînes vides.
    """

    if not a or not b or not a.strip() or not b.strip():
        return 0.0

    try:
        model = get_model()

        emb1 = model.encode(a, convert_to_tensor=True)
        emb2 = model.encode(b, convert_to_tensor=True)

        # util.cos_sim retourne un tensor 1x1 → on convertit proprement.
        sim = util.cos_sim(emb1, emb2).item()

        # Clamp entre 0 et 1
        sim = max(0.0, min(1.0, float(sim)))

        return sim

    except Exception:
        return 0.0
