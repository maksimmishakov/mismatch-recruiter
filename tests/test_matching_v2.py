"""Tests for advanced matching service v2"""

import pytest
from app.services.matching_service_v2 import MatchingServiceV2, MatchRecommendation

class TestMatchingServiceV2:
    @pytest.fixture
    def service(self):
        return MatchingServiceV2()
    
    @pytest.fixture
    def perfect_candidate(self):
        return {
            'id': 1,
            'name': 'Senior Dev',
            'enriched_data': {
                'skills': [{'name': 'Python', 'years': 8}],
                'seniority_level': 'senior',
                'total_years_experience': 10,
                'salary_expectation': 100000
            }
        }
    
    @pytest.fixture
    def test_job(self):
        return {
            'id': 1,
            'title': 'Senior Python Engineer',
            'salary': 150000,
            'enriched_data': {
                'skills_required': [{'name': 'Python', 'level': 3, 'required': True}],
                'seniority_level': 3,
                'years_required': 5,
                'hard_requirements': [{'name': 'Python', 'level': 3}]
            }
        }
    
    def test_perfect_match(self, service, perfect_candidate, test_job):
        """Test perfect match scenario"""
        match = service.calculate_match(perfect_candidate, test_job)
        assert match.final_score > 0.80
        assert match.recommendation == MatchRecommendation.PERFECT_MATCH
    
    def test_seniority_mismatch(self, service, test_job):
        """Test junior candidate for senior role"""
        junior = {
            'id': 2,
            'name': 'Junior Dev',
            'enriched_data': {
                'skills': [{'name': 'Python', 'years': 1}],
                'seniority_level': 'junior',
                'total_years_experience': 1,
            }
        }
        match = service.calculate_match(junior, test_job)
        assert match.final_score < 0.60
    
    def test_hard_requirement_fail(self, service, test_job):
        """Test missing hard requirement"""
        missing_skill = {
            'id': 3,
            'name': 'Dev',
            'enriched_data': {
                'skills': [{'name': 'Java', 'years': 5}],
                'seniority_level': 'mid'
            }
        }
        match = service.calculate_match(missing_skill, test_job)
        assert match.final_score == 0.0
        assert match.recommendation == MatchRecommendation.NOT_SUITABLE
    
    def test_salary_compatibility(self, service, perfect_candidate, test_job):
        """Test salary compatibility scoring"""
        match = service.calculate_match(perfect_candidate, test_job)
        assert match.breakdown.salary_compatibility == 1.0  # Candidate below job salary
    
    def test_weights_sum_to_one(self, service):
        """Verify weights sum to 1.0"""
        total = (
            service.SKILL_WEIGHT +
            service.SENIORITY_WEIGHT +
            service.EXPERIENCE_WEIGHT +
            service.CULTURE_WEIGHT +
            service.GROWTH_WEIGHT
        )
        assert abs(total - 1.0) < 0.001
    
    def test_match_classification(self, service):
        """Test match classification ranges"""
        assert service._classify_match(0.90) == MatchRecommendation.PERFECT_MATCH
        assert service._classify_match(0.75) == MatchRecommendation.GOOD_MATCH
        assert service._classify_match(0.60) == MatchRecommendation.POSSIBLE_MATCH
        assert service._classify_match(0.30) == MatchRecommendation.NOT_SUITABLE
    
    def test_batch_processing(self, service, test_job):
        """Test batch processing multiple candidates"""
        candidates = [
            {'id': i, 'name': f'Candidate {i}', 'enriched_data': {'skills': [], 'seniority_level': 'mid'}}
            for i in range(10)
        ]
        matches = service.batch_calculate_matches(candidates, test_job)
        assert len(matches) == 10
        assert matches[0].final_score >= matches[-1].final_score  # Sorted by score
