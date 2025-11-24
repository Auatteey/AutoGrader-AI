from fastapi import FastAPI, UploadFile, File, Form
from pathlib import Path
from app.preprocess import extract_text_from_pdf
from app.grader import grade_copy
from app.utils import save_grade
from app.config import EXAM_DIR, STUDENT_DIR

app = FastAPI()


@app.post("/api/upload_exam")
async def upload_exam(
    exam_name: str = Form(...),
    questions: UploadFile = File(...),
    correction: UploadFile = File(...),
    bareme: UploadFile = File(...)
):
    exam_dir = Path(EXAM_DIR) / exam_name
    exam_dir.mkdir(parents=True, exist_ok=True)

    # Sauvegarde des fichiers PDF
    with open(exam_dir / "questions.pdf", "wb") as f:
        f.write(await questions.read())
    with open(exam_dir / "correction.pdf", "wb") as f:
        f.write(await correction.read())
    with open(exam_dir / "bareme.pdf", "wb") as f:
        f.write(await bareme.read())

    return {"status": "ok", "message": f"Examen '{exam_name}' uploadé avec succès"}


@app.post("/api/grade_student")
async def grade_student(
    exam_name: str = Form(...),
    student_name: str = Form(...),
    copy: UploadFile = File(...)
):
    exam_path = Path(EXAM_DIR) / exam_name
    correction_pdf = exam_path / "correction.pdf"
    bareme_pdf = exam_path / "bareme.pdf"

    # Vérification des fichiers
    if not exam_path.exists() or not correction_pdf.exists() or not bareme_pdf.exists():
        return {"status": "error",
                "message": "Les fichiers de l'examen n'existent pas. Veuillez d'abord uploader l'examen."}

    # Sauvegarde de la copie de l’étudiant
    student_dir = Path(STUDENT_DIR) / exam_name
    student_dir.mkdir(parents=True, exist_ok=True)

    copy_path = student_dir / f"{student_name}.pdf"
    with open(copy_path, "wb") as f:
        f.write(await copy.read())

    # Extraction du texte
    correction_text = extract_text_from_pdf(correction_pdf)
    bareme_text = extract_text_from_pdf(bareme_pdf)
    student_text = extract_text_from_pdf(copy_path)

    # Calcul de la note
    result = grade_copy(student_text, correction_text, bareme_text)
    save_grade(exam_name, student_name, result["grade"])

    return {
        "status": "ok",
        "student": student_name,
        "grade": result["grade"],
        "similarity_score": result.get("similarity_score", None),
        "message": "Correction terminée"
    }


@app.get("/grade/{exam_name}")
def grade_exam(exam_name: str):
    exam_path = Path(EXAM_DIR) / exam_name
    correction_pdf = exam_path / "correction.pdf"
    bareme_pdf = exam_path / "bareme.pdf"

    if not exam_path.exists() or not correction_pdf.exists() or not bareme_pdf.exists():
        return {"status": "error", "message": "Les fichiers de l'examen n'existent pas."}

    correction_text = extract_text_from_pdf(correction_pdf)
    bareme_text = extract_text_from_pdf(bareme_pdf)

    student_dir = Path(STUDENT_DIR) / exam_name
    if not student_dir.exists():
        return {"status": "error", "message": "Aucune copie d’étudiant trouvée."}

    grades = {}
    for file in student_dir.glob("*.pdf"):
        student_name = file.stem
        student_text = extract_text_from_pdf(file)
        result = grade_copy(student_text, correction_text, bareme_text)
        save_grade(exam_name, student_name, result["grade"])
        grades[student_name] = result["grade"]

    return {"status": "ok", "exam": exam_name, "grades": grades}
