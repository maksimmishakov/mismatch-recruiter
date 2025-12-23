"""Custom scoring engine for candidate evaluation."""
import json
from datetime import datetime

class ScoringEngine:
    """Configurable scoring system for candidate matching."""
    
    def __init__(self, company_id=None):
        """Initialize scoring engine with optional company-specific weights."""
        self.company_id = company_id
        self.default_weights = {
            'experience': 0.30,
            'skills_match': 0.40,
            'culture_fit': 0.20,
            'education': 0.10
        }
        self.company_weights = self._load_company_weights(company_id) if company_id else self.default_weights
    
    def _load_company_weights(self, company_id):
        """Load company-specific weights from storage."""
        try:
            # In production, load from database
            return self.default_weights
        except:
            return self.default_weights
    
    def configure_weights(self, weights):
        """Configure custom scoring weights for a company."""
        if not isinstance(weights, dict):
            raise ValueError('Weights must be a dictionary')
        
        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError('Weights must sum to 1.0')
        
        self.company_weights = weights
        return {'success': True, 'weights': weights}
    
    def calculate_experience_score(self, candidate_experience):
        """Calculate score based on years of experience."""
        if not candidate_experience:
            return 0.0
        
        years = candidate_experience if isinstance(candidate_experience, (int, float)) else 0
        
        if years >= 10:
            return 100.0
        elif years >= 5:
            return 80.0 + (years - 5) * 4
        elif years >= 2:
            return 60.0 + (years - 2) * 5
        elif years >= 1:
            return 40.0 + (years - 1) * 20
        else:
            return max(20.0, years * 40)
    
    def calculate_skills_match_score(self, required_skills, candidate_skills):
        """Calculate score based on skills match."""
        if not required_skills or not candidate_skills:
            return 0.0
        
        required_set = set(s.lower() for s in required_skills) if isinstance(required_skills, list) else set()
        candidate_set = set(s.lower() for s in candidate_skills) if isinstance(candidate_skills, list) else set()
        
        if not required_set:
            return 0.0
        
        matches = len(required_set & candidate_set)
        return (matches / len(required_set)) * 100.0
    
    def calculate_culture_fit_score(self, position, company_values):
        """Calculate score based on potential culture fit."""
        # Simplified: score based on position level
        position_scores = {
            'junior': 60.0,
            'senior': 75.0,
            'lead': 85.0,
            'manager': 80.0
        }
        return position_scores.get(position.lower() if position else '', 70.0)
    
    def calculate_education_score(self, education_level):
        """Calculate score based on education level."""
        education_scores = {
            'phd': 100.0,
            'masters': 90.0,
            'bachelors': 80.0,
            'diploma': 60.0,
            'high school': 40.0,
            'other': 50.0
        }
        return education_scores.get(education_level.lower() if education_level else '', 50.0)
    
    def calculate_overall_score(self, candidate_data):
        """Calculate overall score for a candidate."""
        try:
            experience_score = self.calculate_experience_score(
                candidate_data.get('years_experience', 0)
            )
            
            skills_score = self.calculate_skills_match_score(
                candidate_data.get('required_skills', []),
                candidate_data.get('skills', [])
            )
            
            culture_score = self.calculate_culture_fit_score(
                candidate_data.get('position', ''),
                candidate_data.get('company_values', [])
            )
            
            education_score = self.calculate_education_score(
                candidate_data.get('education', '')
            )
            
            overall_score = (
                experience_score * self.company_weights['experience'] +
                skills_score * self.company_weights['skills_match'] +
                culture_score * self.company_weights['culture_fit'] +
                education_score * self.company_weights['education']
            )
            
            return {
                'overall_score': round(overall_score, 2),
                'experience_score': round(experience_score, 2),
                'skills_score': round(skills_score, 2),
                'culture_score': round(culture_score, 2),
                'education_score': round(education_score, 2),
                'weights': self.company_weights
            }
        except Exception as e:
            return {'error': str(e), 'overall_score': 0.0}
    
    def identify_missing_skills(self, required_skills, candidate_skills):
        """Identify skills that candidate is missing."""
        required_set = set(s.lower() for s in required_skills) if isinstance(required_skills, list) else set()
        candidate_set = set(s.lower() for s in candidate_skills) if isinstance(candidate_skills, list) else set()
        
        missing = required_set - candidate_set
        return list(missing)
    
    def get_recommendation(self, overall_score):
        """Generate recommendation based on overall score."""
        if overall_score >= 80:
            return 'STRONG_MATCH'
        elif overall_score >= 60:
            return 'GOOD_MATCH'
        elif overall_score >= 40:
            return 'MODERATE_MATCH'
        else:
            return 'POOR_MATCH'


def calculate_score(candidate_data, company_weights=None):
    """Standalone function to calculate candidate score."""
    engine = ScoringEngine()
    if company_weights:
        engine.configure_weights(company_weights)
    return engine.calculate_overall_score(candidate_data)
