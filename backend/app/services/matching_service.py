# Matching service for candidate-job matching algorithms
from typing import Tuple, Optional
from app.models import Candidate, JobPosting

class MatchingService:
    """Service for calculating match scores between candidates and jobs"""
    
    @staticmethod
    def calculate_skill_match(candidate: Candidate, job: JobPosting) -> float:
        """
        Calculate skill match score (0.0 - 1.0)
        Based on intersection of candidate skills and required skills
        """
        if not job.required_skills:
            return 0.5  # Default if no skills required
        
        if not candidate.skills:
            return 0.0  # No match if candidate has no skills
        
        required_skills = set(s.lower() for s in job.required_skills)
        candidate_skills = set(s.lower() for s in candidate.skills)
        
        if not required_skills:
            return 0.5
        
        matched_skills = required_skills.intersection(candidate_skills)
        score = len(matched_skills) / len(required_skills)
        return min(score, 1.0)
    
    @staticmethod
    def calculate_experience_match(candidate: Candidate, job: JobPosting) -> float:
        """
        Calculate experience match score (0.0 - 1.0)
        Based on candidate's experience vs required experience
        """
        if not job.experience_required:
            return 0.5
        
        candidate_exp = candidate.experience_years or 0
        required_exp = job.experience_required or 0
        
        if candidate_exp >= required_exp:
            return 1.0  # Meets or exceeds requirement
        
        # Partial credit for having some experience
        if required_exp == 0:
            return 0.5
        
        score = candidate_exp / required_exp
        return max(min(score, 1.0), 0.0)
    
    @staticmethod
    def calculate_salary_match(candidate: Candidate, job: JobPosting) -> float:
        """
        Calculate salary match score (0.0 - 1.0)
        Based on candidate's salary expectation vs job salary range
        """
        if not job.salary_min or not job.salary_max:
            return 0.5  # Unknown salary match
        
        candidate_salary = candidate.salary_expectation or 0
        
        if candidate_salary == 0:
            return 0.5  # No expectation provided
        
        # Perfect match if within range
        if job.salary_min <= candidate_salary <= job.salary_max:
            return 1.0
        
        # Below minimum
        if candidate_salary < job.salary_min:
            gap = job.salary_min - candidate_salary
            max_gap = job.salary_min * 0.3  # Allow 30% below
            if gap <= max_gap:
                score = 1.0 - (gap / max_gap) * 0.5
                return max(score, 0.0)
            return 0.0
        
        # Above maximum
        if candidate_salary > job.salary_max:
            gap = candidate_salary - job.salary_max
            max_gap = job.salary_max * 0.3  # Allow 30% above
            if gap <= max_gap:
                score = 1.0 - (gap / max_gap) * 0.5
                return max(score, 0.0)
            return 0.0
    
    @staticmethod
    def calculate_location_match(candidate: Candidate, job: JobPosting) -> float:
        """
        Calculate location match score (0.0 - 1.0)
        Simple exact match for now
        """
        if not job.location or not candidate.location:
            return 0.5  # Unknown
        
        # Exact match
        if job.location.lower() == candidate.location.lower():
            return 1.0
        
        # Partial match (same city)
        if job.location.lower().split(',')[0] == candidate.location.lower().split(',')[0]:
            return 0.8
        
        return 0.0
    
    @staticmethod
    def calculate_overall_match(candidate: Candidate, job: JobPosting) -> Tuple[float, float, float, float, float]:
        """
        Calculate overall match and component scores
        Returns: (overall_score, skill, experience, salary, location)
        """
        skill_score = MatchingService.calculate_skill_match(candidate, job)
        experience_score = MatchingService.calculate_experience_match(candidate, job)
        salary_score = MatchingService.calculate_salary_match(candidate, job)
        location_score = MatchingService.calculate_location_match(candidate, job)
        
        # Weighted average
        weights = {
            'skill': 0.35,
            'experience': 0.25,
            'salary': 0.25,
            'location': 0.15
        }
        
        overall = (
            skill_score * weights['skill'] +
            experience_score * weights['experience'] +
            salary_score * weights['salary'] +
            location_score * weights['location']
        )
        
        return overall, skill_score, experience_score, salary_score, location_score
