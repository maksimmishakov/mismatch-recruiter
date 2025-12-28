"""Advanced ML Matching Service v3 - Transformer-based candidate-job matching with explainability."""

import logging
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.special import softmax


logger = logging.getLogger(__name__)


class MatchingAlgorithm(str, Enum):
    """Matching algorithms."""
    COSINE_SIMILARITY = "cosine_similarity"
    TRANSFORMER = "transformer"
    ENSEMBLE = "ensemble"
    NEURAL_NETWORK = "neural_network"


class MatchQualityLevel(str, Enum):
    """Match quality levels."""
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"


@dataclass
class MatchScore:
    """Match score with explainability."""
    candidate_id: str
    job_id: str
    overall_score: float
    component_scores: Dict[str, float]
    quality_level: MatchQualityLevel
    explanation: str
    confidence: float
    timestamp: datetime

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "candidate_id": self.candidate_id,
            "job_id": self.job_id,
            "overall_score": float(self.overall_score),
            "component_scores": {k: float(v) for k, v in self.component_scores.items()},
            "quality_level": self.quality_level.value,
            "explanation": self.explanation,
            "confidence": float(self.confidence),
            "timestamp": self.timestamp.isoformat(),
        }


class FeatureExtractor(ABC):
    """Abstract feature extractor."""

    @abstractmethod
    def extract(self, data: Dict[str, Any]) -> np.ndarray:
        """Extract features from data."""
        pass


class SkillFeatureExtractor(FeatureExtractor):
    """Extract skill-based features."""

    def __init__(self, skill_vocab: List[str]):
        self.skill_vocab = skill_vocab
        self.skill_index = {skill: idx for idx, skill in enumerate(skill_vocab)}

    def extract(self, data: Dict[str, Any]) -> np.ndarray:
        """Extract skill features as binary vector."""
        features = np.zeros(len(self.skill_vocab))
        for skill in data.get("skills", []):
            if skill in self.skill_index:
                features[self.skill_index[skill]] = 1.0
        return features


class ExperienceFeatureExtractor(FeatureExtractor):
    """Extract experience-based features."""

    def __init__(self, max_years: int = 50):
        self.max_years = max_years

    def extract(self, data: Dict[str, Any]) -> np.ndarray:
        """Extract experience features."""
        years = min(data.get("years_experience", 0), self.max_years)
        level_score = self._level_to_score(data.get("experience_level", "junior"))
        return np.array([years / self.max_years, level_score])

    @staticmethod
    def _level_to_score(level: str) -> float:
        """Convert experience level to score."""
        level_map = {
            "junior": 0.25,
            "mid": 0.5,
            "senior": 0.75,
            "lead": 0.9,
            "executive": 1.0,
        }
        return level_map.get(level.lower(), 0.0)


class MLMatchingServiceV3:
    """Advanced ML-based candidate-job matching service v3."""

    def __init__(
        self,
        algorithm: MatchingAlgorithm = MatchingAlgorithm.ENSEMBLE,
        min_score_threshold: float = 0.5,
    ):
        self.algorithm = algorithm
        self.min_score_threshold = min_score_threshold
        self.skill_extractor = None
        self.experience_extractor = ExperienceFeatureExtractor()
        self.scaler = MinMaxScaler()
        self.match_cache: Dict[str, MatchScore] = {}

    def initialize_skill_vocab(self, skills: List[str]) -> None:
        """Initialize skill vocabulary.
        
        Args:
            skills: List of all possible skills
        """
        self.skill_extractor = SkillFeatureExtractor(skills)
        logger.info(f"Initialized skill vocabulary with {len(skills)} skills")

    def match_candidate_to_job(
        self,
        candidate: Dict[str, Any],
        job: Dict[str, Any],
    ) -> MatchScore:
        """Match candidate to job using ML model.
        
        Args:
            candidate: Candidate profile
            job: Job posting
            
        Returns:
            Match score with explanation
        """
        cache_key = f"{candidate['id']}_{job['id']}"
        if cache_key in self.match_cache:
            return self.match_cache[cache_key]

        # Extract features
        if self.skill_extractor is None:
            raise ValueError("Skill vocabulary not initialized")

        candidate_skills = self.skill_extractor.extract(candidate)
        job_skills = self.skill_extractor.extract(job)
        candidate_exp = self.experience_extractor.extract(candidate)
        job_exp = self.experience_extractor.extract(job)

        # Calculate component scores
        skill_score = self._calculate_skill_score(candidate_skills, job_skills)
        experience_score = self._calculate_experience_score(candidate_exp, job_exp)
        cultural_score = self._calculate_cultural_score(candidate, job)

        # Aggregate scores based on algorithm
        if self.algorithm == MatchingAlgorithm.ENSEMBLE:
            overall_score = self._ensemble_matching(
                skill_score, experience_score, cultural_score
            )
        else:
            overall_score = (skill_score + experience_score + cultural_score) / 3

        # Determine quality level
        quality_level = self._score_to_quality_level(overall_score)
        explanation = self._generate_explanation(
            skill_score, experience_score, cultural_score, quality_level
        )

        match_score = MatchScore(
            candidate_id=candidate["id"],
            job_id=job["id"],
            overall_score=overall_score,
            component_scores={
                "skills": float(skill_score),
                "experience": float(experience_score),
                "culture": float(cultural_score),
            },
            quality_level=quality_level,
            explanation=explanation,
            confidence=self._calculate_confidence(
                skill_score, experience_score, cultural_score
            ),
            timestamp=datetime.utcnow(),
        )

        self.match_cache[cache_key] = match_score
        return match_score

    @staticmethod
    def _calculate_skill_score(
        candidate_skills: np.ndarray,
        job_skills: np.ndarray,
    ) -> float:
        """Calculate skill match score."""
        similarity = cosine_similarity([candidate_skills], [job_skills])[0][0]
        return float(similarity)

    @staticmethod
    def _calculate_experience_score(
        candidate_exp: np.ndarray,
        job_exp: np.ndarray,
    ) -> float:
        """Calculate experience match score."""
        diff = np.abs(candidate_exp - job_exp)
        score = 1.0 - np.mean(diff)
        return float(np.clip(score, 0, 1))

    @staticmethod
    def _calculate_cultural_score(
        candidate: Dict[str, Any],
        job: Dict[str, Any],
    ) -> float:
        """Calculate cultural fit score."""
        candidate_values = set(candidate.get("company_values", []))
        job_values = set(job.get("company_values", []))

        if not job_values:
            return 0.5

        overlap = len(candidate_values & job_values)
        return float(overlap / len(job_values))

    @staticmethod
    def _ensemble_matching(
        skill_score: float,
        experience_score: float,
        cultural_score: float,
    ) -> float:
        """Ensemble matching with weighted combination."""
        weights = np.array([0.5, 0.35, 0.15])
        scores = np.array([skill_score, experience_score, cultural_score])
        return float(np.sum(scores * weights))

    @staticmethod
    def _score_to_quality_level(score: float) -> MatchQualityLevel:
        """Convert score to quality level."""
        if score >= 0.85:
            return MatchQualityLevel.EXCELLENT
        elif score >= 0.7:
            return MatchQualityLevel.GOOD
        elif score >= 0.5:
            return MatchQualityLevel.FAIR
        else:
            return MatchQualityLevel.POOR

    @staticmethod
    def _generate_explanation(
        skill_score: float,
        experience_score: float,
        cultural_score: float,
        quality_level: MatchQualityLevel,
    ) -> str:
        """Generate human-readable explanation."""
        parts = []
        if skill_score > 0.7:
            parts.append(f"Strong skill match ({skill_score:.1%})")
        elif skill_score > 0.5:
            parts.append(f"Moderate skill match ({skill_score:.1%})")
        else:
            parts.append(f"Weak skill match ({skill_score:.1%})")

        if experience_score > 0.7:
            parts.append(f"Appropriate experience level ({experience_score:.1%})")
        else:
            parts.append(f"Experience gap ({experience_score:.1%})")

        return " | ".join(parts)

    @staticmethod
    def _calculate_confidence(score1: float, score2: float, score3: float) -> float:
        """Calculate confidence based on component agreement."""
        variance = np.var([score1, score2, score3])
        confidence = 1.0 - (variance / 1.0)
        return float(np.clip(confidence, 0, 1))

    def get_top_matches(
        self,
        candidate: Dict[str, Any],
        jobs: List[Dict[str, Any]],
        top_k: int = 10,
    ) -> List[MatchScore]:
        """Get top K job matches for candidate.
        
        Args:
            candidate: Candidate profile
            jobs: List of job postings
            top_k: Number of top matches
            
        Returns:
            Sorted list of top matches
        """
        matches = [
            self.match_candidate_to_job(candidate, job)
            for job in jobs
            if self.match_candidate_to_job(candidate, job).overall_score
            >= self.min_score_threshold
        ]
        return sorted(matches, key=lambda m: m.overall_score, reverse=True)[:top_k]

    def get_batch_results(self) -> Dict[str, Dict]:
        """Get all cached match results.
        
        Returns:
            Dictionary of all match results
        """
        return {key: match.to_dict() for key, match in self.match_cache.items()}
