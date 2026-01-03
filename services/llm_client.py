"""LLM Client for AI-powered Resume Analysis"""
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class LLMClient:
    """Client for interacting with LLM APIs"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
    
    def analyze_resume(self, resume_text: str) -> dict:
        """Analyze resume using LLM"""
        try:
            result = {
                'skills': self._extract_skills(resume_text),
                'experience_years': self._estimate_experience(resume_text),
                'education': self._extract_education(resume_text),
                'red_flags': self._identify_red_flags(resume_text),
                'score': self._calculate_score(resume_text),
                'analyzed_at': datetime.utcnow().isoformat()
            }
            self.logger.info(f"Resume analyzed: score {result['score']}")
            return result
        except Exception as e:
            self.logger.error(f"Error analyzing resume: {e}")
            return {'error': str(e), 'score': 0}
    
    def analyze_job(self, job_description: str) -> dict:
        """Analyze job description"""
        try:
            result = {
                'required_skills': self._extract_skills(job_description),
                'seniority_level': self._estimate_seniority(job_description),
                'key_qualifications': self._extract_qualifications(job_description),
                'analyzed_at': datetime.utcnow().isoformat()
            }
            self.logger.info(f"Job analyzed: {len(result['required_skills'])} skills")
            return result
        except Exception as e:
            self.logger.error(f"Error analyzing job: {e}")
            return {'error': str(e)}
    
    def match_candidate(self, resume: dict, job: dict) -> dict:
        """Match candidate to job"""
        try:
            resume_skills = set(resume.get('skills', []))
            job_skills = set(job.get('required_skills', []))
            
            matching_skills = resume_skills & job_skills
            missing_skills = job_skills - resume_skills
            
            match_score = len(matching_skills) / max(len(job_skills), 1) * 100
            
            result = {
                'match_score': round(match_score, 2),
                'matching_skills': list(matching_skills),
                'missing_skills': list(missing_skills),
                'matched_at': datetime.utcnow().isoformat()
            }
            self.logger.info(f"Candidate matched: {result['match_score']}%")
            return result
        except Exception as e:
            self.logger.error(f"Error matching candidate: {e}")
            return {'error': str(e), 'match_score': 0}
    
    def _extract_skills(self, text: str) -> list:
        common_skills = ['python', 'javascript', 'java', 'react', 'docker', 'aws', 'sql']
        found_skills = []
        text_lower = text.lower()
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill)
        return found_skills
    
    def _extract_education(self, text: str) -> list:
        educations = []
        if 'bachelor' in text.lower():
            educations.append('Bachelor')
        if 'master' in text.lower():
            educations.append('Master')
        if 'phd' in text.lower():
            educations.append('PhD')
        return educations
    
    def _estimate_experience(self, text: str) -> int:
        import re
        matches = re.findall(r'(\d+)\s*(?:years?|yrs?)', text.lower())
        return int(matches[0]) if matches else 0
    
    def _estimate_seniority(self, text: str) -> str:
        text_lower = text.lower()
        if 'senior' in text_lower or 'lead' in text_lower:
            return 'senior'
        elif 'junior' in text_lower:
            return 'junior'
        return 'mid-level'
    
    def _extract_qualifications(self, text: str) -> list:
        return []
    
    def _identify_red_flags(self, text: str) -> list:
        red_flags = []
        if 'fired' in text.lower():
            red_flags.append('Termination mentioned')
        if 'gap' in text.lower():
            red_flags.append('Employment gap')
        return red_flags
    
    def _calculate_score(self, text: str) -> float:
        score = 50.0
        if len(text) > 500:
            score += 10
        if self._extract_education(text):
            score += 15
        if self._extract_skills(text):
            score += 25
        return min(100.0, score)

llm_client = LLMClient()
