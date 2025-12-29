import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class ParsedResume:
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    experience_years: float = 0.0
    primary_role: str = "Software Engineer"
    confidence_score: float = 0.0

class ResumeParser:
    """Parse resume text with high accuracy"""
    
    def __init__(self):
        self.skill_db = self._load_skills()
    
    def parse(self, text: str) -> ParsedResume:
        """Parse resume text"""
        if not text:
            return ParsedResume()
        
        email = self._extract_email(text)
        phone = self._extract_phone(text)
        skills = self._extract_skills(text)
        exp_years = self._extract_experience(text)
        role = self._detect_role(skills, text)
        confidence = self._calculate_confidence(email, phone, skills, exp_years)
        
        return ParsedResume(
            email=email,
            phone=phone,
            skills=skills,
            experience_years=exp_years,
            primary_role=role,
            confidence_score=confidence
        )
    
    def _extract_email(self, text: str) -> Optional[str]:
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(pattern, text)
        return matches[0] if matches else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        pattern = r'\+?[1-9]\d{1,14}'
        matches = re.findall(pattern, text)
        return matches[0] if matches else None
    
    def _extract_skills(self, text: str) -> List[str]:
        found = []
        text_lower = text.lower()
        for skill in self.skill_db:
            if skill.lower() in text_lower:
                found.append(skill)
        return found[:20]
    
    def _extract_experience(self, text: str) -> float:
        pattern = r'(\d+)\s*(?:years?|yrs?|лет)'
        matches = re.findall(pattern, text, re.IGNORECASE)
        return float(matches[0]) if matches else 0.0
    
    def _detect_role(self, skills: List[str], text: str) -> str:
        roles = {
            "Backend Engineer": ["python", "django", "java", "golang"],
            "Frontend Engineer": ["react", "vue", "javascript", "typescript"],
            "DevOps Engineer": ["docker", "kubernetes", "aws"],
        }
        skills_lower = [s.lower() for s in skills]
        for role, role_skills in roles.items():
            if any(rs in skills_lower for rs in role_skills):
                return role
        return "Software Engineer"
    
    def _calculate_confidence(self, email, phone, skills, exp_years) -> float:
        score = 0.0
        if email: score += 0.25
        if phone: score += 0.25
        if len(skills) > 0: score += 0.25
        if exp_years > 0: score += 0.25
        return score
    
    def _load_skills(self) -> List[str]:
        return [
            "Python", "JavaScript", "Java", "TypeScript", "Go", "Rust",
            "Django", "Flask", "FastAPI", "React", "Vue", "Node.js",
            "PostgreSQL", "MongoDB", "Redis", "Elasticsearch",
            "Docker", "Kubernetes", "AWS", "GCP", "Azure",
        ]
