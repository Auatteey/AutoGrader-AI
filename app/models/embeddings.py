"""
Embedding Models for AutoGrader AI
Handles text embeddings using various models (SentenceTransformers, OpenAI, etc.)
"""

import os
from typing import Union, List
import numpy as np
from sentence_transformers import SentenceTransformer, util
from app.config import EMBEDDINGS_MODEL


class EmbeddingModel:
    """
    Wrapper class for embedding models
    Supports both local models (SentenceTransformers) and OpenAI embeddings
    """
    
    def __init__(self, model_name: str = None, use_openai: bool = False):
        """
        Initialize embedding model
        
        Args:
            model_name: Name of the model to use
                       For SentenceTransformers: 'sentence-transformers/all-MiniLM-L6-v2'
                       For OpenAI: 'text-embedding-3-small' or 'text-embedding-3-large'
            use_openai: If True, use OpenAI embeddings API instead of local model
        """
        self.model_name = model_name or EMBEDDINGS_MODEL
        self.use_openai = use_openai
        self.model = None
        
        if not use_openai:
            # Use local SentenceTransformers model
            local_model = 'sentence-transformers/all-MiniLM-L6-v2'
            print(f"Loading local embedding model: {local_model}")
            self.model = SentenceTransformer(local_model)
        else:
            # OpenAI embeddings will be used via API calls
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def encode(self, text: Union[str, List[str]], convert_to_tensor: bool = False) -> Union[np.ndarray, List[float]]:
        """
        Encode text into embeddings
        
        Args:
            text: Single text string or list of texts
            convert_to_tensor: If True, return PyTorch tensor (for SentenceTransformers)
        
        Returns:
            Embedding vector(s) as numpy array or list
        """
        if self.use_openai:
            return self._encode_openai(text)
        else:
            return self._encode_local(text, convert_to_tensor)
    
    def _encode_local(self, text: Union[str, List[str]], convert_to_tensor: bool = False):
        """Encode using local SentenceTransformers model"""
        if self.model is None:
            raise ValueError("Model not initialized")
        
        embeddings = self.model.encode(text, convert_to_tensor=convert_to_tensor)
        
        if convert_to_tensor:
            return embeddings
        else:
            return embeddings if isinstance(embeddings, np.ndarray) else embeddings.cpu().numpy()
    
    def _encode_openai(self, text: Union[str, List[str]]):
        """Encode using OpenAI API"""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        client = OpenAI(api_key=self.api_key)
        
        if isinstance(text, str):
            text = [text]
        
        response = client.embeddings.create(
            model=self.model_name,
            input=text
        )
        
        embeddings = [item.embedding for item in response.data]
        
        if len(embeddings) == 1:
            return np.array(embeddings[0])
        else:
            return np.array(embeddings)
    
    def cosine_similarity(self, emb1, emb2) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            emb1: First embedding vector
            emb2: Second embedding vector
        
        Returns:
            Cosine similarity score (0 to 1)
        """
        if self.use_openai or isinstance(emb1, np.ndarray):
            # Use numpy for OpenAI embeddings or numpy arrays
            return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))
        else:
            # Use PyTorch util for SentenceTransformers tensors
            return util.cos_sim(emb1, emb2).item()
    
    def batch_encode(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Encode multiple texts efficiently
        
        Args:
            texts: List of text strings
            batch_size: Number of texts to process at once
        
        Returns:
            Array of embeddings
        """
        if self.use_openai:
            return self._encode_openai(texts)
        else:
            if self.model is None:
                raise ValueError("Model not initialized")
            return self.model.encode(texts, batch_size=batch_size, show_progress_bar=True)


# Global instance for backward compatibility
_default_embedding_model = None

def get_embedding_model(use_openai: bool = False) -> EmbeddingModel:
    """
    Get or create the default embedding model instance
    
    Args:
        use_openai: Whether to use OpenAI embeddings
    
    Returns:
        EmbeddingModel instance
    """
    global _default_embedding_model
    
    if _default_embedding_model is None:
        _default_embedding_model = EmbeddingModel(use_openai=use_openai)
    
    return _default_embedding_model

