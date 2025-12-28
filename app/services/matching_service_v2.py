"""Advanced Matching Service v2 - ML-based candidate-job matching"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class MatchRecommendation(str, Enum):
    PERFECT_MATCH = "PERFECT_MATCH"
    GOOD_MATCH = "GOOD_MATCH"
    POSSIBLE_MATCH = "POSSIBLE_MATCH"
    NOT_SUITABLE = "NOT_SUITABLE"

@dataclass
class MatchBreakdown:
    skill_match: float
    seniority_match: float
    experience_match: float
    culture_fit: float
    growth_potential: float
    salary_compatibility: float
    final_score: float
    recommendation: MatchRecommendation

@dataclass
class DetailedMatch:
    resume_id: int
    job_id: int
    candidate_name: str
    final_score: float
    breakdown: MatchBreakdown
    recommendation: MatchRecommendation
    explanation: str
    strengths: List[str]
    gaps: List[str]
    learning_potential: str
    interview_questions: List[str]

class MatchingServiceV2:
    """Advanced matching algorithm with weighted factors"""
    
    # WEIGHTS (must sum to 1.0)
    SKILL_WEIGHT = 0.40
    SENIORITY_WEIGHT = 0.30
    EXPERIENCE_WEIGHT = 0.15
    CULTURE_WEIGHT = 0.10
    GROWTH_WEIGHT = 0.05
    
    SENIORITY_MAPPING = {
        "junior": 1,
        "middle": 2,
        "mid": 2,
        "senior": 3,
        "lead": 4,
        "principal": 5,
    }
    
    SALARY_ACCEPTABLE_ABOVE = 1.2
    SALARY_CRITICAL_ABOVE = 1.5
    
    def __init__(self):
        self._validate_weights()
    
    def _validate_weights(self):
        """Ensure weights sum to 1.0"""
        total = (
            self.SKILL_WEIGHT +
            self.SENIORITY_WEIGHT +
            self.EXPERIENCE_WEIGHT +
            self.CULTURE_WEIGHT +
            self.GROWTH_WEIGHT
        )
        assert abs(total - 1.0) < 0.001, f"Weights must sum to 1.0, got {total}"
    
    def calculate_match(self, candidate: Dict, job: Dict) -> DetailedMatch:
        """Calculate comprehensive match between candidate and job"""
        
        # Check hard requirements (early fail)
        if not self._check_hard_requirements(candidate, job):
            return self._create_no_match(candidate, job)
        
        # Calculate individual factors
        skill_score = self._calculate_skill_match(candidate, job)
        seniority_score = self._calculate_seniority_match(candidate, job)
        experience_score = self._calculate_experience_match(candidate, job)
        culture_score = self._calculate_culture_fit(candidate, job)
        growth_score = self._calculate_growth_potential(candidate, job)
        salary_score = self._calculate_salary_compatibility(candidate, job)
        
        # Weighted final score
        final_score = (
            skill_score * self.SKILL_WEIGHT +
            seniority_score * self.SENIORITY_WEIGHT +
            experience_score * self.EXPERIENCE_WEIGHT +
            culture_score * self.CULTURE_WEIGHT +
            growth_score * self.GROWTH_WEIGHT
        )
        
        # Apply salary as multiplier
        if salary_score < 0.3:
            final_score *= 0.5
        elif salary_score < 0.6:
            final_score *= 0.8
        
        final_score = max(0.0, min(1.0, final_score))
        recommendation = self._classify_match(final_score)
        
        breakdown = MatchBreakdown(
            skill_match=skill_score,
            seniority_match=seniority_score,
            experience_match=experience_score,
            culture_fit=culture_score,
            growth_potential=growth_score,
            salary_compatibility=salary_score,
            final_score=final_score,
            recommendation=recommendation
        )
        
        strengths = self._identify_strengths(candidate, job)
        gaps = self._identify_gaps(candidate, job)
        learning_potential = self._assess_learning_potential(candidate, job, gaps)
        explanation = self._generate_explanation(final_score, recommendation, strengths, gaps, learning_potential)
        questions = self._generate_interview_questions(candidate, job, strengths, gaps)
        
        return DetailedMatch(
            resume_id=candidate.get('id'),
            job_id=job.get('id'),
            candidate_name=candidate.get('name', 'Unknown'),
            final_score=final_score,
            breakdown=breakdown,
            recommendation=recommendation,
            explanation=explanation,
            strengths=strengths,
            gaps=gaps,
            learning_potential=learning_potential,
            interview_questions=questions
        )
    
    def _check_hard_requirements(self, candidate: Dict, job: Dict) -> bool:
        """Early fail if hard requirements not met"""
        hard_requirements = job.get('enriched_data', {}).get('hard_requirements', [])
        candidate_skills = self._extract_skills_with_levels(candidate)
        
        for req_skill in hard_requirements:
            skill_name = req_skill.get('name', '').lower()
            if skill_name not in candidate_skills:
                return False
        return True
    
    def _calculate_skill_match(self, candidate: Dict, job: Dict) -> float:
        """Calculate skill matching score (0-1)"""
        candidate_skills = self._extract_skills_with_levels(candidate)
        job_requirements = job.get('enriched_data', {}).get('skills_required', [])
        
        if not job_requirements:
            return 1.0
        
        total_score = 0
        total_weight = 0
        
        for skill_req in job_requirements:
            skill_name = skill_req.get('name', '').lower()
            required_level = skill_req.get('level', 1)
            is_required = skill_req.get('required', True)
            weight = 3.0 if is_required else 1.0
            
            skill_score = 0
            if skill_name in candidate_skills:
                candidate_level = candidate_skills[skill_name]
                if candidate_level >= required_level:
                    skill_score = 1.0
                else:
                    skill_score = min(1.0, candidate_level / required_level)
            
            total_score += skill_score * weight
            total_weight += weight
        
        return (total_score / total_weight) if total_weight > 0 else 0
    
    def _calculate_seniority_match(self, candidate: Dict, job: Dict) -> float:
        """Calculate seniority level compatibility"""
        candidate_seniority = self._extract_seniority_level(candidate)
        job_seniority = job.get('enriched_data', {}).get('seniority_level')
        
        if not job_seniority:
            return 1.0
        
        gap = abs(candidate_seniority - job_seniority)
        
        if gap == 0:
            return 1.0
        elif gap == 1:
            return 0.7
        elif gap == 2:
            return 0.3
        else:
            return 0.0
    
    def _calculate_experience_match(self, candidate: Dict, job: Dict) -> float:
        """Calculate years of experience compatibility"""
        candidate_years = candidate.get('enriched_data', {}).get('total_years_experience', 0)
        job_years_required = job.get('enriched_data', {}).get('years_required', 0)
        
        if job_years_required == 0:
            return 1.0
        
        if candidate_years >= job_years_required:
            return 1.0
        else:
            return min(1.0, candidate_years / job_years_required)
    
    def _calculate_culture_fit(self, candidate: Dict, job: Dict) -> float:
        """Calculate cultural fit and soft skills match"""
        score = 0.5
        
        candidate_remote = candidate.get('enriched_data', {}).get('remote_preference')
        job_remote = job.get('enriched_data', {}).get('remote_policy')
        
        if candidate_remote and job_remote == 'remote':
            score += 0.2
        elif not candidate_remote and job_remote == 'office':
            score += 0.2
        elif job_remote == 'hybrid':
            score += 0.15
        
        return min(1.0, score)
    
    def _calculate_growth_potential(self, candidate: Dict, job: Dict) -> float:
        """Calculate candidate's growth potential for this role"""
        candidate_level = self._extract_seniority_level(candidate)
        job_level = job.get('enriched_data', {}).get('seniority_level', 3)
        
        if candidate_level < job_level:
            learning_ability = candidate.get('enriched_data', {}).get('learning_ability', 0.5)
            return min(0.8, learning_ability + 0.3)
        elif candidate_level == job_level:
            return 0.8
        else:
            return 0.6
    
    def _calculate_salary_compatibility(self, candidate: Dict, job: Dict) -> float:
        """Calculate salary compatibility"""
        candidate_salary = candidate.get('enriched_data', {}).get('salary_expectation', 0)
        job_salary = job.get('salary', 0)
        
        if not job_salary or not candidate_salary:
            return 0.8
        
        ratio = candidate_salary / job_salary
        
        if ratio <= 1.0:
            return 1.0
        elif ratio <= self.SALARY_ACCEPTABLE_ABOVE:
            return 0.8
        elif ratio <= self.SALARY_CRITICAL_ABOVE:
            return 0.4
        else:
            return 0.0
    
    def _extract_skills_with_levels(self, candidate: Dict) -> Dict[str, int]:
        """Extract skills with experience levels"""
        skills = {}
        candidate_skills = candidate.get('enriched_data', {}).get('skills', [])
        
        for skill in candidate_skills:
            if isinstance(skill, dict):
                name = skill.get('name', '').lower()
                years = skill.get('years', 0)
                level = min(5, max(1, (years // 2) + 1))
                skills[name] = level
            else:
                skills[str(skill).lower()] = 1
        
        return skills
    
    def _extract_seniority_level(self, candidate: Dict) -> int:
        """Extract seniority level as integer"""
        seniority_str = candidate.get('enriched_data', {}).get('seniority_level', 'junior').lower()
        return self.SENIORITY_MAPPING.get(seniority_str, 1)
    
    def _identify_strengths(self, candidate: Dict, job: Dict) -> List[str]:
        """Identify candidate's key strengths"""
        strengths = []
        candidate_skills = self._extract_skills_with_levels(candidate)
        job_requirements = job.get('enriched_data', {}).get('skills_required', [])
        
        for skill_req in job_requirements:
            skill_name = skill_req.get('name', '').lower()
            if skill_name in candidate_skills:
                strengths.append(f"{skill_name.title()}")
        
        if self._calculate_seniority_match(candidate, job) == 1.0:
            seniority = candidate.get('enriched_data', {}).get('seniority_level', 'mid')
            strengths.append(f"Right seniority ({seniority})")
        
        return strengths or ["Relevant background"]
    
    def _identify_gaps(self, candidate: Dict, job: Dict) -> List[str]:
        """Identify gaps between candidate and job"""
        gaps = []
        candidate_skills = self._extract_skills_with_levels(candidate)
        job_requirements = job.get('enriched_data', {}).get('skills_required', [])
        
        for skill_req in job_requirements:
            skill_name = skill_req.get('name', '').lower()
            if skill_name not in candidate_skills:
                gaps.append(f"{skill_name.title()}")
        
        return gaps or ["All requirements met"]
    
    def _assess_learning_potential(self, candidate: Dict, job: Dict, gaps: List[str]) -> str:
        """Assess if candidate can learn missing skills"""
        if not gaps or gaps == ["All requirements met"]:
            return "EXCELLENT"
        
        learning_ability = candidate.get('enriched_data', {}).get('learning_ability', 0.5)
        gap_count = len(gaps)
        
        if learning_ability > 0.7 and gap_count <= 2:
            return "HIGH"
        elif learning_ability > 0.5 and gap_count <= 1:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_explanation(self, final_score: float, recommendation, strengths, gaps, learning_potential) -> str:
        """Generate human-readable match explanation"""
        explanation = f"{final_score:.0%} match. "
        
        if recommendation == MatchRecommendation.PERFECT_MATCH:
            explanation += "Excellent candidate. "
        elif recommendation == MatchRecommendation.GOOD_MATCH:
            explanation += "Strong candidate. "
        elif recommendation == MatchRecommendation.POSSIBLE_MATCH:
            explanation += "Possible candidate. "
        else:
            explanation += "Not a good fit. "
        
        if strengths and strengths[0] != "Relevant background":
            explanation += f"Strengths: {', '.join(strengths[:2])}. "
        
        if gaps and gaps[0] != "All requirements met":
            explanation += f"Gaps: {', '.join(gaps[:2])}. "
        
        explanation += f"Learning potential: {learning_potential}."
        
        return explanation
    
    def _generate_interview_questions(self, candidate: Dict, job: Dict, strengths, gaps) -> List[str]:
        """Generate targeted interview questions"""
        questions = []
        
        candidate_skills = self._extract_skills_with_levels(candidate)
        for skill in list(candidate_skills.keys())[:2]:
            questions.append(f"Tell me about your experience with {skill.title()}.")
        
        for gap in gaps[:2]:
            skill_name = gap.split('(')[0].strip()
            questions.append(f"You don't have {skill_name} experience. How would you learn it?")
        
        job_title = job.get('enriched_data', {}).get('title', 'position')
        questions.append(f"Why are you interested in this {job_title} role?")
        
        return questions[:5]
    
    def _classify_match(self, score: float) -> MatchRecommendation:
        """Classify match quality based on score"""
        if score >= 0.85:
            return MatchRecommendation.PERFECT_MATCH
        elif score >= 0.70:
            return MatchRecommendation.GOOD_MATCH
        elif score >= 0.50:
            return MatchRecommendation.POSSIBLE_MATCH
        else:
            return MatchRecommendation.NOT_SUITABLE
    
    def _create_no_match(self, candidate: Dict, job: Dict) -> DetailedMatch:
        """Create no-match result"""
        return DetailedMatch(
            resume_id=candidate.get('id'),
            job_id=job.get('id'),
            candidate_name=candidate.get('name', 'Unknown'),
            final_score=0.0,
            breakdown=MatchBreakdown(
                skill_match=0.0,
                seniority_match=0.0,
                experience_match=0.0,
                culture_fit=0.0,
                growth_potential=0.0,
                salary_compatibility=0.0,
                final_score=0.0,
                recommendation=MatchRecommendation.NOT_SUITABLE
            ),
            recommendation=MatchRecommendation.NOT_SUITABLE,
            explanation="Does not meet hard requirements.",
            strengths=[],
            gaps=["Missing required skills"],
            learning_potential="NOT_APPLICABLE",
            interview_questions=[]
        )
    
    def batch_calculate_matches(self, candidates: List[Dict], job: Dict, limit: int = None) -> List[DetailedMatch]:
        """Calculate matches for multiple candidates"""
        matches = []
        
        for candidate in candidates:
            match = self.calculate_match(candidate, job)
            matches.append(match)
        
        matches.sort(key=lambda m: m.final_score, reverse=True)
        
        if limit:
            matches = matches[:limit]
        
        return matches
    
    def find_jobs_for_candidate(self, candidate: Dict, jobs: List[Dict], limit: int = 10) -> List[DetailedMatch]:
        """Find best job matches for a candidate"""
        matches = []
        
        for job in jobs:
            match = self.calculate_match(candidate, job)
            matches.append(match)
        
        matches.sort(key=lambda m: m.final_score, reverse=True)
        
        return matches[:limit]
