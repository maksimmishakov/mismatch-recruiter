from typing import List, Dict
from enum import Enum

class SkillCategory(Enum):
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    DATABASE = "database"
    DEVOPS = "devops"
    SOFT_SKILL = "soft_skill"

class SkillExtractor:
    def __init__(self):
        self.skill_taxonomy = self._build_taxonomy()
    
    def extract_and_categorize(self, text: str) -> List[Dict]:
        found_skills = []
        text_lower = text.lower()
        
        for skill, metadata in self.skill_taxonomy.items():
            if skill.lower() in text_lower:
                found_skills.append({
                    "name": skill,
                    "category": metadata["category"],
                    "confidence": 0.85,
                    "level": metadata.get("level", "intermediate")
                })
        
        return sorted(found_skills, key=lambda x: x["confidence"], reverse=True)[:20]
    
    def _build_taxonomy(self) -> Dict:
        return {
            "Python": {"category": SkillCategory.LANGUAGE.value, "level": "advanced"},
            "JavaScript": {"category": SkillCategory.LANGUAGE.value, "level": "advanced"},
            "Java": {"category": SkillCategory.LANGUAGE.value, "level": "intermediate"},
            "TypeScript": {"category": SkillCategory.LANGUAGE.value, "level": "intermediate"},
            "Go": {"category": SkillCategory.LANGUAGE.value, "level": "intermediate"},
            
            "Django": {"category": SkillCategory.FRAMEWORK.value, "level": "advanced"},
            "FastAPI": {"category": SkillCategory.FRAMEWORK.value, "level": "advanced"},
            "Flask": {"category": SkillCategory.FRAMEWORK.value, "level": "advanced"},
            "React": {"category": SkillCategory.FRAMEWORK.value, "level": "advanced"},
            "Vue": {"category": SkillCategory.FRAMEWORK.value, "level": "intermediate"},
            "Node.js": {"category": SkillCategory.FRAMEWORK.value, "level": "intermediate"},
            
            "PostgreSQL": {"category": SkillCategory.DATABASE.value, "level": "advanced"},
            "MySQL": {"category": SkillCategory.DATABASE.value, "level": "intermediate"},
            "MongoDB": {"category": SkillCategory.DATABASE.value, "level": "intermediate"},
            "Redis": {"category": SkillCategory.DATABASE.value, "level": "intermediate"},
            
            "Docker": {"category": SkillCategory.DEVOPS.value, "level": "advanced"},
            "Kubernetes": {"category": SkillCategory.DEVOPS.value, "level": "intermediate"},
            "AWS": {"category": SkillCategory.DEVOPS.value, "level": "advanced"},
            "GCP": {"category": SkillCategory.DEVOPS.value, "level": "intermediate"},
            "Jenkins": {"category": SkillCategory.DEVOPS.value, "level": "intermediate"},
        }
