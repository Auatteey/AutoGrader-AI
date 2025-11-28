# app/main.py
from fastapi import FastAPI, UploadFile, File, Form
from pathlib import Path
from app.preprocess import extract_text_from_pdf
from app.grader import grade_copy
from app.utils import save_grade_csv
from app.config import EXAM_DIR, STUDENT_DIR, RESULTS_DIR

app = FastAPI()


#########################################
# UPLOAD EXAM
#########################################
@app.post("/api/upload_exam")
async def upload_exam(
    exam_name: str = Form(...),
    questions: UploadFile = File(...),
    correction: UploadFile = File(...),
    bareme: UploadFile = File(...)
):

    exam_dir = Path(EXAM_DIR) / exam_name
    exam_dir.mkdir(parents=True, exist_ok=True)

    # Save PDFs
    with open(exam_dir / "questions.pdf", "wb") as f:
        f.write(await questions.read())
    with open(exam_dir / "correction.pdf", "wb") as f:
        f.write(await correction.read())
    with open(exam_dir / "bareme.pdf", "wb") as f:
        f.write(await bareme.read())

    return {"status": "ok", "message": f"Exam '{exam_name}' uploaded successfully."}


#########################################
# GRADE STUDENT
#########################################
@app.post("/api/grade_student")
async def grade_student(
    exam_name: str = Form(...),
    student_name: str = Form(...),
    copy: UploadFile = File(...)
):

    exam_path = Path(EXAM_DIR) / exam_name
    correction_pdf = exam_path / "correction.pdf"
    bareme_pdf = exam_path / "bareme.pdf"

    # Verify exam availability
    if not exam_path.exists():
        return {"status": "error", "message": "Exam files missing."}

    # Save student copy
    student_dir = Path(STUDENT_DIR) / exam_name
    student_dir.mkdir(parents=True, exist_ok=True)

    copy_path = student_dir / f"{student_name}.pdf"
    with open(copy_path, "wb") as f:
        f.write(await copy.read())

    # Extract text
    correction_text = extract_text_from_pdf(correction_pdf)
    bareme_text = extract_text_from_pdf(bareme_pdf)
    student_text = extract_text_from_pdf(copy_path)

    # Grade with IA
    result = grade_copy(student_text, correction_text, bareme_text)

    grade = float(result.get("grade", 0))
    similarity = float(result.get("similarity_score", 0))
    feedback = result.get("feedback", "No detailed feedback was generated.")

    # Save CSV
    save_grade_csv(exam_name, student_name, grade, similarity, feedback)

    return {
        "status": "ok",
        "exam": exam_name,
        "student": student_name,
        "grade": grade,
        "similarity_score": similarity,
        "feedback": feedback,
        "message": "Grading complete."
    }


#########################################
# GET ALL GRADES FOR EXAM
#########################################
@app.get("/api/exam/{exam_name}/grades")
def get_exam_grades(exam_name: str):

    csv_path = Path(RESULTS_DIR) / exam_name / "grades.csv"

    if not csv_path.exists():
        return {"status": "error", "message": "No grades available for this exam."}

    # Read CSV
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            student, grade, sim, feedback = line.strip().split(",", 3)
            rows.append({
                "student": student,
                "grade": float(grade),
                "similarity": float(sim),
                "feedback": feedback.strip('"')
            })

    return {"status": "ok", "exam": exam_name, "results": rows}

