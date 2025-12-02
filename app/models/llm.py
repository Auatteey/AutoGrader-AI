import google.generativeai as genai
from app.config import GEMINI_API_KEY


# Configure API
genai.configure(api_key=GEMINI_API_KEY)

# Load the model once
model = genai.GenerativeModel("gemini-2.0-flash")

def ask_llm(question, correct_answer, student_answer, bareme):
    """
    Ask Gemini Flash 2.5 to grade a student's answer.
    Output REQUIRED format:
    
    SCORE: <number>
    JUSTIFICATION: <text>
    """

    prompt = f"""
You are an exam grading AI.

GRADE THE STUDENT ANSWER STRICTLY BASED ON THE EXPECTED ANSWER AND THE BAREME.

QUESTION:
{question}

EXPECTED CORRECTION:
{correct_answer}

STUDENT ANSWER:
{student_answer}

MAX SCORE: {bareme}

VERY IMPORTANT:
Respond ONLY in this exact format:

SCORE: <number between 0 and {bareme}>
JUSTIFICATION: <short explanation>

Do NOT add anything before or after.
"""

    # Generate response
    response = model.generate_content(prompt)

    return response.text
