import re

def parse_corrections(text: str):
    """
    Extract correction answers.
    Returns dict: {"Q1": "...", "Q2": "...", ...}
    """
    lines = text.split("\n")
    result = {}

    for line in lines:
        m = re.match(r"(\d+)\.\s*(.+)", line)
        if m:
            q_id = f"Q{m.group(1)}"
            answer = m.group(2).strip()
            result[q_id] = answer

    return result
