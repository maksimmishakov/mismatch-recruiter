"""Salary Predictor Service - ML-based salary prediction"""

import logging
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


class SalaryPredictor:
    """Service for predicting salaries based on job parameters"""
    
    def __init__(self):
        """Initialize the salary predictor"""
        self.model = None
        self.is_ready = True
        logger.info("SalaryPredictor initialized")
    
    def predict(self, job_data: Dict) -> Optional[Dict]:
        """Predict salary for given job parameters
        
        Args:
            job_data: Dictionary with job parameters (title, level, location, skills, etc.)
            
        Returns:
            Dictionary with predicted salary info or None if prediction fails
        """
        try:
            if not job_data:
                return None
            
            # Extract key parameters
            title = job_data.get('title', '')
            level = job_data.get('level', 'middle')
            location = job_data.get('location', '')
            
            # Basic salary estimation logic
            base_salary = self._get_base_salary(title, level)
            
            if base_salary is None:
                return None
            
            # Adjust based on location
            location_multiplier = self._get_location_multiplier(location)
            predicted_salary = base_salary * location_multiplier
            
            return {
                'min_salary': int(predicted_salary * 0.8),
                'max_salary': int(predicted_salary * 1.2),
                'expected_salary': int(predicted_salary),
                'confidence': 0.75
            }
        except Exception as e:
            logger.error(f"Error predicting salary: {e}")
            return None
    
    def _get_base_salary(self, title: str, level: str) -> Optional[int]:
        """Get base salary for job title and level"""
        salary_map = {
            'junior': 60000,
            'middle': 100000,
            'senior': 150000,
            'lead': 180000,
            'manager': 160000,
        }
        return salary_map.get(level.lower(), 100000)
    
    def _get_location_multiplier(self, location: str) -> float:
        """Get salary multiplier based on location"""
        location_map = {
            'moscow': 1.3,
            'saint_petersburg': 1.2,
            'spb': 1.2,
            'default': 1.0
        }
        return location_map.get(location.lower(), 1.0)
    
    def get_salary_range(self, position_id: str) -> Optional[Dict]:
        """Get salary range for a specific position"""
        try:
            # Placeholder for getting salary data from database
            return None
        except Exception as e:
            logger.error(f"Error getting salary range: {e}")
            return None
