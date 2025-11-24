"""
Models module for AutoGrader AI
Contains embedding models and LLM models
"""

from app.models.embeddings import EmbeddingModel
from app.models.llm import LLMModel

__all__ = ['EmbeddingModel', 'LLMModel']

