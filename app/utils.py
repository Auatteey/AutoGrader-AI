import os
import uuid
from fastapi import HTTPException, UploadFile

# Acceptable MIME types
ALLOWED_MIME = ["application/pdf"]

# Taille max : 20 MB
MAX_FILE_SIZE = 20 * 1024 * 1024


def secure_filename(name: str) -> str:
    """
    Nettoie un nom de fichier (pas d'espaces, accents, caractères non-sécurisés)
    """
    import re
    name = name.lower()
    name = re.sub(r'[^a-z0-9._-]', '_', name)
    return name


def validate_pdf(file: UploadFile):
    """
    Vérifie que le fichier est un vrai PDF.
    """
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(400, f"Invalid file type: {file.content_type}. PDF only.")

    # Vérification de taille
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large (max 20MB).")


def save_pdf_secure(file: UploadFile, output_path: str) -> str:
    """
    Sauvegarde un PDF de manière sécurisée sans casser les répertoires.
    output_path = chemin COMPLET SANS EXTENSION (ex: uploads/exams/exam1/questions)
    """
    validate_pdf(file)

    # Only clean the FILENAME, NOT the directories
    directory = os.path.dirname(output_path)
    filename = os.path.basename(output_path)

    filename = secure_filename(filename)

    # Final path
    final_path = os.path.join(directory, filename + ".pdf")

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    try:
        with open(final_path, "wb") as f:
            content = file.file.read()
            f.write(content)

    except Exception as e:
        raise HTTPException(500, f"Failed to save file: {str(e)}")

    return final_path
