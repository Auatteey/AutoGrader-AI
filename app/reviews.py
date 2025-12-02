import os
import json
import uuid
import re
from datetime import datetime
from fastapi import HTTPException

# --- UTILITAIRES DE SÉCURITÉ ---

def sanitize_text(text: str) -> str:
    """
    Empêche XSS et injections. Nettoie le texte utilisateur.
    """
    if not text:
        return ""
    
    # empêche les attaques CSV injection (= @ + -)
    if text.startswith(("=", "+", "-", "@")):
        text = "'" + text

    # enlève les balises HTML dangereuses
    text = re.sub(r"<.*?>", "", text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # limite la taille du message
    return text[:2000]


def sanitize_id(value: str) -> str:
    """
    Autorise seulement lettres, chiffres, _.
    """
    if not re.match(r"^[a-zA-Z0-9_]+$", value):
        raise HTTPException(400, f"Invalid identifier: {value}")
    return value


def validate_problem_type(problem: str) -> str:
    """
    Liste blanche des catégories de problèmes.
    """
    allowed = ["wrong_grade", "wrong_file", "missing_pages", "ask_review", "other"]
    if problem not in allowed:
        raise HTTPException(400, "Invalid problem type.")
    return problem


# --- CORE FUNCTIONS ---

def get_review_file(exam_id: str):
    exam_id = sanitize_id(exam_id)

    folder = f"data/reviews/{exam_id}"
    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/reviews.json"
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

    return path


def submit_review(exam_id: str, student: str, problem_type: str, message: str):
    """
    Ajoute une nouvelle review étudiante.
    """

    exam_id = sanitize_id(exam_id)
    student = sanitize_id(student)
    problem_type = validate_problem_type(problem_type)
    message = sanitize_text(message)

    review = {
        "id": str(uuid.uuid4()),
        "exam_id": exam_id,
        "student": student,
        "problem_type": problem_type,
        "message": message,
        "status": "open",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    path = get_review_file(exam_id)

    # Charger et ajouter
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.append(review)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return review


def list_reviews(exam_id: str):
    """
    Retourne toutes les reviews d’un examen.
    """
    path = get_review_file(exam_id)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_review(exam_id: str, review_id: str):
    """
    Marque une review comme résolue.
    """

    exam_id = sanitize_id(exam_id)
    review_id = sanitize_id(review_id.replace("-", ""))[:32]  # simplification sécurisée

    path = get_review_file(exam_id)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    found = False
    for review in data:
        if review["id"].replace("-", "") == review_id:
            review["status"] = "resolved"
            found = True

    if not found:
        raise HTTPException(404, "Review not found")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return {"status": "success", "review_id": review_id}
