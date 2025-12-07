import os
import csv

from app.parsers.questions_parser import parse_questions
from app.parsers.correction_parser import parse_corrections
from app.parsers.bareme_parser import parse_bareme
from app.parsers.student_parser import parse_student_answers

from app.models.llm import ask_llm
from app.models.embeddings import compute_similarity
from app.preprocess import extract_text_from_pdf


# ---------------------------------------------
# Extract a numeric score from LLM output
# ---------------------------------------------
def extract_score(text: str) -> float:
    """
    Extract a score from LLM output.
    Formats supported:
    SCORE: 3
    SCORE = 4
    SCORE: 3/4
    80%
    """
    import re

    patterns = [
        r"score\s*[:=]\s*(\d+)\s*/\s*(\d+)",  # SCORE: 3/4
        r"score\s*[:=]\s*(\d+)",             # SCORE: 3
        r"(\d+)\s*/\s*(\d+)",                # 3/4
        r"(\d+)\s*%",                        # 80%
    ]

    for p in patterns:
        m = re.search(p, text, flags=re.IGNORECASE)
        if m:
            if "/" in m.group(0):
                val = float(m.group(1))
                total = float(m.group(2))
                return round((val / total) * 100, 2)
            if "%" in m.group(0):
                return float(m.group(1))
            return float(m.group(1))

    return 0.0


# ---------------------------------------------
# Normalize score (0–100)
# ---------------------------------------------
def normalize_score(score: float) -> float:
    try:
        return max(0, min(float(score), 100))
    except:
        return 0.0


# ---------------------------------------------
# Grade ONE question
# ---------------------------------------------
def grade_question(q_id, question_text, correct_answer, student_answer, bareme):
    """
    Returns:
    {
      "question": Q1,
      "score": x,
      "similarity": y,
      "feedback": "...",
      "bareme": bareme,
      "student_answer": "...",
      "correct_answer": "..."
    }
    """

    # 1) Embedding similarity
    similarity = compute_similarity(student_answer, correct_answer)

    # 2) LLM grading
    llm_response = ask_llm(question_text, correct_answer, student_answer, bareme)

    llm_raw = llm_response.strip()
    llm_score = extract_score(llm_raw)
    llm_score = normalize_score(llm_score)

    # 3) Combine scores
    final_score = round(llm_score * (0.7 + 0.3 * similarity), 2)

    return {
        "question": q_id,
        "score": final_score,
        "similarity": similarity,
        "feedback": llm_raw,
        "bareme": bareme,
        "student_answer": student_answer,
        "correct_answer": correct_answer,
    }


# ---------------------------------------------
# Save result to CSV
# ---------------------------------------------
def save_grade_csv(exam_id: str, student: str, results: list, total_score: float):
    folder = f"results/{exam_id}"
    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/grades.csv"
    exists = os.path.exists(path)

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "student", "question", "score", "similarity",
                "feedback", "bareme", "student_answer", "correct_answer", "total"
            ])

        for r in results:
            writer.writerow([
                student,
                r["question"],
                r["score"],
                r["similarity"],
                r["feedback"],
                r["bareme"],
                r["student_answer"],
                r["correct_answer"],
                total_score
            ])


# ---------------------------------------------
# Grade entire copy (PHASE 2)
# ---------------------------------------------
def grade_copy(exam_id: str, student: str, raw_student_text: str):
    """
    Full multi-question grading pipeline:
    - Extract teacher questions
    - Extract corrections
    - Extract bareme
    - Extract student answers
    - Grade each question
    """

    # -------------------------
    # Load exam official files
    # -------------------------
    q_text = extract_text_from_pdf(f"uploads/exams/{exam_id}/questions.pdf")
    c_text = extract_text_from_pdf(f"uploads/exams/{exam_id}/correction.pdf")
    b_text = extract_text_from_pdf(f"uploads/exams/{exam_id}/bareme.pdf")

    # -------------------------
    # Parse them
    # -------------------------
    questions = parse_questions(q_text)
    corrections = parse_corrections(c_text)
    baremes = parse_bareme(b_text)

    # -------------------------
    # Parse student copy
    # -------------------------
    student_answers = parse_student_answers(raw_student_text)

    # -------------------------
    # Grade per question
    # -------------------------
    results = []
    total_score = 0

    for q_id, q_info in questions.items():
        question_text = q_info["question"]
        correct_answer = corrections.get(q_id, "")
        bareme = baremes.get(q_id, 0)
        student_answer = student_answers.get(q_id, "")

        q_result = grade_question(
            q_id,
            question_text,
            correct_answer,
            student_answer,
            bareme
        )

        results.append(q_result)
        total_score += q_result["score"]

    # -------------------------
    # Save CSV
    # -------------------------
    save_grade_csv(exam_id, student, results, total_score)

    # -------------------------
    # Final JSON response
    # -------------------------
    return {
        "student": student,
        "exam_id": exam_id,
        "total_score": round(total_score, 2),
        "questions": results
    }
