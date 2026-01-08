"""Matching service for calculating match scores between candidates and jobs."""
from typing import Dict

class MatchingService:
    """AI-powered matching algorithm for MisMatch."""
    SKILL_WEIGHT = 0.40
    EXPERIENCE_WEIGHT = 0.30
    SALARY_WEIGHT = 0.20
    LOCATION_WEIGHT = 0.10
    
    @staticmethod
    def calculate_match_score(candidate, job) -> Dict[str, float]:
        """Calculate comprehensive match score between candidate and job."""
        skill_score = MatchingService.calculate_skill_match(
            candidate.skills, job.required_skills
        )
        experience_score = MatchingService.calculate_experience_match(
            candidate.experience_years, job.min_experience
        )
        salary_score = MatchingService.calculate_salary_match(
            candidate.salary_expectation, job.min_salary, job.max_salary
        )
        location_score = MatchingService.calculate_location_match(
            candidate.location, job.location
        )
        
        total_score = (
            skill_score * MatchingService.SKILL_WEIGHT +
            experience_score * MatchingService.EXPERIENCE_WEIGHT +
            salary_score * MatchingService.SALARY_WEIGHT +
            location_score * MatchingService.LOCATION_WEIGHT
        )
        total_score = max(0.0, min(1.0, total_score))
        
        return {
            'total': round(total_score, 3),
            'skill_match': round(skill_score, 3),
            'experience_match': round(experience_score, 3),
            'salary_match': round(salary_score, 3),
            'location_match': round(location_score, 3)
        }
    
    @staticmethod
    def calculate_skill_match(candidate_skills: list, required_skills: list) -> float:
        """Calculate skill match percentage."""
        if not required_skills or len(required_skills) == 0:
            return 0.5
        if not candidate_skills or len(candidate_skills) == 0:
            return 0.0
        
        candidate_skills_lower = [s.lower().strip() for s in candidate_skills]
        required_skills_lower = [s.lower().strip() for s in required_skills]
        matched = sum(1 for skill in required_skills_lower if skill in candidate_skills_lower)
        match_percentage = matched / len(required_skills_lower)
        return min(match_percentage, 1.0)
    
    @staticmethod
    def calculate_experience_match(candidate_years: int, min_experience: int) -> float:
        """Calculate experience match."""
        if min_experience == 0:
            return min(candidate_years / 5, 1.0)
        if candidate_years < min_experience:
            return candidate_years / min_experience * 0.8
        years_above_min = candidate_years - min_experience
        bonus = min(years_above_min / 5, 0.2)
        return min(0.8 + bonus, 1.0)
    
    @staticmethod
    def calculate_salary_match(candidate_salary: int, min_salary: int, max_salary: int) -> float:
        """Calculate salary match."""
        if min_salary == 0 and max_salary == 0:
            return 0.7
        if candidate_salary == 0:
            return 0.7
        if min_salary <= candidate_salary <= max_salary:
            return 1.0
        if candidate_salary < min_salary:
            percentage_below = (min_salary - candidate_salary) / min_salary
            if percentage_below > 0.2:
                return 0.3
            return 0.7 - (percentage_below * 2)
        if candidate_salary > max_salary:
            percentage_above = (candidate_salary - max_salary) / max_salary
            if percentage_above > 0.2:
                return 0.2
            return 0.7 - (percentage_above * 2)
        return 0.5
    
    @staticmethod
    def calculate_location_match(candidate_location: str, job_location: str) -> float:
        """Calculate location match."""
        if not candidate_location or not job_location:
            return 0.7
        candidate_loc_lower = candidate_location.lower().strip()
        job_loc_lower = job_location.lower().strip()
        if candidate_loc_lower == job_loc_lower:
            return 1.0
        if candidate_loc_lower.split(',')[0] == job_loc_lower.split(',')[0]:
            return 0.8
        return 0.5
