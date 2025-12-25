"""Извлечение и нормализация технических скиллов из резюме."""

import re
from typing import List, Dict
from app.logger import get_logger

logger = get_logger("skill_extractor")

# Полная база технических скиллов
TECH_SKILLS_DB = {
    # Языки программирования
    'python': {'category': 'language', 'level': 3, 'popularity': 95},
    'javascript': {'category': 'language', 'level': 3, 'popularity': 95},
    'java': {'category': 'language', 'level': 3, 'popularity': 90},
    'typescript': {'category': 'language', 'level': 3, 'popularity': 85},
    'golang': {'category': 'language', 'level': 2, 'popularity': 70},
    'rust': {'category': 'language', 'level': 2, 'popularity': 65},
    'cpp': {'category': 'language', 'level': 2, 'popularity': 75},
    'csharp': {'category': 'language', 'level': 2, 'popularity': 80},
    'php': {'category': 'language', 'level': 2, 'popularity': 70},
    'kotlin': {'category': 'language', 'level': 1, 'popularity': 60},
    
    # Фреймворки Python
    'django': {'category': 'framework', 'parent': 'python', 'level': 3, 'popularity': 85},
    'flask': {'category': 'framework', 'parent': 'python', 'level': 3, 'popularity': 80},
    'fastapi': {'category': 'framework', 'parent': 'python', 'level': 2, 'popularity': 75},
    'celery': {'category': 'framework', 'parent': 'python', 'level': 2, 'popularity': 70},
    'sqlalchemy': {'category': 'framework', 'parent': 'python', 'level': 2, 'popularity': 75},
    
    # Фреймворки JavaScript
    'react': {'category': 'framework', 'parent': 'javascript', 'level': 3, 'popularity': 95},
    'vue': {'category': 'framework', 'parent': 'javascript', 'level': 3, 'popularity': 80},
    'angular': {'category': 'framework', 'parent': 'javascript', 'level': 3, 'popularity': 75},
    'nodejs': {'category': 'framework', 'parent': 'javascript', 'level': 3, 'popularity': 90},
    'express': {'category': 'framework', 'parent': 'javascript', 'level': 2, 'popularity': 85},
    'nextjs': {'category': 'framework', 'parent': 'javascript', 'level': 2, 'popularity': 80},
    
    # Базы данных
    'postgresql': {'category': 'database', 'level': 3, 'popularity': 85},
    'mysql': {'category': 'database', 'level': 3, 'popularity': 80},
    'mongodb': {'category': 'database', 'level': 3, 'popularity': 85},
    'redis': {'category': 'database', 'level': 2, 'popularity': 80},
    'elasticsearch': {'category': 'database', 'level': 2, 'popularity': 75},
    'dynamodb': {'category': 'database', 'level': 1, 'popularity': 70},
    'cassandra': {'category': 'database', 'level': 1, 'popularity': 60},
    
    # DevOps & Cloud
    'docker': {'category': 'devops', 'level': 3, 'popularity': 95},
    'kubernetes': {'category': 'devops', 'level': 2, 'popularity': 85},
    'jenkins': {'category': 'devops', 'level': 2, 'popularity': 75},
    'gitlab': {'category': 'devops', 'level': 2, 'popularity': 75},
    'github': {'category': 'devops', 'level': 3, 'popularity': 95},
    
    # Cloud providers
    'aws': {'category': 'cloud', 'level': 3, 'popularity': 95},
    'gcp': {'category': 'cloud', 'level': 2, 'popularity': 80},
    'azure': {'category': 'cloud', 'level': 2, 'popularity': 75},
    'heroku': {'category': 'cloud', 'level': 2, 'popularity': 65},
    
    # Tools
    'git': {'category': 'tool', 'level': 3, 'popularity': 100},
    'linux': {'category': 'tool', 'level': 2, 'popularity': 80},
    'nginx': {'category': 'tool', 'level': 2, 'popularity': 75},
    'apache': {'category': 'tool', 'level': 1, 'popularity': 60},
}

class SkillExtractor:
    """Извлечение скиллов из текста резюме."""
    
    def __init__(self):
        self.skills_db = TECH_SKILLS_DB
        logger.info("SkillExtractor initialized")
    
    def extract(self, text: str) -> List[Dict]:
        """
        Извлечь скиллы из текста.
        
        Returns:
        [
            {
                'name': 'Python',
                'category': 'language',
                'level': 3,
                'popularity': 95,
                'confidence': 0.95,
                'mentions': 5
            }
        ]
        """
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = {}
        
        # Поиск известных скиллов
        for skill_name, metadata in self.skills_db.items():
            # Regex с word boundaries
            pattern = r'\b' + re.escape(skill_name) + r'\b'
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            
            if matches:
                confidence = min(len(matches) * 0.2, 1.0)
                found_skills[skill_name] = {
                    'name': skill_name.title(),
                    'category': metadata['category'],
                    'level': metadata.get('level', 2),
                    'popularity': metadata.get('popularity', 50),
                    'confidence': confidence,
                    'mentions': len(matches)
                }
        
        # Сортировка по уверенности и количеству упоминаний
        sorted_skills = sorted(
            found_skills.values(),
            key=lambda x: (x['confidence'] * x['mentions'], x['popularity']),
            reverse=True
        )
        
        logger.info(f"Extracted {len(sorted_skills)} skills from text")
        return sorted_skills
    
    def extract_by_category(self, text: str, category: str) -> List[Dict]:
        """Извлечь скиллы определённой категории."""
        all_skills = self.extract(text)
        return [s for s in all_skills if s['category'] == category]
