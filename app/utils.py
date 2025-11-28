# app/utils.py
from pathlib import Path
from app.config import RESULTS_DIR
import csv
import os

def save_grade_csv(exam_name, student_name, grade, similarity, feedback):
    exam_result_dir = Path(RESULTS_DIR) / exam_name
    exam_result_dir.mkdir(parents=True, exist_ok=True)

    csv_path = exam_result_dir / "grades.csv"

    file_exists = csv_path.exists()

    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["student_name", "grade", "similarity_score", "feedback"])

        writer.writerow([student_name, grade, similarity, f'"{feedback}"'])
