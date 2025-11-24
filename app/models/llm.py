"""
LLM Models for AutoGrader AI
Handles Large Language Models for grading and feedback generation
"""

import os
from typing import List, Dict, Optional
from app.config import LLM_MODEL


class LLMModel:
    """
    Wrapper class for LLM models
    Supports OpenAI models (GPT-4, GPT-3.5, etc.)
    Can be extended to support other providers (Anthropic, local models, etc.)
    """
    
    def __init__(self, model_name: str = None, api_key: str = None):
        """
        Initialize LLM model
        
        Args:
            model_name: Name of the model (e.g., 'gpt-4o-mini', 'gpt-4', 'gpt-3.5-turbo')
            api_key: OpenAI API key (if None, reads from OPENAI_API_KEY env var)
        """
        self.model_name = model_name or LLM_MODEL
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """
        Generate text using the LLM
        
        Args:
            prompt: User prompt/question
            system_prompt: System instruction (role definition)
            temperature: Sampling temperature (0-2, higher = more creative)
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters for the API call
        
        Returns:
            Generated text response
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def grade_assignment(
        self,
        student_answer: str,
        correct_answer: str,
        rubric: str,
        max_score: float = 20.0
    ) -> Dict:
        """
        Grade a student's assignment using LLM
        
        Args:
            student_answer: Student's answer text
            correct_answer: Correct/reference answer
            rubric: Grading rubric and criteria
            max_score: Maximum possible score (default: 20)
        
        Returns:
            Dictionary with grade, feedback, and explanation
        """
        system_prompt = f"""You are an expert teacher grading student assignments.
Your task is to evaluate the student's answer against the correct answer and rubric.
Provide a fair, accurate grade and detailed feedback.

Grading Rubric:
{rubric}

Maximum Score: {max_score}/20

Provide your response in a structured format."""
        
        prompt = f"""Please grade the following student assignment:

STUDENT ANSWER:
{student_answer}

CORRECT ANSWER:
{correct_answer}

Please provide:
1. A numerical grade (out of {max_score})
2. Detailed feedback explaining what the student did well
3. Areas for improvement
4. Specific examples from their answer

Format your response as:
Grade: X/{max_score}
Feedback: [detailed feedback]
Strengths: [list strengths]
Improvements: [list areas to improve]"""
        
        response = self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,  # Lower temperature for more consistent grading
            max_tokens=1500
        )
        
        # Parse the response to extract grade
        # This is a simple parser - you might want to improve it
        grade = self._extract_grade(response, max_score)
        
        return {
            "grade": grade,
            "feedback": response,
            "max_score": max_score,
            "model": self.model_name
        }
    
    def generate_feedback(
        self,
        student_answer: str,
        correct_answer: str,
        grade: float,
        max_score: float = 20.0
    ) -> str:
        """
        Generate detailed feedback for a student
        
        Args:
            student_answer: Student's answer
            correct_answer: Correct answer
            grade: Assigned grade
            max_score: Maximum possible score
        
        Returns:
            Detailed feedback text
        """
        system_prompt = """You are a helpful teacher providing constructive feedback to students.
Be encouraging, specific, and focus on helping the student learn."""
        
        prompt = f"""A student received a grade of {grade}/{max_score} for their assignment.

STUDENT ANSWER:
{student_answer}

CORRECT ANSWER:
{correct_answer}

Please provide:
1. What the student did correctly
2. What they missed or got wrong
3. Specific suggestions for improvement
4. Encouraging words to help them learn

Write in a friendly, educational tone."""
        
        return self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=1000
        )
    
    def compare_answers(
        self,
        student_answer: str,
        correct_answer: str
    ) -> Dict:
        """
        Compare student answer with correct answer
        
        Args:
            student_answer: Student's answer
            correct_answer: Correct answer
        
        Returns:
            Dictionary with comparison analysis
        """
        system_prompt = """You are an expert at analyzing and comparing answers.
Identify similarities, differences, and key points."""
        
        prompt = f"""Compare these two answers:

STUDENT ANSWER:
{student_answer}

CORRECT ANSWER:
{correct_answer}

Please analyze:
1. Key concepts covered in both
2. Concepts missing in student answer
3. Concepts incorrectly stated
4. Overall accuracy percentage estimate"""
        
        analysis = self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=800
        )
        
        return {
            "analysis": analysis,
            "model": self.model_name
        }
    
    def _extract_grade(self, response: str, max_score: float) -> float:
        """
        Extract numerical grade from LLM response
        Simple parser - can be improved with regex or structured output
        
        Args:
            response: LLM response text
            max_score: Maximum possible score
        
        Returns:
            Extracted grade (0 to max_score)
        """
        import re
        
        # Look for patterns like "Grade: 15/20" or "15/20" or "Grade: 15"
        patterns = [
            rf"grade[:\s]+(\d+\.?\d*)\s*/\s*{max_score}",
            rf"grade[:\s]+(\d+\.?\d*)",
            rf"(\d+\.?\d*)\s*/\s*{max_score}",
            rf"score[:\s]+(\d+\.?\d*)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                try:
                    grade = float(match.group(1))
                    return min(max(0, grade), max_score)  # Clamp between 0 and max_score
                except ValueError:
                    continue
        
        # If no grade found, return None (caller should handle)
        return None


# Global instance for backward compatibility
_default_llm_model = None

def get_llm_model(model_name: str = None) -> LLMModel:
    """
    Get or create the default LLM model instance
    
    Args:
        model_name: Optional model name override
    
    Returns:
        LLMModel instance
    """
    global _default_llm_model
    
    if _default_llm_model is None or (model_name and _default_llm_model.model_name != model_name):
        _default_llm_model = LLMModel(model_name=model_name)
    
    return _default_llm_model

