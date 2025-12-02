from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from app.utils import save_pdf_secure
from app.grader import grade_copy
from app.preprocess import extract_text_from_pdf
from app.reviews import submit_review, list_reviews, resolve_review
from app.models.llm import ask_llm
from app.preprocess import extract_text_from_pdf
from fastapi import UploadFile, File

app = FastAPI()

@app.post("/upload_exam")
async def upload_exam(exam_id: str,
                      questions: UploadFile = File(...),
                      correction: UploadFile = File(...),
                      bareme: UploadFile = File(...)):

    try:
        base_dir = f"uploads/exams/{exam_id}"
        os.makedirs(base_dir, exist_ok=True)

        q_path = save_pdf_secure(questions, f"{base_dir}/questions")
        c_path = save_pdf_secure(correction, f"{base_dir}/correction")
        b_path = save_pdf_secure(bareme, f"{base_dir}/bareme")

        return {"status": "success",
                "exam_id": exam_id,
                "paths": {
                    "questions": q_path,
                    "correction": c_path,
                    "bareme": b_path
                }}

    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/upload_copy")
async def upload_copy(exam_id: str,
                      student_name: str,
                      copy: UploadFile = File(...)):

    try:
        base_dir = f"uploads/students/{exam_id}/{student_name}"
        os.makedirs(base_dir, exist_ok=True)

        path = save_pdf_secure(copy, f"{base_dir}/copy")

        return {"status": "success",
                "exam_id": exam_id,
                "student": student_name,
                "path": path}

    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/grade_copy")
async def grade_exam_copy(exam_id: str,
                          student_name: str):

    try:
        base_dir = f"uploads/students/{exam_id}/{student_name}"
        copy_path = f"{base_dir}/copy.pdf"

        if not os.path.exists(copy_path):
            raise HTTPException(404, "Student copy not found")

        text = extract_text_from_pdf(copy_path)
        results = grade_copy(exam_id, student_name, text)

        return {"status": "success",
                "exam_id": exam_id,
                "student": student_name,
                "results": results}

    except Exception as e:
        raise HTTPException(500, str(e))
    

   

@app.post("/reviews/submit")
async def api_submit_review(exam_id: str, student: str, problem_type: str, message: str):
    return submit_review(exam_id, student, problem_type, message)

@app.get("/reviews/get")
async def api_get_reviews(exam_id: str):
    return list_reviews(exam_id)

@app.post("/reviews/resolve")
async def api_resolve_review(exam_id: str, review_id: str):
    return resolve_review(exam_id, review_id)



@app.get("/test/llm")
def test_llm():
    res = ask_llm("What is AI?", "AI is...", "AI is intelligence...", 5)
    return {"result": res}

@app.post("/test/pdf")
async def test_pdf(file: UploadFile = File(...)):
    """
    Test PDF text extraction (PyMuPDF + OCR fallback).
    """
    # Save the uploaded file temporarily
    contents = await file.read()
    temp_path = "temp_test_pdf.pdf"

    with open(temp_path, "wb") as f:
        f.write(contents)

    # Extract text
    text = extract_text_from_pdf(temp_path)

  
    return {"extracted_text": text}

@app.post("/test/grade")
async def test_grade():
    """
    Test full grading pipeline with one question.
    """
    question = "Compute the limit lim (x→0) sin(x)/x."
    correct_answer = "The limit is 1."
    student_answer = "The limit goes to 1."
    bareme = 2

    from grader import grade_answer

    score, justification = grade_answer(
        question, correct_answer, student_answer, bareme
    )

    return {
        "score": score,
        "justification": justification
    }
