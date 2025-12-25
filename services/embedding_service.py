from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    def match_resume_to_job(self, resume_text, job_description):
        """Match with semantic understanding, not just keywords"""
        
        resume_embedding = self.model.encode(resume_text)
        job_embedding = self.model.encode(job_description)
        
        similarity = cosine_similarity(
            [resume_embedding], 
            [job_embedding]
        )[0][0]
        
        return {
            "match_score": round(similarity * 100),
            "semantic_fit": "high" if similarity > 0.7 else "medium" if similarity > 0.5 else "low",
            "confidence": round(similarity * 100)
        }
