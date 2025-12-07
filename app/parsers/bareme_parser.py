import re

def parse_bareme(text: str):
    """
    Extract scoring weights.
    Returns dict: {"Q1": 4, "Q2": 6, "Q3": 10}
    """
    lines = text.split("\n")
    result = {}

    for line in lines:
        m = re.match(r"(Q\d+):\s*(\d+)", line)
        if m:
            q_id = m.group(1)
            score = int(m.group(2))
            result[q_id] = score

    return result
