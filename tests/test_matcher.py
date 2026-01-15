"""Tests for ML Matching Engine - Phase 2"""
import pytest
from datetime import datetime
from app.ml.matcher import MatchingEngine
from app.models import db, Candidate, Job, Match


class TestMatchingEngine:
    """Test suite for MatchingEngine class"""

    def setup_method(self):
        """Setup test fixtures"""
        self.engine = MatchingEngine()
        self.candidate_data = {
            'skills': ['Python', 'JavaScript', 'React'],
            'experience_years': 5,
            'location': 'San Francisco',
            'salary_expectation': 120000,
            'availability': 'immediate'
        }
        self.job_data = {
            'required_skills': ['Python', 'JavaScript'],
            'experience_required': 3,
            'location': 'San Francisco',
            'salary_range': (100000, 150000),
            'job_type': 'full-time'
        }

    def test_skill_matching(self):
        """Test skill matching algorithm"""
        score = self.engine.calculate_skill_match(self.candidate_data['skills'], self.job_data['required_skills'])
        assert score > 0.8  # Should have high match
        assert isinstance(score, float)

    def test_experience_matching(self):
        """Test experience level matching"""
        score = self.engine.calculate_experience_match(
            self.candidate_data['experience_years'],
            self.job_data['experience_required']
        )
        assert score > 0.7  # Candidate has more experience than required

    def test_location_matching(self):
        """Test location compatibility"""
        score = self.engine.calculate_location_match(
            self.candidate_data['location'],
            self.job_data['location']
        )
        assert score == 1.0  # Exact match

    def test_salary_matching(self):
        """Test salary expectation vs range"""
        score = self.engine.calculate_salary_match(
            self.candidate_data['salary_expectation'],
            self.job_data['salary_range']
        )
        assert 0.5 < score <= 1.0  # Within acceptable range

    def test_overall_score_calculation(self):
        """Test overall match score calculation"""
        overall_score = self.engine.calculate_overall_score(
            self.candidate_data,
            self.job_data
        )
        assert 0 <= overall_score <= 100
        assert isinstance(overall_score, (int, float))

    def test_score_breakdown(self):
        """Test score breakdown by category"""
        breakdown = self.engine.calculate_score_breakdown(
            self.candidate_data,
            self.job_data
        )
        assert 'skills' in breakdown
        assert 'experience' in breakdown
        assert 'location' in breakdown
        assert 'salary' in breakdown
        assert all(0 <= score <= 100 for score in breakdown.values())

    def test_low_skill_match(self):
        """Test low skill match scenario"""
        poor_candidate = self.candidate_data.copy()
        poor_candidate['skills'] = ['Java', 'C++']
        score = self.engine.calculate_skill_match(poor_candidate['skills'], self.job_data['required_skills'])
        assert score < 0.5  # Low match

    def test_overqualified_experience(self):
        """Test overqualified candidate"""
        overqualified = self.candidate_data.copy()
        overqualified['experience_years'] = 15
        score = self.engine.calculate_overall_score(overqualified, self.job_data)
        assert score > self.engine.calculate_overall_score(self.candidate_data, self.job_data)

    def test_salary_out_of_range(self):
        """Test candidate with salary expectation outside range"""
        demanding = self.candidate_data.copy()
        demanding['salary_expectation'] = 250000
        score = self.engine.calculate_salary_match(
            demanding['salary_expectation'],
            self.job_data['salary_range']
        )
        assert score < 0.5  # Poor match


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
