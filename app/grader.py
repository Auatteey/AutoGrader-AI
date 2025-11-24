from sentence_transformers import SentenceTransformer, util

# Initialisation du modèle global pour réutilisation
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def grade_copy(student_text: str, exam_text: str, bareme_text: str):
    """
    Compare le texte de l'étudiant avec la correction et calcule une note.
    """
    # Création des embeddings
    student_emb = embed_model.encode(student_text, convert_to_tensor=True)
    correction_emb = embed_model.encode(exam_text, convert_to_tensor=True)

    # Similarité cosinus
    sim_score = util.cos_sim(student_emb, correction_emb).item()  # valeur entre 0 et 1

    # Calcul d'une note sur 20
    grade = round(sim_score * 20, 2)

    return {
        "grade": grade,
        "similarity_score": sim_score
    }
