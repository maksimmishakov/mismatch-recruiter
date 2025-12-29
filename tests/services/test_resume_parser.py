import pytest
from app.services.parsing.resume_parser import ResumeParser, ParsedResume

@pytest.fixture
def parser():
    return ResumeParser()

@pytest.fixture
def sample_resume():
    return """
    John Doe
    john.doe@example.com
    +1-234-567-8900
    
    Senior Backend Engineer with 8 years of experience
    
    Skills: Python, Django, PostgreSQL, Docker, AWS
    
    Experience: Backend Engineer at Tech Company (2020-2025)
    Junior Developer at Startup (2017-2020)
    """

def test_parse_resume(parser, sample_resume):
    result = parser.parse(sample_resume)
    assert isinstance(result, ParsedResume)
    assert result.email == "john.doe@example.com"
    assert "+1-234-567-8900" in result.phone
    assert result.experience_years == 8.0
    assert len(result.skills) > 0

def test_extract_skills(parser, sample_resume):
    result = parser.parse(sample_resume)
    assert "Python" in result.skills
    assert "Django" in result.skills
    assert "PostgreSQL" in result.skills

def test_detect_primary_role(parser, sample_resume):
    result = parser.parse(sample_resume)
    assert "Backend" in result.primary_role

def test_confidence_score(parser, sample_resume):
    result = parser.parse(sample_resume)
    assert 0 <= result.confidence_score <= 1.0
    assert result.confidence_score > 0.5

def test_empty_resume(parser):
    result = parser.parse("")
    assert result.email == ""
    assert len(result.skills) == 0
    assert result.confidence_score > 0
