"""Advanced matching service for candidates and vacancies."""
import numpy as np
from typing import List, Dict, Tuple
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
            'culture_fit': 0.1,
        }

    def match_candidate_to_vacancy(
        self,
        candidate: Dict,
        vacancy: Dict
    ) -> Tuple[float, Dict]:
        """Match single candidate to vacancy."""
        details = {}
        total_score = 0

        # Skills matching (30% weight)
        skills_score = self._match_skills(
            candidate.get('skills', []),
            vacancy.get('required_skills', [])
        )
        details['skills'] = skills_score
        total_score += skills_score * self.weights['skills']

        # Experience matching (20% weight)
        exp_score = self._match_experience(
            candidate.get('years_experience', 0),
            vacancy.get('experience_required', 0)
        )
        details['experience'] = exp_score
        total_score += exp_score * self.weights['experience']

        # Location matching (15% weight)
        location_score = self._match_location(
            candidate.get('location', ''),
            vacancy.get('location', '')
        )
        details['location'] = location_score
        total_score += location_score * self.weights['location']

        # Salary expectations matching (15% weight)
        salary_score = self._match_salary(
            candidate.get('salary_expectation', 0),
            vacancy.get('salary_range', {})
        )
        details['salary'] = salary_score
        total_score += salary_score * self.weights['salary']

        # Education matching (10% weight)
        education_score = self._match_education(
            candidate.get('education', {}),
            vacancy.get('education_required', '')
        )
        details['education'] = education_score
        total_score += education_score * self.weights['education']

        # Culture fit (10% weight)
        culture_score = self._calculate_culture_fit(
            candidate,
            vacancy
        )
        details['culture_fit'] = culture_score
        total_score += culture_score * self.weights['culture_fit']

        return total_score, details

    def _match_skills(self, candidate_skills: List[str], required_skills: List[str]) -> float:
        """Match candidate skills with required skills. Returns score 0-100."""
        if not required_skills:
            return 100.0

        candidate_set = set(s.lower().strip() for s in candidate_skills)
        required_set = set(s.lower().strip() for s in required_skills)

        if not candidate_set:
            return 0.0

        intersection = len(candidate_set & required_set)
        union = len(candidate_set | required_set)
        jaccard_score = intersection / union if union > 0 else 0

        return jaccard_score * 100

    def _match_experience(self, candidate_years: int, required_years: int) -> float:
        """Match candidate years of experience with requirement."""
        if required_years == 0:
            return 100.0

        if candidate_years < required_years * 0.8:
            return (candidate_years / (required_years * 0.8)) * 50
        elif candidate_years < required_years:
            return 50 + (candidate_years - required_years * 0.8) / (required_years * 0.2) * 25
        elif candidate_years <= required_years * 1.5:
            return 100.0
        else:
            return 95.0

    def _match_location(self, candidate_loc: str, vacancy_loc: str) -> float:
        """Match candidate location with vacancy location."""
        if not vacancy_loc:
            return 100.0

        candidate_loc = candidate_loc.lower().strip()
        vacancy_loc = vacancy_loc.lower().strip()

        if candidate_loc == vacancy_loc:
            return 100.0
        elif "remote" in vacancy_loc.lower():
            return 100.0 if "remote" in candidate_loc.lower() else 80.0
        else:
            return 70.0

    def _match_salary(self, candidate_exp: int, vacancy_range: Dict) -> float:
        """Match candidate salary expectations with vacancy range."""
        min_salary = vacancy_range.get('min', 0)
        max_salary = vacancy_range.get('max', float('inf'))

        if min_salary == 0 or max_salary == float('inf'):
            return 100.0

        if candidate_exp <= min_salary:
            return 100.0
        elif candidate_exp <= max_salary:
            return 100.0
        else:
            percentage_above = (candidate_exp - max_salary) / max_salary
            return max(0.0, 100.0 - percentage_above * 50)

    def _match_education(self, candidate_edu: Dict, required_edu: str) -> float:
        """Match candidate education with requirement."""
        if not required_edu:
            return 100.0

        education_levels = {
            'high_school': 1,
            'bachelor': 2,
            'master': 3,
            'phd': 4,
        }

        candidate_level = education_levels.get(
            candidate_edu.get('level', 'high_school').lower(),
            1
        )
        required_level = education_levels.get(required_edu.lower(), 2)

        if candidate_level >= required_level:
            return 100.0
        else:
            return (candidate_level / required_level) * 100

    def _calculate_culture_fit(self, candidate: Dict, vacancy: Dict) -> float:
        """Calculate culture fit between candidate and company."""
        score = 50.0

        candidate_values = set(candidate.get('values', []))
        company_values = set(vacancy.get('company_values', []))

        if company_values:
            values_match = len(candidate_values & company_values) / len(company_values)
            score += values_match * 30
        else:
            score += 30

        return min(100.0, score)

    def batch_match_candidates(
        self,
        candidates: List[Dict],
        vacancy: Dict,
        limit: int = 10
    ) -> List[Tuple[Dict, float, Dict]]:
        """Match multiple candidates to vacancy and return top matches."""
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
                'low_match': 0,
            }

        scores = [score for _, score, _ in matches]

        return {
            'total': len(matches),
            'average_score': sum(scores) / len(scores),
            'high_match': sum(1 for s in scores if s >= 80),
            'medium_match': sum(1 for s in scores if 50 <= s < 80),
            'low_match': sum(1 for s in scores if s < 50),
            'max_score': max(scores),
            'min_score': min(scores),
        }

matching_service = MatchingService()
