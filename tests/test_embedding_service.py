import pytest
import numpy as np
from services.embedding_service import EmbeddingService


class TestEmbeddingService:
    """Test suite for EmbeddingService"""

    @pytest.fixture
    def service(self):
        return EmbeddingService()

    def test_generate_embedding(self, service):
        """Test basic embedding generation"""
        text = "Python developer with 5 years experience"
        embedding = service.generate_embedding(text)
        
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) > 0
        assert embedding.dtype == np.float32 or embedding.dtype == np.float64

    def test_generate_resume_embedding(self, service):
        """Test resume-specific embedding"""
        resume = "John Doe\nSoftware Engineer\nSkills: Python, JavaScript, React"
        embedding = service.generate_resume_embedding(resume)
        
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) > 0

    def test_generate_job_embedding(self, service):
        """Test job description embedding"""
        job_desc = "Senior Backend Engineer\nRequirements: Python, AWS, PostgreSQL"
        embedding = service.generate_job_embedding(job_desc)
        
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) > 0

    def test_calculate_similarity(self, service):
        """Test similarity calculation"""
        text1 = "Python developer"
        text2 = "Python developer"
        
        emb1 = service.generate_embedding(text1)
        emb2 = service.generate_embedding(text2)
        
        similarity = service.calculate_similarity(emb1, emb2)
        
        assert 0 <= similarity <= 1
        assert similarity > 0.5  # Same text should have high similarity

    def test_batch_embeddings(self, service):
        """Test batch embedding generation"""
        texts = [
            "Python developer",
            "JavaScript engineer",
            "Data scientist"
        ]
        
        embeddings = service.batch_generate_embeddings(texts)
        
        assert len(embeddings) == 3
        assert all(isinstance(emb, np.ndarray) for emb in embeddings)

    def test_empty_text_handling(self, service):
        """Test handling of empty text"""
        embedding = service.generate_embedding("")
        assert isinstance(embedding, np.ndarray)

    def test_get_top_matches(self, service):
        """Test top matches retrieval"""
        query_text = "Senior Python developer"
        candidate_texts = [
            "Python developer",
            "Java developer",
            "Senior Python engineer",
            "Frontend developer",
            "Python backend engineer"
        ]
        
        query_emb = service.generate_embedding(query_text)
        candidate_embs = service.batch_generate_embeddings(candidate_texts)
        
        matches = service.get_top_matches(query_emb, candidate_embs, top_k=3)
        
        assert len(matches) == 3
        assert all(isinstance(match, tuple) for match in matches)
        assert matches[0][1] >= matches[1][1]  # Scores should be sorted


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
