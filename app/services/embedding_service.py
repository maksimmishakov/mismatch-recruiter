"""Embedding Service - Generate embeddings for text data"""

import logging
from typing import List, Dict, Optional
import hashlib

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating and managing text embeddings"""
    
    def __init__(self):
        """Initialize the embedding service"""
        self.embedding_cache = {}
        self.dimension = 384
        logger.info("EmbeddingService initialized")
    
    def embed(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding, or None if error
        """
        try:
            if not text:
                return None
            
            # Check cache first
            text_hash = hashlib.md5(text.encode()).hexdigest()
            if text_hash in self.embedding_cache:
                return self.embedding_cache[text_hash]
            
            # Generate simple embedding (in production, use transformers or similar)
            embedding = self._simple_embed(text)
            
            # Cache the result
            self.embedding_cache[text_hash] = embedding
            return embedding
        except Exception as e:
            logger.error(f"Error embedding text: {e}")
            return None
    
    def embed_batch(self, texts: List[str]) -> Optional[List[List[float]]]:
        """Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings, or None if error
        """
        try:
            if not texts:
                return None
            
            embeddings = []
            for text in texts:
                embedding = self.embed(text)
                if embedding is not None:
                    embeddings.append(embedding)
            
            return embeddings if embeddings else None
        except Exception as e:
            logger.error(f"Error in batch embedding: {e}")
            return None
    
    def similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Similarity score between -1 and 1
        """
        try:
            if not embedding1 or not embedding2:
                return 0.0
            
            dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
            norm1 = sum(a ** 2 for a in embedding1) ** 0.5
            norm2 = sum(b ** 2 for b in embedding2) ** 0.5
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def _simple_embed(self, text: str) -> List[float]:
        """Simple embedding generation using character frequencies"""
        embedding = [0.0] * self.dimension
        
        for i, char in enumerate(text.lower()):
            idx = (ord(char) + i) % self.dimension
            embedding[idx] += 1.0 / len(text)
        
        # Normalize
        norm = sum(x ** 2 for x in embedding) ** 0.5
        if norm > 0:
            embedding = [x / norm for x in embedding]
        
        return embedding
    
    def clear_cache(self) -> None:
        """Clear the embedding cache"""
        self.embedding_cache.clear()
        logger.info("Embedding cache cleared")
