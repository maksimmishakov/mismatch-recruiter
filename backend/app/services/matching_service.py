from app.models import Candidate, JobPosting, Match
from app import db
from typing import Dict, List, Tuple

class MatchingService:
    """Service for calculating job-candidate matches"""
    
    @staticmethod
    def calculate_skill_match(candidate_skills: List[str], job_required_skills: List[str]) -> float:
        """Calculate skill match score (0.0 to 1.0)"""
        if not job_required_skills:
            return 1.0
        
        candidate_set = set(s.lower() for s in candidate_skills) if candidate_skills else set()
        required_set = set(s.lower() for s in job_required_skills)
        
        if not required_set:
            return 1.0
        
        matches = len(candidate_set & required_set)
        return matches / len(required_set)
    
    @staticmethod
    def calculate_experience_match(candidate_experience: int, job_level: str) -> float:
        """Calculate experience match score"""
        if not candidate_experience or not job_level:
            return 0.5
        
        level_mapping = {'junior': (0, 3), 'mid': (3, 7), 'senior': (7, 100)}
        min_exp, max_exp = level_mapping.get(job_level.lower(), (0, 100))
        
        if min_exp <= candidate_experience <= max_exp:
            return 1.0
        elif candidate_experience > max_exp:
            return 0.8  # Over-qualified
        else:
            return max(0, 0.5 - (min_exp - candidate_experience) * 0.1)
    
    @staticmethod
    def calculate_overall_match(skill_match: float, experience_match: float) -> float:
        """Calculate overall match score"""
        # Weight: 60% skill match, 40% experience match
        return (skill_match * 0.6) + (experience_match * 0.4)
    
    @staticmethod
    def find_matches_for_candidate(candidate_id: int, threshold: float = 0.5) -> List[Dict]:
        """Find all matching jobs for a candidate"""
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return []
        
        jobs = JobPosting.query.filter_by(is_active=True).all()
        matches = []
        
        for job in jobs:
            skill_match = MatchingService.calculate_skill_match(
                candidate.skills or [],
                job.required_skills or []
            )
            exp_match = MatchingService.calculate_experience_match(
                candidate.experience_years,
                job.experience_level
            )
            overall = MatchingService.calculate_overall_match(skill_match, exp_match)
            
            if overall >= threshold:
                matches.append({
                    'job_id': job.id,
                    'job_title': job.title,
                    'company': job.company,
                    'skill_match': round(skill_match, 2),
                    'experience_match': round(exp_match, 2),
                    'overall_score': round(overall, 2)
                })
        
        return sorted(matches, key=lambda x: x['overall_score'], reverse=True)
