# services/embedding_service.py - AI/ML Embedding Service for Resume-Job Matching

import os
import numpy as np
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating semantic embeddings for resumes and jobs."""
    
    def __init__(self):
        """Initialize embedding service."""
        try:
            from sentence_transformers import SentenceTransformer
            # Using multilingual model for Russian language support
            self.model = SentenceTransformer('sentence-transformers/multilingual-MiniLM-L12-v2')
            self.model_name = 'sentence-transformers/multilingual-MiniLM-L12-v2'
            logger.info(f"Embedding model loaded: {self.model_name}")
        except ImportError:
            logger.warning("sentence-transformers not installed, using fallback")
            self.model = None
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text.
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        if not text or not isinstance(text, str):
            logger.warning(f"Invalid input text: {text}")
            return np.zeros(384)  # Default vector size
        
        try:
            if self.model:
                embedding = self.model.encode(text, convert_to_numpy=True)
            else:
                # Fallback: random embedding for testing
                embedding = np.random.randn(384)
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return np.zeros(384)
    
    def generate_resume_embedding(self, resume_text: str) -> np.ndarray:
        """Generate embedding specific to resume content.
        
        Args:
            resume_text: Resume content
            
        Returns:
            Embedding vector
        """
        # Clean and prepare resume text
        cleaned = self._preprocess_text(resume_text)
        return self.generate_embedding(cleaned)
    
    def generate_job_embedding(self, job_description: str) -> np.ndarray:
        """Generate embedding specific to job description.
        
        Args:
            job_description: Job description text
            
        Returns:
            Embedding vector
        """
        # Clean and prepare job description
        cleaned = self._preprocess_text(job_description)
        return self.generate_embedding(cleaned)
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            # Normalize vectors
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            # Cosine similarity
            similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
            # Convert to 0-1 range
            return float((similarity + 1) / 2)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def batch_generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Generate embeddings for multiple texts efficiently.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        try:
            if self.model:
                embeddings = self.model.encode(texts, convert_to_numpy=True)
                return [emb for emb in embeddings]
            else:
                return [np.random.randn(384) for _ in texts]
        except Exception as e:
            logger.error(f"Error in batch embedding: {e}")
            return [np.zeros(384) for _ in texts]
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for embedding.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = " ".join(text.split())
        # Limit length to improve performance
        text = text[:5000]  # Max 5000 characters
        return text
    
    def get_top_matches(self, query_embedding: np.ndarray, 
                       candidates: List[np.ndarray], 
                       top_k: int = 10) -> List[Tuple[int, float]]:
        """Get top K matching embeddings.
        
        Args:
            query_embedding: Query embedding vector
            candidates: List of candidate embeddings
            top_k: Number of top matches to return
            
        Returns:
            List of (index, similarity) tuples
        """
        similarities = []
        for idx, candidate in enumerate(candidates):
            sim = self.calculate_similarity(query_embedding, candidate)
            similarities.append((idx, sim))
        
        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]


# Global instance
_embedding_service = None


def get_embedding_service() -> EmbeddingService:
    """Get or create embedding service instance."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
