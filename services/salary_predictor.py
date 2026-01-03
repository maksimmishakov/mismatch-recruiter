# services/salary_predictor.py - Salary Prediction Service

import logging
from typing import Dict, List, Optional, Tuple
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class SalaryPredictorService:
    """Service for predicting salary ranges based on job market data."""
    
    # Russian IT salary reference data (in RUB)
    SALARY_RANGES = {
        'junior': {'min': 50000, 'max': 100000, 'avg': 75000},
        'middle': {'min': 100000, 'max': 200000, 'avg': 150000},
        'senior': {'min': 200000, 'max': 400000, 'avg': 300000},
        'lead': {'min': 300000, 'max': 600000, 'avg': 450000},
        'architect': {'min': 400000, 'max': 800000, 'avg': 600000},
    }
    
    SKILL_MULTIPLIERS = {
        'python': 1.1,
        'javascript': 1.1,
        'rust': 1.3,
        'go': 1.2,
        'java': 1.1,
        'kubernetes': 1.2,
        'aws': 1.15,
        'gcp': 1.15,
        'azure': 1.15,
        'machine learning': 1.3,
        'ai': 1.3,
        'nlp': 1.4,
        'deep learning': 1.35,
        'blockchain': 1.25,
    }
    
    EXPERIENCE_MULTIPLIERS = {
        0: 0.6,    # Intern
        1: 0.8,    # Junior
        3: 1.0,    # Middle
        5: 1.2,    # Senior
        8: 1.4,    # Lead
        10: 1.6,   # Architect
    }
    
    LOCATION_MULTIPLIERS = {
        'moscow': 1.3,
        'spb': 1.1,
        'saint-petersburg': 1.1,
        'novosibirsk': 0.8,
        'yekaterinburg': 0.9,
        'russia': 1.0,
        'remote': 1.0,
    }
    
    def __init__(self):
        """Initialize salary predictor service."""
        logger.info("Salary Predictor Service initialized")
    
    def predict_salary(self, 
                      experience_years: int,
                      seniority_level: str,
                      skills: List[str],
                      location: str = 'moscow',
                      industry: str = 'tech') -> Dict[str, float]:
        """Predict salary range based on job parameters.
        
        Args:
            experience_years: Years of professional experience
            seniority_level: Junior, Middle, Senior, Lead, Architect
            skills: List of technical skills
            location: Job location (Moscow, SPb, etc)
            industry: Industry (tech, finance, etc)
            
        Returns:
            Dict with min, max, and average salary predictions
        """
        try:
            # Validate seniority level
            level = seniority_level.lower()
            if level not in self.SALARY_RANGES:
                level = self._determine_level(experience_years)
            
            # Get base salary
            base = self.SALARY_RANGES[level]['avg']
            
            # Apply multipliers
            multiplier = 1.0
            
            # Experience multiplier
            multiplier *= self._get_experience_multiplier(experience_years)
            
            # Skills multiplier
            for skill in skills:
                skill_lower = skill.lower()
                if skill_lower in self.SKILL_MULTIPLIERS:
                    multiplier *= self.SKILL_MULTIPLIERS[skill_lower]
            
            # Location multiplier
            location_lower = location.lower()
            multiplier *= self.LOCATION_MULTIPLIERS.get(location_lower, 1.0)
            
            # Calculate final salary
            predicted_salary = base * multiplier
            
            # Define range (±20%)
            min_salary = predicted_salary * 0.8
            max_salary = predicted_salary * 1.2
            
            return {
                'min': round(min_salary),
                'max': round(max_salary),
                'avg': round(predicted_salary),
                'currency': 'RUB',
                'level': level,
                'multiplier': round(multiplier, 2)
            }
        except Exception as e:
            logger.error(f"Error predicting salary: {e}")
            return {'min': 50000, 'max': 300000, 'avg': 150000, 'currency': 'RUB'}
    
    def predict_salary_for_job(self, job_description: Dict) -> Dict[str, float]:
        """Predict salary from job description.
        
        Args:
            job_description: Dict with job details
            
        Returns:
            Salary prediction
        """
        experience = job_description.get('experience_years', 3)
        level = job_description.get('level', 'middle')
        skills = job_description.get('required_skills', [])
        location = job_description.get('location', 'moscow')
        
        return self.predict_salary(experience, level, skills, location)
    
    def _determine_level(self, years: int) -> str:
        """Determine seniority level from experience.
        
        Args:
            years: Years of experience
            
        Returns:
            Seniority level
        """
        if years < 2:
            return 'junior'
        elif years < 5:
            return 'middle'
        elif years < 8:
            return 'senior'
        elif years < 10:
            return 'lead'
        else:
            return 'architect'
    
    def _get_experience_multiplier(self, years: int) -> float:
        """Get multiplier based on experience.
        
        Args:
            years: Years of experience
            
        Returns:
            Experience multiplier
        """
        for exp_threshold in sorted(self.EXPERIENCE_MULTIPLIERS.keys(), reverse=True):
            if years >= exp_threshold:
                return self.EXPERIENCE_MULTIPLIERS[exp_threshold]
        return self.EXPERIENCE_MULTIPLIERS[0]
    
    def get_market_stats(self, location: str = 'moscow') -> Dict:
        """Get market salary statistics.
        
        Args:
            location: Location to get stats for
            
        Returns:
            Market statistics
        """
        return {
            'location': location,
            'currency': 'RUB',
            'updated': datetime.now().isoformat(),
            'levels': self.SALARY_RANGES,
            'location_multipliers': self.LOCATION_MULTIPLIERS,
        }
    
    def compare_salaries(self, 
                        salary1: Dict,
                        salary2: Dict) -> Dict:
        """Compare two salary predictions.
        
        Args:
            salary1: First salary prediction
            salary2: Second salary prediction
            
        Returns:
            Comparison results
        """
        return {
            'difference': salary2['avg'] - salary1['avg'],
            'percentage_change': ((salary2['avg'] - salary1['avg']) / salary1['avg'] * 100),
            'salary1': salary1,
            'salary2': salary2,
        }


# Global instance
_salary_service = None


def get_salary_service() -> SalaryPredictorService:
    """Get or create salary predictor instance."""
    global _salary_service
    if _salary_service is None:
        _salary_service = SalaryPredictorService()
    return _salary_service
