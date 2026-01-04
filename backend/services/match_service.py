from typing import List, Dict
from datetime import datetime

class MatchService:
    """Matching Algorithm Service"""
    
    @staticmethod
    def calculate_skill_match(job_skills: List[str], candidate_skills: List[str]) -> float:
        """Calculate skill match percentage"""
        if not job_skills:
            return 100.0
        matched = len(set(candidate_skills) & set(job_skills))
        return (matched / len(job_skills)) * 100
    
    @staticmethod
    def calculate_experience_match(job_seniority: str, years_exp: int) -> float:
        """Calculate experience match"""
        seniority_map = {'Junior': (0, 3), 'Mid': (3, 7), 'Senior': (7, 100)}
        if job_seniority not in seniority_map:
            return 50.0
        
        min_exp, max_exp = seniority_map[job_seniority]
        if years_exp < min_exp:
            return (years_exp / min_exp) * 50
        elif years_exp > max_exp:
            return 100.0
        else:
            return ((years_exp - min_exp) / (max_exp - min_exp)) * 100
    
    @staticmethod
    def calculate_location_match(job_mode: str, candidate_pref: str) -> float:
        """Calculate location/work mode match"""
        if job_mode == 'Remote' or candidate_pref == 'Remote':
            return 100.0
        elif job_mode == candidate_pref:
            return 100.0
        elif job_mode == 'Hybrid' or candidate_pref == 'Hybrid':
            return 75.0
        return 0.0
    
    @staticmethod
    def create_match(candidate_id: int, job_id: int, candidate_data: Dict, job_data: Dict) -> Dict:
        """Create match between candidate and job"""
        skill_score = MatchService.calculate_skill_match(job_data.get('skills', []), candidate_data.get('skills', []))
        exp_score = MatchService.calculate_experience_match(job_data.get('seniority', 'Mid'), candidate_data.get('experience', 0))
        loc_score = MatchService.calculate_location_match(job_data.get('mode', 'Hybrid'), candidate_data.get('preference', 'Hybrid'))
        
        final_score = skill_score * 0.5 + exp_score * 0.3 + loc_score * 0.2
        
        if final_score >= 80:
            recommendation = 'PERFECT_MATCH'
        elif final_score >= 60:
            recommendation = 'GOOD_MATCH'
        elif final_score >= 40:
            recommendation = 'FAIR_MATCH'
        else:
            recommendation = 'POOR_MATCH'
        
        return {
            'id': 1,
            'candidate_id': candidate_id,
            'job_id': job_id,
            'skill_score': skill_score,
            'experience_score': exp_score,
            'location_score': loc_score,
            'final_score': round(final_score, 2),
            'recommendation': recommendation,
            'created_at': datetime.now().isoformat()
        }
