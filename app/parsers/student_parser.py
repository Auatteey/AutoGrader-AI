import re

def parse_student_answers(text: str):
    """
    Capture:
    1. Question...
    Answer...
    2. Question...
    Answer...
    3. Question...
    Answer...
    (fin du texte)
    """

    pattern = r"(\d+)\.\s*(.*?)(?=\n\d+\.\s|$)"
    matches = re.findall(pattern, text, flags=re.DOTALL)

    answers = {}
    for num, ans in matches:
        answers[f"Q{num}"] = ans.strip()

    return answers
