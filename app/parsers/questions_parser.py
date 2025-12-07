import re

def parse_questions(text: str):
    """
    Extract questions and expected formats.
    Returns dict: { "Q1": {question, expected_format}, ... }
    """
    blocks = re.split(r"\n\s*\d+\.\s*\n", text)[1:]  # split after QUESTION numbers
    result = {}

    for i, block in enumerate(blocks, start=1):
        q_id = f"Q{i}"

        # Extract the question text
        question_match = re.search(r"Question:\s*(.+)", block)
        question = question_match.group(1).strip() if question_match else ""

        # Extract expected format
        format_match = re.search(r"Expected answer format:\s*(.+)", block)
        expected_format = format_match.group(1).strip() if format_match else "Unknown"

        result[q_id] = {
            "question": question,
            "expected_format": expected_format
        }

    return result
