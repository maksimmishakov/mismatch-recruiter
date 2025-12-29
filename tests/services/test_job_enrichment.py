import pytest
from app.services.enrichment.job_enricher import JobEnricher, EnrichedJob

class TestJobEnrichment:
    @pytest.fixture
    def enricher(self):
        return JobEnricher()
    
    @pytest.fixture
    def sample_job(self):
        return {
            "title": "Senior Backend Engineer",
            "description": "We are looking for experienced Python developer with Django, Docker and PostgreSQL",
            "company": "TechCorp",
            "salary_min": 150000,
            "salary_max": 200000,
            "location": "Moscow"
        }
    
    def test_enrich_job_complete(self, enricher, sample_job):
        result = enricher.enrich(sample_job)
        assert isinstance(result, EnrichedJob)
        assert result.title == "Senior Backend Engineer"
        assert len(result.required_skills) > 0
    
    def test_extract_required_skills(self, enricher, sample_job):
        result = enricher.enrich(sample_job)
        assert "Python" in result.required_skills
        assert "Django" in result.required_skills
    
    def test_salary_normalization(self, enricher, sample_job):
        result = enricher.enrich(sample_job)
        assert result.salary_min == 150000
        assert result.salary_max == 200000
        assert result.salary_avg == 175000
    
    def test_job_level_detection(self, enricher, sample_job):
        result = enricher.enrich(sample_job)
        assert result.job_level == "Senior"
    
    def test_location_standardization(self, enricher, sample_job):
        result = enricher.enrich(sample_job)
        assert result.location == "Moscow"
        assert result.location_code == "RU"
    
    def test_soft_skills_extraction(self, enricher, sample_job):
        result = enricher.enrich(sample_job)
        assert result.soft_skills is not None
    
    def test_enrichment_quality_score(self, enricher, sample_job):
        result = enricher.enrich(sample_job)
        assert 0 <= result.enrichment_quality <= 1.0
    
    def test_missing_description(self, enricher):
        job = {"title": "Engineer", "company": "Corp"}
        result = enricher.enrich(job)
        assert result.required_skills == []
