import os
import csv
from app.models.llm import ask_llm


def grade_answer(question, correct_answer, student_answer, bareme):
    """
    A clean and unified grading function.
    Returns (score:int, justification:str).
    """

    result = ask_llm(question, correct_answer, student_answer, bareme)

    try:
        lines = result.split("\n")
        score_line = next((x for x in lines if x.upper().startswith("SCORE")), None)
        just_line = next((x for x in lines if x.upper().startswith("JUSTIFICATION")), None)

        score = int(score_line.split(":")[1].strip())
        justification = just_line.split(":", 1)[1].strip()

        return score, justification

    except Exception as e:
        return 0, f"Parsing error: {e}\nRaw output: {result}"


def grade_copy(exam_id: str, student: str, text: str):
    """
    SAFE MODE:
    Treats the entire student copy as a single answer.
    """

    question = "Correct this mathematical exam."
    correct_answer = "Refer to the correction PDF."
    student_answer = text
    bareme = 20

    score, justification = grade_answer(
        question,
        correct_answer,
        student_answer,
        bareme
    )

    results = [{
        "question": "Q1",
        "score_final": score,
        "feedback": justification
    }]

    total_score = score

    save_grade_csv(exam_id, student, results, total_score)

    return {
        "student": student,
        "exam_id": exam_id,
        "questions": results,
        "total_score": total_score
    }


def save_grade_csv(exam_id: str, student: str, results: list, final_score: float):
    """
    Saves results/<exam_id>/grades.csv
    """

    folder = f"results/{exam_id}"
    os.makedirs(folder, exist_ok=True)
    path = f"{folder}/grades.csv"

    file_exists = os.path.exists(path)

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["student", "question", "score", "feedback", "total"])

        for r in results:
            writer.writerow([
                student,
                r["question"],
                r["score_final"],
                r["feedback"],
                final_score
            ])
