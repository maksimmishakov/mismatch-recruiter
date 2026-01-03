"""Embedding Service for Resume/Job Analysis"""
import numpy as np
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating embeddings from text"""
    
    def __init__(self):
        self.model = None
        self.logger = logging.getLogger(__name__)
    
    def generate_embedding(self, text: str) -> list:
        """Generate embedding for given text"""
        if not text:
            return [0] * 384
        
        try:
            # Placeholder embedding (384-dimensional)
            embedding = np.random.rand(384).tolist()
            self.logger.info(f"Generated embedding for text: {len(text)} chars")
            return embedding
        except Exception as e:
            self.logger.error(f"Error generating embedding: {e}")
            return [0] * 384
    
    def similarity(self, embedding1: list, embedding2: list) -> float:
        """Calculate cosine similarity between two embeddings"""
        try:
            a = np.array(embedding1)
            b = np.array(embedding2)
            
            dot_product = np.dot(a, b)
            magnitude_a = np.linalg.norm(a)
            magnitude_b = np.linalg.norm(b)
            
            if magnitude_a == 0 or magnitude_b == 0:
                return 0.0
            
            similarity = dot_product / (magnitude_a * magnitude_b)
            return float(similarity)
        except Exception as e:
            self.logger.error(f"Error calculating similarity: {e}")
            return 0.0

embedding_service = EmbeddingService()
