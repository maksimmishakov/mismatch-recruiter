"""Продвинутый парсер резюме с полной структуризацией данных."""

from typing import Dict, Any, List
from datetime import datetime
import re
from app.services.parsing.skill_extractor import SkillExtractor
from app.logger import get_logger

logger = get_logger("resume_parser")

class ResumeParserAdvanced:
    """Full resume parser with structured data extraction."""
    
    def __init__(self):
        self.skill_extractor = SkillExtractor()
    
    def parse(self, raw_text: str) -> Dict[str, Any]:
        """
        Complete resume parsing and structuring.
        Returns structured data with skills, experience, role, tech stack, education, languages.
        """
        try:
            if not raw_text or len(raw_text.strip()) == 0:
                raise ValueError("Empty resume text")
            
            result = {
                'skills': self.skill_extractor.extract(raw_text),
                'experience_years': self._estimate_experience(raw_text),
                'primary_role': self._identify_role(raw_text),
                'tech_stack': self._extract_tech_stack(raw_text),
                'education': self._extract_education(raw_text),
                'languages': self._extract_languages(raw_text),
                'parsing_status': 'success',
                'parsed_at': datetime.utcnow().isoformat(),
                'confidence_score': self._calculate_confidence(raw_text)
            }
            
            logger.info(f"Resume parsed: {len(result['skills'])} skills, {result['experience_years']} years exp")
            return result
            
        except Exception as e:
            logger.error(f"Resume parsing error: {e}", exc_info=True)
            return {
                'skills': [],
                'experience_years': 0,
                'primary_role': None,
                'tech_stack': {'languages': [], 'frameworks': [], 'databases': [], 'tools': []},
                'education': [],
                'languages': [],
                'parsing_status': 'error',
                'error': str(e),
                'parsed_at': datetime.utcnow().isoformat()
            }
    
    def _estimate_experience(self, text: str) -> float:
        """Estimate total experience in years from resume text."""
        patterns = [
            (r'(\d+)\s*\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)', 1.0),
            (r'(\d+)\s*\+?\s*(?:лет|года|years)', 1.0),
            (r'experience.*?(\d+)\s*(?:years?|лет)', 1.0),
        ]
        
        for pattern, weight in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    return min(float(matches[0]), 60)
                except (ValueError, IndexError):
                    continue
        return 0.0
    
    def _identify_role(self, text: str) -> str:
        """Identify primary role/job title from resume."""
        roles_map = {
            'backend engineer': r'(?:backend|server-side)',
            'frontend engineer': r'(?:frontend|ui|ux engineer)',
            'full stack engineer': r'(?:full.?stack)',
            'devops engineer': r'(?:devops|infrastructure)',
            'data scientist': r'(?:data scientist|data science)',
            'ml engineer': r'(?:machine learning|ml engineer)',
            'qa engineer': r'(?:qa|quality assurance)',
            'product manager': r'(?:product manager|pm|product owner)',
            'architect': r'(?:architect|solution architect)',
        }
        
        text_lower = text.lower()
        for role, pattern in roles_map.items():
            if re.search(pattern, text_lower[:500], re.IGNORECASE):
                return role.title()
        return None
    
    def _extract_tech_stack(self, text: str) -> Dict[str, List[str]]:
        """Extract and organize technology stack."""
        skills = self.skill_extractor.extract(text)
        return {
            'languages': [s['name'] for s in skills if s['category'] == 'language'][:8],
            'frameworks': [s['name'] for s in skills if s['category'] == 'framework'][:8],
            'databases': [s['name'] for s in skills if s['category'] == 'database'][:5],
            'tools': [s['name'] for s in skills if s['category'] in ['devops', 'tool', 'cloud']][:8],
        }
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education information."""
        degrees = {
            'phd': [r'(?:phd|ph\.d\.|doctor)', r'(?:доктор)'],
            'master': [r'(?:master|m\.s\.|mba)', r'(?:магистр)'],
            'bachelor': [r'(?:bachelor|b\.s\.|bs|ba)', r'(?:бакалавр)'],
        }
        
        education = []
        text_lower = text.lower()
        for degree_type, patterns in degrees.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    education.append({'type': degree_type, 'found': True})
                    break
        return education
    
    def _extract_languages(self, text: str) -> List[str]:
        """Extract communication languages."""
        languages_map = {
            'English': r'(?:english|eng)',
            'Russian': r'(?:russian|рус)',
            'Spanish': r'(?:spanish|испан)',
            'German': r'(?:german|нем)',
            'French': r'(?:french|фран)',
        }
        
        found = []
        text_lower = text.lower()
        for lang, pattern in languages_map.items():
            if re.search(pattern, text_lower, re.IGNORECASE):
                found.append(lang)
        return found
    
    def _calculate_confidence(self, text: str) -> float:
        """Calculate parsing confidence score (0-1)."""
        score = 0.5
        score += min(len(text) / 5000, 0.3)
        skills = self.skill_extractor.extract(text)
        score += min(len(skills) / 20, 0.2)
        return min(score, 1.0)
