"""Тесты для обогащения вакансий."""

import pytest
from app.services.job_enrichment_service import JobEnrichmentService

@pytest.fixture
def enricher():
    return JobEnrichmentService()

class TestJobEnrichmentService:
    def test_extract_required_skills(self, enricher):
        requirements = "Python, Django, PostgreSQL, Docker, Kubernetes"
        skills = enricher._extract_required_skills(requirements)
        assert len(skills) >= 3
        assert any(s['name'].lower() == 'python' for s in skills)

    def test_identify_seniority_junior(self, enricher):
        text = "Junior Developer, entry-level position, 0-2 years experience"
        level = enricher._identify_seniority(text)
        assert level == 'junior'

    def test_identify_seniority_mid(self, enricher):
        text = "Mid-level Engineer with 5+ years experience"
        level = enricher._identify_seniority(text)
        assert level == 'mid'

    def test_identify_seniority_senior(self, enricher):
        text = "Senior Backend Engineer, 8+ years required"
        level = enricher._identify_seniority(text)
        assert level == 'senior'

    def test_identify_seniority_lead(self, enricher):
        text = "Lead Architect, Principal Engineer, 15+ years"
        level = enricher._identify_seniority(text)
        assert level == 'lead'

    def test_calculate_difficulty_simple(self, enricher):
        requirements = "Python, Flask"
        score = enricher._calculate_difficulty(requirements)
        assert 0.0 <= score <= 1.0
        assert score < 0.5

    def test_calculate_difficulty_complex(self, enricher):
        requirements = """
        Python, Django, FastAPI, PostgreSQL, MongoDB, Redis, 
        Docker, Kubernetes, AWS, GCP, Machine Learning, Deep Learning,
        Distributed Systems, Microservices
        """
        score = enricher._calculate_difficulty(requirements)
        assert score > 0.5

    def test_extract_benefits(self, enricher):
        text = """
        We offer:
        - Fully remote position
        - Flexible working hours
        - Unlimited PTO
        - Stock options
        - Health insurance
        - Conference budget
        """
        benefits = enricher._extract_benefits(text)
        assert 'remote' in benefits
        assert 'flexible_hours' in benefits
        assert 'unlimited_pto' in benefits

    def test_extract_salary_min(self, enricher):
        text = "Salary: $100k - $150k per year"
        salary = enricher._extract_salary_min(text)
        assert salary == 100000

    def test_extract_salary_max(self, enricher):
        text = "Salary: $100k - $150k per year"
        salary = enricher._extract_salary_max(text)
        assert salary == 150000

    def test_enrich_full_job(self, enricher):
        job_title = "Senior Backend Engineer"
        description = """
        We're looking for a Senior Backend Engineer to join our team.
        You'll work with Python, Django, and PostgreSQL.
        Fully remote position with flexible hours.
        Salary: $120k - $180k
        """
        requirements = """
        Required:
        - 8+ years of backend development
        - Python, Django, FastAPI
        - PostgreSQL, Redis
        - Docker, Kubernetes
        - AWS
        
        Nice to have:
        - Machine Learning
        - Distributed systems
        """
        
        result = enricher.enrich(job_title, description, requirements)
        
        assert result['enrichment_status'] == 'success'
        assert result['seniority_level'] == 'senior'
        assert result['difficulty_score'] > 0.5
        assert 'remote' in result['benefits']
        assert result['salary_min'] == 120000
        assert result['salary_max'] == 180000
        assert len(result['required_skills']) > 0
