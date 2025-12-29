from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

class JobLevel(Enum):
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    LEAD = "Lead"

@dataclass
class EnrichedJob:
    title: str
    description: str
    company: str
    required_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    job_level: str = "Middle"
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_avg: Optional[float] = None
    location: Optional[str] = None
    location_code: Optional[str] = None
    industry: Optional[str] = None
    remote_friendly: bool = False
    skill_confidence: float = 0.0
    enrichment_quality: float = 0.0

class JobEnricher:
    def __init__(self):
        self.skills_db = self._load_skills_db()
        self.soft_skills_db = self._load_soft_skills()
        self.level_keywords = self._load_level_keywords()
        self.location_db = self._load_locations()
    
    def enrich(self, job_data: Dict) -> EnrichedJob:
        title = job_data.get('title', '')
        description = job_data.get('description', '')
        company = job_data.get('company', '')
        
        required_skills = self._extract_skills(title, description)
        soft_skills = self._extract_soft_skills(description)
        job_level = self._detect_job_level(title, description)
        salary_min = job_data.get('salary_min')
        salary_max = job_data.get('salary_max')
        location = self._standardize_location(job_data.get('location', ''))
        location_code = self._get_location_code(location)
        industry = self._detect_industry(description)
        remote_friendly = self._detect_remote(description)
        
        skill_confidence = min(len(required_skills) / max(len(self.skills_db), 1), 1.0)
        enrichment_quality = self._calculate_quality(
            required_skills, soft_skills, job_level, salary_min, location
        )
        
        salary_avg = None
        if salary_min and salary_max:
            salary_avg = (salary_min + salary_max) / 2
        
        return EnrichedJob(
            title=title,
            description=description,
            company=company,
            required_skills=required_skills,
            soft_skills=soft_skills,
            job_level=job_level,
            salary_min=salary_min,
            salary_max=salary_max,
            salary_avg=salary_avg,
            location=location,
            location_code=location_code,
            industry=industry,
            remote_friendly=remote_friendly,
            skill_confidence=skill_confidence,
            enrichment_quality=enrichment_quality
        )
    
    def _extract_skills(self, title: str, description: str) -> List[str]:
        text = f"{title} {description}".lower()
        found = []
        for skill in self.skills_db:
            if skill.lower() in text:
                found.append(skill)
        return found[:15]
    
    def _extract_soft_skills(self, description: str) -> List[str]:
        text = description.lower()
        found = []
        for skill in self.soft_skills_db:
            if skill.lower() in text:
                found.append(skill)
        return found[:10]
    
    def _detect_job_level(self, title: str, description: str) -> str:
        text = f"{title} {description}".lower()
        for level, keywords in self.level_keywords.items():
            if any(kw in text for kw in keywords):
                return level.value
        return "Middle"
    
    def _standardize_location(self, location: str) -> Optional[str]:
        if not location:
            return None
        location_clean = location.split(',')[0].strip()
        for db_location in self.location_db.keys():
            if location_clean.lower() == db_location.lower():
                return db_location
        return location_clean
    
    def _get_location_code(self, location: Optional[str]) -> Optional[str]:
        if not location:
            return None
        return self.location_db.get(location, "").split("|")[0]
    
    def _detect_industry(self, description: str) -> Optional[str]:
        return "Technology"
    
    def _detect_remote(self, description: str) -> bool:
        remote_keywords = ["remote", "work from home"]
        return any(kw in description.lower() for kw in remote_keywords)
    
    def _calculate_quality(self, skills, soft_skills, level, salary, location) -> float:
        score = 0.0
        if len(skills) > 0: score += 0.25
        if len(soft_skills) > 0: score += 0.20
        if level != "Middle": score += 0.15
        if salary is not None: score += 0.20
        if location is not None: score += 0.20
        return min(score, 1.0)
    
    def _load_skills_db(self) -> List[str]:
        return ["Python", "JavaScript", "Java", "Django", "Flask", "React", 
                "PostgreSQL", "Docker", "Kubernetes", "AWS", "Git"]
    
    def _load_soft_skills(self) -> List[str]:
        return ["Communication", "Teamwork", "Leadership", "Problem solving"]
    
    def _load_level_keywords(self):
        return {
            JobLevel.JUNIOR: ["junior", "entry-level"],
            JobLevel.MIDDLE: ["middle", "experienced"],
            JobLevel.SENIOR: ["senior", "lead"],
            JobLevel.LEAD: ["lead engineer"],
        }
    
    def _load_locations(self) -> Dict[str, str]:
        return {
            "Moscow": "RU|Moscow",
            "New York": "US|NY",
            "London": "UK|LND",
        }
