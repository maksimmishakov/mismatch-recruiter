import pytest
from app.services.resume_parser import ResumeParser

@pytest.fixture
def parser():
    return ResumeParser()

class TestEmailExtraction:
    def test_valid_email(self, parser):
        text = "Contact me at john.doe@example.com"
        email = parser._extract_email(text)
        assert email == "john.doe@example.com"
    
    def test_invalid_email_no_tld(self, parser):
        text = "Contact john@example"
        email = parser._extract_email(text)
        assert email is None
    
    def test_none_input(self, parser):
        email = parser._extract_email(None)
        assert email is None
    
    def test_empty_string(self, parser):
        email = parser._extract_email("")
        assert email is None

