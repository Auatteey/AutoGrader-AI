import os
import csv

def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def save_grade(exam_name, student_name, note):
    path = f"results/{exam_name}/grades.csv"
    ensure_dir(os.path.dirname(path))

    write_header = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["student", "grade"])
        writer.writerow([student_name, note])
