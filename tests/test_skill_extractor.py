import pytest
from app.services.parsing.skill_extractor import SkillExtractor

@pytest.fixture
def extractor():
    return SkillExtractor()

class TestSkillExtraction:
    def test_none_input(self, extractor):
        result = extractor.extract_and_categorize(None)
        assert result == []
    
    def test_empty_string(self, extractor):
        result = extractor.extract_and_categorize("")
        assert result == []
    
    def test_invalid_type(self, extractor):
        result = extractor.extract_and_categorize(123)
        assert result == []
