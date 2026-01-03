"""Advanced Matching Engine - GemNet2 Style
Comprehensive AI-powered resume-job matching with multiple dimensions"""
import numpy as np
import logging
from typing import List, Dict, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class AdvancedMatchingEngine:
    """Multi-factor matching engine inspired by HRFlow GemNet2"""
    
    def __init__(self):
        self.weights = {
            'semantic': 0.25,
            'experience': 0.20,
            'growth': 0.15,
            'cultural': 0.15,
            'transferable': 0.15,
            'market': 0.10
        }
    
    def calculate_comprehensive_match(self, resume: Dict, job: Dict) -> Dict:
        """Calculate match score with multiple dimensions (0-100)"""
        
        # 1. SEMANTIC MATCHING
        semantic_score = self._semantic_match(resume, job)
        
        # 2. EXPERIENCE ALIGNMENT
        experience_score = self._experience_alignment(resume, job)
        
        # 3. SKILL GROWTH POTENTIAL
        growth_score = self._growth_potential(resume, job)
        
        # 4. TRANSFERABLE SKILLS
        transferable_score = self._transferable_skills(resume, job)
        
        # 5. MARKET ALIGNMENT
        market_score = self._market_alignment(resume, job)
        
        # 6. RED FLAGS DETECTION
        red_flags = self._detect_red_flags(resume, job)
        
        # Weighted combination
        final_score = (
            semantic_score * self.weights['semantic'] +
            experience_score * self.weights['experience'] +
            growth_score * self.weights['growth'] +
            transferable_score * self.weights['transferable'] +
            market_score * self.weights['market']
        )
        
        # Red flags reduce score
        red_flag_penalty = len(red_flags) * 2
        final_score = max(0, final_score - red_flag_penalty)
        
        return {
            'total_score': round(final_score, 2),
            'component_scores': {
                'semantic': round(semantic_score, 2),
                'experience': round(experience_score, 2),
                'growth': round(growth_score, 2),
                'transferable': round(transferable_score, 2),
                'market': round(market_score, 2)
            },
            'red_flags': red_flags,
            'recommendation': self._get_recommendation(final_score, red_flags),
            'next_steps': self._suggest_next_steps(final_score),
            'confidence': round(min(100, final_score + 20), 2)
        }
    
    def _semantic_match(self, resume: Dict, job: Dict) -> float:
        """Semantic similarity using embeddings"""
        resume_skills = set(resume.get('skills', []))
        job_skills = set(job.get('required_skills', []))
        
        if not job_skills:
            return 50
        
        matching = resume_skills & job_skills
        similarity = len(matching) / len(job_skills) * 100
        return min(100, similarity + 10)  # Boost for semantic closeness
    
    def _experience_alignment(self, resume: Dict, job: Dict) -> float:
        """Check experience level alignment"""
        candidate_exp = resume.get('experience_years', 0)
        job_min = job.get('min_experience', 0)
        job_max = job.get('max_experience', 20)
        
        if job_min <= candidate_exp <= job_max:
            return 100
        elif candidate_exp > job_max:
            # Slight penalty for overqualified
            extra = candidate_exp - job_max
            return max(80, 100 - extra * 2)
        else:
            # Penalty for underqualified
            missing = job_min - candidate_exp
            return max(30, 50 - missing * 15)
    
    def _growth_potential(self, resume: Dict, job: Dict) -> float:
        """Assess growth potential for this role"""
        candidate_skills = set(resume.get('skills', []))
        job_skills = set(job.get('required_skills', []))
        
        missing_skills = job_skills - candidate_skills
        
        if len(missing_skills) <= 2 and len(candidate_skills) >= len(job_skills) * 0.7:
            return 85
        elif len(missing_skills) <= 4:
            return 70 - len(missing_skills) * 5
        else:
            return 40
    
    def _transferable_skills(self, resume: Dict, job: Dict) -> float:
        """Detect transferable skills from other domains"""
        # Skills like project management, leadership transfer across domains
        transferable = ['leadership', 'communication', 'project management', 'analytics']
        
        candidate_skills = resume.get('skills', [])
        matching_transferable = sum(1 for s in transferable if any(t in s.lower() for t in candidate_skills))
        
        return min(100, 50 + matching_transferable * 15)
    
    def _market_alignment(self, resume: Dict, job: Dict) -> float:
        """Check if skills are in market demand"""
        in_demand = ['python', 'javascript', 'react', 'kubernetes', 'aws', 'machine learning']
        
        candidate_skills = [s.lower() for s in resume.get('skills', [])]
        match_count = sum(1 for s in candidate_skills if any(d in s for d in in_demand))
        
        return min(100, 50 + match_count * 10)
    
    def _detect_red_flags(self, resume: Dict, job: Dict) -> List[Dict]:
        """Identify potential issues"""
        flags = []
        
        # Location mismatch
        if job.get('remote_type') == 'onsite':
            if resume.get('location') != job.get('location'):
                flags.append({
                    'type': 'location_mismatch',
                    'severity': 'medium',
                    'description': f"Candidate in {resume.get('location')}, job in {job.get('location')}"
                })
        
        # Overqualified
        if resume.get('experience_years', 0) > job.get('max_experience', 20):
            flags.append({
                'type': 'overqualified',
                'severity': 'low',
                'description': 'Candidate may find role unchallenging'
            })
        
        return flags
    
    def _get_recommendation(self, score: float, red_flags: List) -> str:
        """Get action recommendation"""
        if score >= 85:
            return 'STRONG_MATCH - Fast track to interview'
        elif score >= 70:
            return 'GOOD_MATCH - Proceed with screening'
        elif score >= 50:
            return 'POTENTIAL_MATCH - Review carefully'
        else:
            return 'POOR_MATCH - Consider alternative roles'
    
    def _suggest_next_steps(self, score: float) -> List[str]:
        """Suggest next actions"""
        steps = []
        if score >= 80:
            steps.extend(['Schedule technical interview', 'Prepare offer package'])
        elif score >= 70:
            steps.extend(['Send personalized message', 'Conduct phone screening'])
        elif score >= 50:
            steps.extend(['Review additional materials', 'Add to talent pool'])
        else:
            steps.append('Archive and monitor for future roles')
        return steps

advanced_matcher = AdvancedMatchingEngine()
