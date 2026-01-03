import pytest
from services.salary_predictor import SalaryPredictorService


class TestSalaryPredictorService:
    """Test suite for SalaryPredictorService"""

    @pytest.fixture
    def service(self):
        return SalaryPredictorService()

    def test_predict_salary_junior(self, service):
        """Test salary prediction for junior developer"""
        result = service.predict_salary(
            experience_years=1,
            seniority_level='junior',
            skills=['Python', 'JavaScript'],
            location='moscow'
        )
        
        assert result['min'] > 0
        assert result['max'] > result['min']
        assert result['avg'] > 0
        assert result['currency'] == 'RUB'
        assert 'level' in result

    def test_predict_salary_senior(self, service):
        """Test salary prediction for senior developer"""
        result = service.predict_salary(
            experience_years=7,
            seniority_level='senior',
            skills=['Python', 'AWS', 'Kubernetes', 'Machine Learning'],
            location='moscow'
        )
        
        assert result['avg'] > 200000  # Senior should earn more
        assert result['multiplier'] > 1.0

    def test_skill_multipliers(self, service):
        """Test that rare skills increase salary"""
        base = service.predict_salary(3, 'middle', ['Python'], 'moscow')
        with_rust = service.predict_salary(3, 'middle', ['Python', 'Rust'], 'moscow')
        
        assert with_rust['avg'] > base['avg']

    def test_location_multiplier(self, service):
        """Test location impact on salary"""
        moscow = service.predict_salary(3, 'middle', ['Python'], 'moscow')
        spb = service.predict_salary(3, 'middle', ['Python'], 'spb')
        
        assert moscow['avg'] > spb['avg']  # Moscow pays more

    def test_invalid_level_detection(self, service):
        """Test that invalid level is handled"""
        result = service.predict_salary(
            experience_years=3,
            seniority_level='invalid_level',
            skills=['Python'],
            location='moscow'
        )
        
        assert 'level' in result
        assert result['level'] == 'middle'  # Should default to experience-based level

    def test_market_stats(self, service):
        """Test market statistics retrieval"""
        stats = service.get_market_stats('moscow')
        
        assert stats['location'] == 'moscow'
        assert stats['currency'] == 'RUB'
        assert 'levels' in stats
        assert len(stats['levels']) > 0

    def test_salary_comparison(self, service):
        """Test salary comparison"""
        salary1 = service.predict_salary(3, 'middle', ['Python'], 'moscow')
        salary2 = service.predict_salary(5, 'senior', ['Python', 'AWS'], 'moscow')
        
        comparison = service.compare_salaries(salary1, salary2)
        
        assert comparison['difference'] > 0
        assert comparison['percentage_change'] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
