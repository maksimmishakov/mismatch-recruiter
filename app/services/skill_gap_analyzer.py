"""Skill Gap Analyzer - Analyze and recommend skill development"""

import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class SkillGapAnalyzer:
    """Service for analyzing skill gaps and recommending training"""
    
    def __init__(self):
        """Initialize the skill gap analyzer"""
        self.skill_categories = {
            'technical': ['Python', 'JavaScript', 'SQL', 'Docker', 'Kubernetes'],
            'soft_skills': ['Communication', 'Leadership', 'Problem-solving', 'Time Management'],
            'business': ['Project Management', 'Sales', 'Marketing', 'Finance']
        }
        logger.info("SkillGapAnalyzer initialized")
    
    def analyze_gaps(self, current_skills: List[str], target_role: str) -> Optional[Dict]:
        """Analyze skill gaps for a candidate
        
        Args:
            current_skills: List of skills the candidate currently has
            target_role: Target job role
            
        Returns:
            Dictionary with gap analysis or None if error
        """
        try:
            if not current_skills or not target_role:
                return None
            
            # Get required skills for target role
            required_skills = self._get_required_skills(target_role)
            if not required_skills:
                return None
            
            # Calculate gaps
            current_set = set(s.lower() for s in current_skills)
            required_set = set(s.lower() for s in required_skills)
            
            gaps = required_set - current_set
            matched = current_set & required_set
            
            return {
                'matched_skills': list(matched),
                'skill_gaps': list(gaps),
                'coverage_percentage': (len(matched) / len(required_set) * 100) if required_set else 0,
                'priority_skills': self._prioritize_gaps(gaps, target_role),
                'recommendations': self._get_recommendations(gaps, target_role)
            }
        except Exception as e:
            logger.error(f"Error analyzing skill gaps: {e}")
            return None
    
    def _get_required_skills(self, role: str) -> List[str]:
        """Get required skills for a role"""
        role_skills = {
            'software engineer': ['Python', 'JavaScript', 'SQL', 'Docker', 'Git', 'Problem-solving'],
            'data scientist': ['Python', 'SQL', 'Statistics', 'Machine Learning', 'Data Visualization'],
            'product manager': ['Project Management', 'Communication', 'Analytics', 'Leadership'],
            'devops engineer': ['Docker', 'Kubernetes', 'CI/CD', 'Linux', 'Cloud Platforms'],
        }
        return role_skills.get(role.lower(), [])
    
    def _prioritize_gaps(self, gaps: set, role: str) -> List[str]:
        """Prioritize which skills to learn first"""
        if not gaps:
            return []
        
        # Simplified prioritization - technical skills first
        priority_order = ['Python', 'SQL', 'Docker', 'Kubernetes', 'Linux']
        prioritized = [skill for skill in priority_order if skill.lower() in gaps]
        
        # Add remaining gaps
        remaining = [skill for skill in gaps if skill.lower() not in [s.lower() for s in prioritized]]
        prioritized.extend(remaining)
        
        return prioritized[:5]  # Return top 5
    
    def _get_recommendations(self, gaps: set, role: str) -> List[Dict]:
        """Get learning recommendations for gaps"""
        recommendations = []
        
        gap_resources = {
            'python': {'type': 'Course', 'resource': 'Python for Everybody, Real Python'},
            'sql': {'type': 'Course', 'resource': 'SQL Basics, Mode Analytics'},
            'docker': {'type': 'Course', 'resource': 'Docker Mastery'},
            'kubernetes': {'type': 'Course', 'resource': 'Kubernetes Bootcamp'},
            'machine learning': {'type': 'Course', 'resource': 'Andrew Ng ML Course'},
            'communication': {'type': 'Workshop', 'resource': 'Toastmasters, Public Speaking'},
        }
        
        for gap in list(gaps)[:5]:
            resource_info = gap_resources.get(gap.lower())
            if resource_info:
                recommendations.append({
                    'skill': gap,
                    'type': resource_info['type'],
                    'resource': resource_info['resource'],
                    'estimated_hours': 40 if resource_info['type'] == 'Course' else 20
                })
        
        return recommendations
    
    def get_learning_path(self, gaps: List[str]) -> Optional[List[Dict]]:
        """Create a structured learning path"""
        try:
            if not gaps:
                return None
            
            path = []
            for i, skill in enumerate(gaps[:5], 1):
                path.append({
                    'phase': i,
                    'skill': skill,
                    'duration_weeks': 4,
                    'resources': self._get_recommendations({skill}, '').copy(),
                    'assessment': f'Complete project or certification for {skill}'
                })
            
            return path
        except Exception as e:
            logger.error(f"Error creating learning path: {e}")
            return None
