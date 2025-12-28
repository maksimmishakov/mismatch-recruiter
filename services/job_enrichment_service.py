"""Сервис обогащения описаний вакансий."""

import re
from typing import Dict, Any, List
from datetime import datetime
from app.logger import get_logger
from app.services.parsing.skill_extractor import SkillExtractor

logger = get_logger("job_enrichment")

class JobEnrichmentService:
    """Обогащение вакансий структурированными данными."""
    
    def __init__(self):
        self.skill_extractor = SkillExtractor()
    
    def enrich(self, job_title: str, job_description: str, requirements: str) -> Dict[str, Any]:
        """
        Полное обогащение вакансии.
        
        Args:
            job_title: Название должности
            job_description: Описание работы
            requirements: Требования
        
        Returns:
            {
                'required_skills': [...],
                'seniority_level': 'mid',
                'difficulty_score': 0.65,
                'benefits': ['remote', 'flexible_hours'],
                'salary_min': 100000,
                'salary_max': 150000,
                'enrichment_status': 'success'
            }
        """
        try:
            combined_text = f"{job_title} {job_description} {requirements}"
            
            result = {
                'required_skills': self._extract_required_skills(requirements),
                'seniority_level': self._identify_seniority(job_description),
                'difficulty_score': self._calculate_difficulty(requirements),
                'benefits': self._extract_benefits(job_description),
                'salary_min': self._extract_salary_min(job_description),
                'salary_max': self._extract_salary_max(job_description),
                'enrichment_status': 'success',
                'enriched_at': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Job enriched successfully: {len(result['required_skills'])} skills, "
                       f"level={result['seniority_level']}, difficulty={result['difficulty_score']:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Job enrichment error: {e}", exc_info=True)
            return {
                'required_skills': [],
                'seniority_level': 'mid',
                'difficulty_score': 0.5,
                'benefits': [],
                'salary_min': None,
                'salary_max': None,
                'enrichment_status': 'error',
                'error': str(e)
            }
    
    def _extract_required_skills(self, text: str) -> List[Dict]:
        """Извлечь требуемые скиллы из requirements."""
        return self.skill_extractor.extract(text)
    
    def _identify_seniority(self, text: str) -> str:
        """Определить уровень senior'ти."""
        seniority_patterns = {
            'lead': [
                r'(?:lead|principal|architect|staff)',
                r'(?:team lead|tech lead)',
                r'(?:10\+|15\+|20\+)\s*(?:years?|yrs?)',
            ],
            'senior': [
                r'(?:senior|старший)',
                r'(?:8\+|9\+|10\+)\s*(?:years?|yrs?)',
                r'(?:опыт от 8|опыт от 10)',
            ],
            'mid': [
                r'(?:middle|mid|intermediate)',
                r'(?:3\+|4\+|5\+|6\+|7\+)\s*(?:years?|yrs?)',
                r'(?:опыт от 3|опыт от 5)',
            ],
            'junior': [
                r'(?:junior|начинающ|entry.?level)',
                r'(?:0\+|1\+|2\+)\s*(?:years?|yrs?)',
            ],
        }
        
        text_lower = text.lower()
        
        for level in ['lead', 'senior', 'mid', 'junior']:
            patterns = seniority_patterns[level]
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return level
        
        return 'mid'
    
    def _calculate_difficulty(self, requirements: str) -> float:
        """
        Рассчитать сложность позиции (0-1).
        
        Факторы:
        - Количество требований
        - Редкость требуемых скиллов
        - Специализированные tech stack
        """
        score = 0.3
        
        skills = self.skill_extractor.extract(requirements)
        skill_count_score = min(len(skills) / 15, 0.3)
        
        rare_skills = {
            'kubernetes': 0.15,
            'rust': 0.15,
            'machine learning': 0.15,
            'deep learning': 0.15,
            'data science': 0.1,
            'distributed systems': 0.1,
            'microservices': 0.1,
        }
        
        rare_score = 0.0
        req_lower = requirements.lower()
        for skill, weight in rare_skills.items():
            if skill in req_lower:
                rare_score += weight
        
        rare_score = min(rare_score, 0.3)
        
        combined_score = 0.1 if len(skills) >= 10 else 0.0
        
        total_score = score + skill_count_score + rare_score + combined_score
        return min(total_score, 1.0)
    
    def _extract_benefits(self, text: str) -> List[str]:
        """Извлечь предлагаемые бенефиты."""
        benefits_patterns = {
            'remote': [
                r'(?:remote|работа из дома|work from home)',
                r'(?:fully remote|100% remote)',
            ],
            'flexible_hours': [
                r'(?:flexible|гибкий)',
                r'(?:flexible working hours)',
            ],
            'relocation': [
                r'(?:relocation|переезд|relocation package)',
                r'(?:visa sponsorship)',
            ],
            'health_insurance': [
                r'(?:health insurance|страховка|medical)',
                r'(?:health benefits)',
            ],
            'stock_options': [
                r'(?:stock options|опционы|equity)',
                r'(?:stock grants)',
            ],
            'unlimited_pto': [
                r'(?:unlimited pto|unlimited vacation)',
                r'(?:unlimited time off)',
            ],
            'conference_budget': [
                r'(?:conference|conferences|обучение)',
                r'(?:professional development)',
                r'(?:learning budget)',
            ],
            'wellness': [
                r'(?:wellness|gym|fitness)',
                r'(?:mental health)',
            ],
            'parental_leave': [
                r'(?:parental leave|paternity|maternity)',
            ],
            'bonus': [
                r'(?:bonus|bonuses|performance bonus)',
                r'(?:annual bonus)',
            ],
        }
        
        found_benefits = []
        text_lower = text.lower()
        
        for benefit, patterns in benefits_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    found_benefits.append(benefit)
                    break
        
        return found_benefits
    
    def _extract_salary_min(self, text: str) -> float | None:
        """Извлечь минимальную зарплату."""
        patterns = [
            r'\$(\d{3,})\s*(?:k|K|\d{3})?',
            r'(\d{3,})\s*(?:usd|USD)',
            r'from\s*\$(\d{3,})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    salary = int(matches[0])
                    if salary < 1000:
                        salary = salary * 1000
                    return float(salary)
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def _extract_salary_max(self, text: str) -> float | None:
        """Извлечь максимальную зарплату."""
        patterns = [
            r'(\d{3,})\s*(?:k|K)\s*$',
            r'to\s*\$(\d{3,})',
            r'-\s*\$(\d{3,})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    salary = int(matches[-1])
                    if salary < 1000:
                        salary = salary * 1000
                    return float(salary)
                except (ValueError, IndexError):
                    continue
        
        return None
