import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Dossiers pour exams, copies et résultats
EXAM_DIR = os.path.join(BASE_DIR, "uploads/exams")
STUDENT_DIR = os.path.join(BASE_DIR, "uploads/students")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

LLM_MODEL = "gpt-4o-mini"
EMBEDDINGS_MODEL = "text-embedding-3-small"

# Note: Set OPENAI_API_KEY as environment variable, don't print it!