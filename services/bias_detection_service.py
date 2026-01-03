import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from datetime import datetime
from typing import Dict, List

class BiasDetectionService:
    """Advanced bias detection for EU AI Act compliance"""
   
    BIAS_TYPES = {
        'gender': {'threshold': 0.15, 'weight': 0.25},
        'age': {'threshold': 0.20, 'weight': 0.20},
        'disability': {'threshold': 0.25, 'weight': 0.15},
        'location': {'threshold': 0.20, 'weight': 0.10}
    }
   
    def comprehensive_audit(self, hiring_data: Dict) -> Dict:
        """Comprehensive bias audit for compliance"""
        try:
            audit_results = {}
            
            for bias_type in self.BIAS_TYPES.keys():
                audit_results[bias_type] = self._detect_bias(bias_type, hiring_data)
            
            fairness_scores = [
                1 - r.get('bias_level', 0) 
                for r in audit_results.values()
            ]
            overall_score = np.mean(fairness_scores) if fairness_scores else 0
            
            compliance_status = self._determine_compliance(overall_score, audit_results)
            
            return {
                'overall_fairness_score': float(overall_score),
                'compliance_status': compliance_status,
                'detailed_results': audit_results,
                'critical_issues': self._find_critical_issues(audit_results),
                'recommendations': self._generate_recommendations(audit_results),
                'audit_timestamp': datetime.now().isoformat(),
                'eu_ai_act_compliant': compliance_status == 'COMPLIANT'
            }
        except Exception as e:
            return {
                'error': str(e),
                'compliance_status': 'ERROR',
                'eu_ai_act_compliant': False
            }
   
    def _detect_bias(self, bias_type: str, hiring_data: Dict) -> Dict:
        """Detect specific type of bias"""
        if bias_type == 'gender':
            return self._detect_gender_bias(hiring_data)
        elif bias_type == 'age':
            return self._detect_age_bias(hiring_data)
        elif bias_type == 'disability':
            return self._detect_disability_bias(hiring_data)
        elif bias_type == 'location':
            return self._detect_location_bias(hiring_data)
        return {'bias_level': 0, 'is_biased': False}
   
    def _detect_gender_bias(self, hiring_data: Dict) -> Dict:
        """Detect gender discrimination"""
        candidates = hiring_data.get('candidates', [])
        if len(candidates) < 2:
            return {'bias_level': 0, 'is_biased': False}
        
        male_count = sum(1 for c in candidates if c.get('gender') == 'male' and c.get('hired'))
        female_count = sum(1 for c in candidates if c.get('gender') == 'female' and c.get('hired'))
        male_total = sum(1 for c in candidates if c.get('gender') == 'male')
        female_total = sum(1 for c in candidates if c.get('gender') == 'female')
        
        male_rate = male_count / male_total if male_total > 0 else 0
        female_rate = female_count / female_total if female_total > 0 else 0
        
        bias_level = abs(male_rate - female_rate)
        
        return {
            'bias_level': bias_level,
            'is_biased': bias_level > self.BIAS_TYPES['gender']['threshold'],
            'male_hire_rate': male_rate,
            'female_hire_rate': female_rate,
            'recommendation': 'Review hiring process' if bias_level > 0.1 else 'No significant bias detected'
        }
   
    def _detect_age_bias(self, hiring_data: Dict) -> Dict:
        """Detect age discrimination"""
        candidates = hiring_data.get('candidates', [])
        if len(candidates) < 2:
            return {'bias_level': 0, 'is_biased': False}
        
        ages = [c.get('age', 35) for c in candidates]
        hired_ages = [c.get('age', 35) for c in candidates if c.get('hired')]
        
        if not hired_ages:
            return {'bias_level': 0, 'is_biased': False}
        
        avg_all = np.mean(ages)
        avg_hired = np.mean(hired_ages)
        
        bias_level = abs(avg_all - avg_hired) / avg_all if avg_all > 0 else 0
        
        return {
            'bias_level': min(bias_level, 1.0),
            'is_biased': bias_level > self.BIAS_TYPES['age']['threshold'],
            'avg_candidate_age': float(avg_all),
            'avg_hired_age': float(avg_hired),
            'recommendation': 'Consider blind resume screening' if bias_level > 0.1 else 'No significant age bias'
        }
   
    def _detect_disability_bias(self, hiring_data: Dict) -> Dict:
        """Detect disability discrimination"""
        candidates = hiring_data.get('candidates', [])
        if len(candidates) < 2:
            return {'bias_level': 0, 'is_biased': False}
        
        with_disability = sum(1 for c in candidates if c.get('disability', False) and c.get('hired'))
        without_disability = sum(1 for c in candidates if not c.get('disability', False) and c.get('hired'))
        with_total = sum(1 for c in candidates if c.get('disability', False))
        without_total = sum(1 for c in candidates if not c.get('disability', False))
        
        with_rate = with_disability / with_total if with_total > 0 else 0
        without_rate = without_disability / without_total if without_total > 0 else 0
        
        bias_level = abs(with_rate - without_rate)
        
        return {
            'bias_level': bias_level,
            'is_biased': bias_level > self.BIAS_TYPES['disability']['threshold'],
            'with_disability_hire_rate': with_rate,
            'without_disability_hire_rate': without_rate,
            'recommendation': 'Review accessibility and accommodation practices' if bias_level > 0.1 else 'No significant disability bias'
        }
   
    def _detect_location_bias(self, hiring_data: Dict) -> Dict:
        """Detect location-based discrimination"""
        candidates = hiring_data.get('candidates', [])
        if len(candidates) < 2:
            return {'bias_level': 0, 'is_biased': False}
        
        locations = {}
        for candidate in candidates:
            loc = candidate.get('location', 'unknown')
            if loc not in locations:
                locations[loc] = {'total': 0, 'hired': 0}
            locations[loc]['total'] += 1
            if candidate.get('hired'):
                locations[loc]['hired'] += 1
        
        rates = [locations[loc]['hired'] / locations[loc]['total'] 
                for loc in locations if locations[loc]['total'] > 0]
        
        if not rates:
            return {'bias_level': 0, 'is_biased': False}
        
        bias_level = max(rates) - min(rates) if len(rates) > 1 else 0
        
        return {
            'bias_level': bias_level,
            'is_biased': bias_level > self.BIAS_TYPES['location']['threshold'],
            'location_rates': {loc: locations[loc]['hired']/locations[loc]['total'] for loc in locations if locations[loc]['total'] > 0},
            'recommendation': 'Evaluate location-based hiring patterns' if bias_level > 0.1 else 'No significant location bias'
        }
   
    def _determine_compliance(self, fairness_score: float, results: Dict) -> str:
        """Determine EU AI Act compliance status"""
        biased_count = sum(1 for r in results.values() if r.get('is_biased'))
        
        if fairness_score >= 0.85 and biased_count == 0:
            return 'COMPLIANT'
        elif fairness_score >= 0.70:
            return 'AT_RISK'
        else:
            return 'NON_COMPLIANT'
   
    def _find_critical_issues(self, results: Dict) -> List[Dict]:
        """Find critical compliance issues"""
        issues = []
        for bias_type, result in results.items():
            if result.get('is_biased'):
                issues.append({
                    'type': bias_type,
                    'severity': 'CRITICAL' if result.get('bias_level', 0) > 0.25 else 'HIGH',
                    'bias_level': result.get('bias_level', 0),
                    'recommendation': result.get('recommendation', '')
                })
        return sorted(issues, key=lambda x: x['bias_level'], reverse=True)
   
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        for bias_type, result in results.items():
            if result.get('is_biased') and result.get('recommendation'):
                recommendations.append(result['recommendation'])
        return recommendations
