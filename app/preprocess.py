import fitz  # PyMuPDF
import re
import pytesseract
from PIL import Image
import io
import os


def extract_text_from_pdf(path: str) -> str:
    """
    Extraction PDF robuste via PyMuPDF.
    Fallback : OCR si pages scannées.
    """

    if not os.path.exists(path):
        return ""

    doc = fitz.open(path)
    text_full = ""

    for page in doc:
        text = page.get_text()

        # Si page vide → OCR fallback
        if len(text.strip()) < 5:
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(img)

        text_full += "\n" + text

    return clean_text(text_full)


def clean_text(text: str) -> str:
    """
    Normalisation :
    - enlève les espaces inutiles
    - remplace plusieurs \n par un seul
    - supprime caractères invisibles
    """
    text = text.replace("\r", "")
    text = re.sub(r"\n\s*\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def split_questions(text: str):
    """
    Découpe un texte en questions selon formats courants :
    - Q1, Q2, Q3
    - 1., 2., 3.
    - Question 1
    """

    pattern = r"(?:^|\n)(Q\d+|Question\s+\d+|\d+\.)\s"
    parts = re.split(pattern, text)

    questions = {}
    current = None

    for i in range(1, len(parts), 2):
        q_id = parts[i].strip().replace("Question", "Q").replace(".", "")
        q_body = parts[i+1].strip()

        questions[q_id] = q_body

    return questions


def prepare_exam_struct(questions_text, correction_text, student_text, bareme_default=20):
    """
    Combine les trois sources :
    - questions
    - corrections
    - réponses étudiant

    Retourne un dictionnaire structuré :
    {
        "Q1": {
            "question": "...",
            "answer": "...",
            "student_answer": "...",
            "bareme": 20
        }, ...
    }
    """

    q = split_questions(questions_text)
    c = split_questions(correction_text)
    s = split_questions(student_text)

    results = {}

    for key in q.keys():
        results[key] = {
            "question": q.get(key, ""),
            "answer": c.get(key, ""),
            "student_answer": s.get(key, ""),
            "bareme": bareme_default
        }

    return results
