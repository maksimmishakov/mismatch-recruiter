# Advanced Matching Algorithm - ML-based job-candidate matching

import logging
import numpy as np
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class AdvancedMatcher:
    """Advanced matching algorithm using TF-IDF and cosine similarity."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500, lowercase=True)
        self.weights = {
            'skills': 0.35,
            'experience': 0.25,
            'education': 0.20,
            'location': 0.10,
            'salary': 0.10
        }
    
    def calculate_match_score(
        self,
        candidate: Dict,
        vacancy: Dict
    ) -> Tuple[float, Dict]:
        """Calculate match score between candidate and vacancy.
        
        Returns:
            Tuple of (score, details)
        """
        scores = {}
        
        # Skills matching (35%)
        candidate_skills = ' '.join(candidate.get('skills', []))
        vacancy_skills = ' '.join(vacancy.get('required_skills', []))
        skills_score = self._calculate_text_similarity(candidate_skills, vacancy_skills)
        scores['skills'] = skills_score * self.weights['skills']
        
        # Experience matching (25%)
        exp_score = self._match_experience(
            candidate.get('years_experience', 0),
            vacancy.get('experience_required', 0)
        )
        scores['experience'] = exp_score * self.weights['experience']
        
        # Education matching (20%)
        edu_score = self._match_education(
            candidate.get('education_level', ''),
            vacancy.get('education_required', '')
        )
        scores['education'] = edu_score * self.weights['education']
        
        # Location matching (10%)
        location_score = 100.0 if candidate.get('location') == vacancy.get('location') else 50.0
        scores['location'] = (location_score / 100.0) * self.weights['location']
        
        # Salary expectation matching (10%)
        salary_score = self._match_salary(
            candidate.get('salary_expectation', 0),
            vacancy.get('salary_range', {})
        )
        scores['salary'] = salary_score * self.weights['salary']
        
        total_score = sum(scores.values()) * 100
        
        return round(total_score, 2), scores
    
    @staticmethod
    def _calculate_text_similarity(text1: str, text2: str) -> float:
        """Calculate similarity between two text strings using TF-IDF."""
        if not text1 or not text2:
            return 0.0
        
        documents = [text1, text2]
        vectorizer = TfidfVectorizer()
        try:
            tfidf_matrix = vectorizer.fit_transform(documents)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Text similarity calculation error: {e}")
            return 0.0
    
    @staticmethod
    def _match_experience(candidate_exp: int, required_exp: int) -> float:
        """Match candidate experience with job requirement."""
        if candidate_exp >= required_exp:
            return 1.0
        elif candidate_exp >= required_exp * 0.7:
            return 0.8
        elif candidate_exp >= required_exp * 0.5:
            return 0.6
        else:
            return 0.4
    
    @staticmethod
    def _match_education(candidate_edu: str, required_edu: str) -> float:
        """Match candidate education level with job requirement."""
        education_levels = {
            'high_school': 1,
            'bachelor': 2,
            'master': 3,
            'phd': 4
        }
        
        candidate_level = education_levels.get(candidate_edu, 0)
        required_level = education_levels.get(required_edu, 0)
        
        if candidate_level >= required_level:
            return 1.0
        elif candidate_level >= required_level - 1:
            return 0.7
        else:
            return 0.4
    
    @staticmethod
    def _match_salary(candidate_salary: int, salary_range: Dict) -> float:
        """Match candidate salary expectation with job salary range."""
        salary_min = salary_range.get('min', 0)
        salary_max = salary_range.get('max', float('inf'))
        
        if salary_min <= candidate_salary <= salary_max:
            return 1.0
        elif candidate_salary < salary_min:
            return 0.7
        else:
            return 0.5
    
    def get_match_level(self, score: float) -> str:
        """Get qualitative match level from score."""
        if score >= 80:
            return 'excellent'
        elif score >= 60:
            return 'good'
        elif score >= 40:
            return 'fair'
        else:
            return 'poor'
