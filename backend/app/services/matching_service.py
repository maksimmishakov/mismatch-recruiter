"""Advanced matching service for candidates and vacancies."""
import numpy as np
from typing import List, Dict, Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logger = logging.getLogger(__name__)

class MatchingService:
    """Advanced matching engine using ML algorithms."""
    
    def __init__(self):
        """Initialize matching service."""
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.weights = {
            'skills': 0.3,
            'experience': 0.2,
            'location': 0.15,
            'salary': 0.15,
            'education': 0.1,
            'culture_fit': 0.1
        }
    
    def match_candidate_to_vacancy(self, candidate: Dict, vacancy: Dict) -> Tuple[float, Dict]:
        """Match single candidate to vacancy."""
        details = {}
        total_score = 0
        
        # Skills matching
        skills_score = self.match_skills(
            candidate.get('skills', []),
            vacancy.get('required_skills', [])
        )
        details['skills'] = skills_score
        total_score += skills_score * self.weights['skills']
        
        # Experience matching
        exp_score = self.match_experience(
            candidate.get('years_experience', 0),
            vacancy.get('experience_required', 0)
        )
        details['experience'] = exp_score
        total_score += exp_score * self.weights['experience']
        
        # Location matching
        location_score = self.match_location(
            candidate.get('location', ''),
            vacancy.get('location', '')
        )
        details['location'] = location_score
        total_score += location_score * self.weights['location']
        
        # Salary matching
        salary_score = self.match_salary(
            candidate.get('salary_expectation', 0),
            vacancy.get('salary_range', {})
        )
        details['salary'] = salary_score
        total_score += salary_score * self.weights['salary']
        
        # Education matching
        education_score = self.match_education(
            candidate.get('education', {}),
            vacancy.get('education_required', '')
        )
        details['education'] = education_score
        total_score += education_score * self.weights['education']
        
        # Culture fit
        culture_score = self.calculate_culture_fit(candidate, vacancy)
        details['culture_fit'] = culture_score
        total_score += culture_score * self.weights['culture_fit']
        
        return total_score, details
    
    def match_skills(self, candidate_skills: List[str], required_skills: List[str]) -> float:
        """Match candidate skills with required skills."""
        if not required_skills:
            return 100.0
        
        candidate_set = {s.lower().strip() for s in candidate_skills}
        required_set = {s.lower().strip() for s in required_skills}
        
        if not candidate_set:
            return 0.0
        
        # Jaccard similarity
        intersection = len(candidate_set & required_set)
        union = len(candidate_set | required_set)
        jaccard_score = (intersection / union * 100) if union > 0 else 0
        
        return jaccard_score
    
    def match_experience(self, candidate_years: int, required_years: int) -> float:
        """Match years of experience."""
        if required_years == 0:
            return 100.0
        
        if candidate_years >= required_years:
            return min(100.0, (candidate_years / required_years) * 100)
        else:
            return (candidate_years / required_years) * 80
    
    def match_location(self, candidate_loc: str, vacancy_loc: str) -> float:
        """Match location."""
        if not vacancy_loc:
            return 100.0
        
        candidate_loc = candidate_loc.lower().strip()
        vacancy_loc = vacancy_loc.lower().strip()
        
        if candidate_loc == vacancy_loc:
            return 100.0
        elif 'remote' in vacancy_loc:
            return 100.0 if 'remote' in candidate_loc else 80.0
        else:
            return 70.0
    
    def match_salary(self, candidate_exp: int, vacancy_range: Dict) -> float:
        """Match salary expectations."""
        min_salary = vacancy_range.get('min', 0)
        max_salary = vacancy_range.get('max', float('inf'))
        
        if min_salary == 0 or max_salary == float('inf'):
            return 100.0
        
        if candidate_exp <= max_salary:
            return 100.0
        else:
            return max(0.0, 100.0 - ((candidate_exp - max_salary) / max_salary) * 50)
    
    def match_education(self, candidate_edu: Dict, required_edu: str) -> float:
        """Match education level."""
        if not required_edu:
            return 100.0
        
        education_levels = {
            'highschool': 1,
            'bachelor': 2,
            'master': 3,
            'phd': 4
        }
        
        candidate_level = education_levels.get(candidate_edu.get('level', 'highschool').lower(), 1)
        required_level = education_levels.get(required_edu.lower(), 2)
        
        if candidate_level >= required_level:
            return 100.0
        else:
            return (candidate_level / required_level) * 100
    
    def calculate_culture_fit(self, candidate: Dict, vacancy: Dict) -> float:
        """Calculate culture fit score."""
        score = 50.0
        
        # Values alignment
        candidate_values = set(candidate.get('values', []))
        company_values = set(vacancy.get('company_values', []))
        
        if company_values:
            values_match = len(candidate_values & company_values)
            score += (values_match / len(company_values)) * 30
        else:
            score += 30
        
        # Work style
        candidate_style = candidate.get('work_style', '')
        vacancy_style = vacancy.get('work_style', '')
        
        if candidate_style == vacancy_style:
            score += 20
        else:
            score += 10
        
        return min(100.0, score)
    
    def batch_match_candidates(self, candidates: List[Dict], vacancy: Dict, limit: int = 10) -> List[Tuple]:
        """Match multiple candidates to vacancy."""
        matches = []
        for candidate in candidates:
            score, details = self.match_candidate_to_vacancy(candidate, vacancy)
            matches.append((candidate, score, details))
        
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:limit]
    
    def get_matching_stats(self, matches: List[Tuple]) -> Dict:
        """Get statistics about matching results."""
        if not matches:
            return {
                'total': 0,
                'average_score': 0,
                'high_match': 0,
                'medium_match': 0,
                'low_match': 0
            }
        
        scores = [score for _, score, _ in matches]
        return {
            'total': len(matches),
            'average_score': sum(scores) / len(scores),
            'high_match': sum(1 for s in scores if s >= 80),
            'medium_match': sum(1 for s in scores if 50 <= s < 80),
            'low_match': sum(1 for s in scores if s < 50),
            'max_score': max(scores),
            'min_score': min(scores)
        }

# Initialize global service
matching_service = MatchingService()
