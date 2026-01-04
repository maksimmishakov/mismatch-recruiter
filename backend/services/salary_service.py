from typing import Dict
from datetime import datetime

class SalaryService:
    """Salary Intelligence Service"""
    
    SALARY_BENCHMARKS = {
        'Python Developer': {'Junior': 60000, 'Mid': 92500, 'Senior': 150000},
        'React Developer': {'Junior': 65000, 'Mid': 100000, 'Senior': 160000},
        'Product Manager': {'Junior': 82500, 'Mid': 120000, 'Senior': 185000},
        'Data Scientist': {'Junior': 77500, 'Mid': 112500, 'Senior': 170000}
    }
    
    @staticmethod
    def get_salary_range(job_title: str, seniority: str, location: str = 'USA') -> Dict:
        """Get salary range for job position"""
        matched_title = None
        for title in SalaryService.SALARY_BENCHMARKS:
            if title.lower() in job_title.lower():
                matched_title = title
                break
        
        if not matched_title:
            return {'min': 70000, 'max': 120000, 'avg': 95000}
        
        avg = SalaryService.SALARY_BENCHMARKS[matched_title].get(seniority, 95000)
        return {
            'title': matched_title,
            'seniority': seniority,
            'location': location,
            'min': int(avg * 0.75),
            'max': int(avg * 1.25),
            'avg': avg
        }
    
    @staticmethod
    def calculate_salary_match(job_min: int, job_max: int, cand_min: int, cand_max: int) -> Dict:
        """Calculate salary compatibility"""
        overlap_min = max(job_min, cand_min)
        overlap_max = min(job_max, cand_max)
        
        if overlap_min > overlap_max:
            score = 0
        else:
            score = min(100, ((overlap_max - overlap_min) / (job_max - job_min) * 100) if job_max > job_min else 50)
        
        return {
            'job_range': {'min': job_min, 'max': job_max},
            'candidate_range': {'min': cand_min, 'max': cand_max},
            'compatibility_score': score,
            'match_status': 'Perfect' if score >= 80 else 'Good' if score >= 60 else 'Poor'
        }
