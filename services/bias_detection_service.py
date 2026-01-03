"""Bias Detection Service - AI Fairness & Compliance
Detects and mitigates hiring bias to ensure fair recruitment
Compliance: EU AI Act, GDPR, Equal Employment Opportunity"""
import logging
from typing import List, Dict
from collections import Counter

logger = logging.getLogger(__name__)

class BiasDetectionService:
    """Detect and mitigate bias in hiring process"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def audit_job_hiring(self, job_id: str, applications: List[Dict]) -> Dict:
        """Audit a specific job's hiring process for bias"""
        
        findings = {
            'job_id': job_id,
            'total_applications': len(applications),
            'biases_detected': [],
            'risk_level': 'low',
            'recommendations': []
        }
        
        if len(applications) < 10:
            return findings  # Not enough data
        
        # Check various bias dimensions
        self._check_gender_bias(applications, findings)
        self._check_age_bias(applications, findings)
        self._check_location_bias(applications, findings)
        self._check_education_bias(applications, findings)
        
        # Determine risk level
        findings['risk_level'] = self._calculate_risk_level(findings['biases_detected'])
        
        self.logger.info(f"Bias audit complete for job {job_id}: {len(findings['biases_detected'])} issues found")
        return findings
    
    def _check_gender_bias(self, applications: List[Dict], findings: Dict) -> None:
        """Check if there's gender bias in screening"""
        genders = []
        selected = []
        
        for app in applications:
            gender = app.get('inferred_gender', 'unknown')
            genders.append(gender)
            if app.get('status') in ['interview_scheduled', 'hired']:
                selected.append(gender)
        
        if len(genders) > 10:
            gender_ratio = Counter(genders)
            selected_ratio = Counter(selected) if selected else Counter()
            
            for gender, count in gender_ratio.items():
                selection_rate = selected_ratio.get(gender, 0) / count if count > 0 else 0
                
                if selection_rate < 0.3:  # Less than 30% selected
                    findings['biases_detected'].append({
                        'type': 'gender_bias',
                        'gender': gender,
                        'selection_rate': round(selection_rate, 2),
                        'severity': 'high' if selection_rate < 0.1 else 'medium'
                    })
    
    def _check_age_bias(self, applications: List[Dict], findings: Dict) -> None:
        """Check for age-based discrimination"""
        age_groups = []
        selected = []
        
        for app in applications:
            age = app.get('inferred_age', 0)
            age_group = self._categorize_age(age)
            age_groups.append(age_group)
            if app.get('status') in ['interview_scheduled', 'hired']:
                selected.append(age_group)
        
        if len(age_groups) > 10:
            age_ratio = Counter(age_groups)
            selected_ratio = Counter(selected) if selected else Counter()
            
            for age_group, count in age_ratio.items():
                selection_rate = selected_ratio.get(age_group, 0) / count if count > 0 else 0
                
                if selection_rate < 0.2:
                    findings['biases_detected'].append({
                        'type': 'age_bias',
                        'age_group': age_group,
                        'selection_rate': round(selection_rate, 2),
                        'severity': 'high'
                    })
    
    def _check_location_bias(self, applications: List[Dict], findings: Dict) -> None:
        """Check if candidates from certain locations are disadvantaged"""
        locations = []
        selected = []
        
        for app in applications:
            location = app.get('location', 'unknown')
            locations.append(location)
            if app.get('status') in ['interview_scheduled', 'hired']:
                selected.append(location)
        
        location_ratio = Counter(locations)
        selected_ratio = Counter(selected) if selected else Counter()
        
        for location, count in location_ratio.items():
            selection_rate = selected_ratio.get(location, 0) / count if count > 0 else 0
            
            if selection_rate < 0.15:
                findings['biases_detected'].append({
                    'type': 'location_bias',
                    'location': location,
                    'selection_rate': round(selection_rate, 2),
                    'severity': 'medium'
                })
    
    def _check_education_bias(self, applications: List[Dict], findings: Dict) -> None:
        """Check if candidates with certain education are favored/disfavored"""
        education_levels = []
        selected = []
        
        for app in applications:
            edu = app.get('education_level', 'unknown')
            education_levels.append(edu)
            if app.get('status') in ['interview_scheduled', 'hired']:
                selected.append(edu)
        
        edu_ratio = Counter(education_levels)
        selected_ratio = Counter(selected) if selected else Counter()
        
        for edu, count in edu_ratio.items():
            selection_rate = selected_ratio.get(edu, 0) / count if count > 0 else 0
            
            if selection_rate < 0.15:
                findings['biases_detected'].append({
                    'type': 'education_bias',
                    'education_level': edu,
                    'selection_rate': round(selection_rate, 2),
                    'severity': 'low'
                })
    
    def _categorize_age(self, age: int) -> str:
        """Categorize age into groups"""
        if age < 25:
            return 'under_25'
        elif age < 35:
            return '25_34'
        elif age < 45:
            return '35_44'
        elif age < 55:
            return '45_54'
        else:
            return 'over_55'
    
    def _calculate_risk_level(self, biases: List[Dict]) -> str:
        """Determine overall risk level"""
        if not biases:
            return 'low'
        
        high_severity = sum(1 for b in biases if b.get('severity') == 'high')
        
        if high_severity >= 2:
            return 'critical'
        elif high_severity == 1:
            return 'high'
        else:
            return 'medium'
    
    def blind_screen_applications(self, applications: List[Dict]) -> List[Dict]:
        """Return applications with personal info hidden for bias-free screening"""
        blind_apps = []
        
        for app in applications:
            blind_app = {
                'application_id': app.get('id'),
                'match_score': app.get('match_score'),
                'experience_years': app.get('experience_years'),
                'skills': app.get('skills'),
                'match_reasons': app.get('match_reasons')
                # Hidden: name, gender, age, location, university, etc.
            }
            blind_apps.append(blind_app)
        
        return blind_apps
    
    def get_recommendations(self, findings: Dict) -> List[str]:
        """Generate recommendations to mitigate bias"""
        recs = []
        
        if findings['biases_detected']:
            recs.append('Implement blind screening process (hide names, age, gender)')
            recs.append('Review job description for biased language')
            recs.append('Ensure diverse hiring panel')
            recs.append('Use structured interviews with standardized questions')
            recs.append('Document hiring decisions with clear justifications')
        else:
            recs.append('Continue current fair practices')
        
        return recs

bias_detector = BiasDetectionService()
