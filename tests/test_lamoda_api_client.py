"""Test Lamoda API Client
Tests for app.services.lamoda_api_client module
"""
import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock
from app.services.lamoda_api_client import (
    LamodaAPIClient,
    LamodaJob,
    CandidateProfile,
    Placement,
    LamodaAPIError,
    PlacementStatus,
    LamodaJobStatus
)


class TestLamodaClientInit:
    """Test LamodaAPIClient initialization"""
    
    def test_client_initialization(self):
        """Test client can be initialized with credentials"""
        client = LamodaAPIClient(
            api_key="test-key",
            api_secret="test-secret",
            api_url="https://api.test.com"
        )
        assert client.api_key == "test-key"
        assert client.api_secret == "test-secret"
        assert client.api_url == "https://api.test.com"
    
    def test_client_with_environment(self):
        """Test client initialization with environment parameter"""
        client = LamodaAPIClient(
            api_key="test",
            api_secret="test",
            api_url="https://api.test.com",
            environment="sandbox"
        )
        assert client.environment == "sandbox"


class TestHMACSignature:
    """Test HMAC signature generation"""
    
    def test_signature_generation(self):
        """Test HMAC-SHA256 signature is generated correctly"""
        client = LamodaAPIClient(
            api_key="test",
            api_secret="secret",
            api_url="https://api.test.com"
        )
        signature = client._generate_signature("GET", "/jobs", "")
        assert signature is not None
        assert "Lamoda" in signature
        assert ":" in signature
    
    def test_signature_deterministic(self):
        """Test signature is deterministic for same input"""
        client = LamodaAPIClient(
            api_key="test",
            api_secret="secret",
            api_url="https://api.test.com"
        )
        sig1 = client._generate_signature("POST", "/placements", '{}')
        sig2 = client._generate_signature("POST", "/placements", '{}')
        assert sig1 == sig2


class TestLamodaJobModel:
    """Test LamodaJob data structure"""
    
    def test_job_to_dict(self):
        """Test LamodaJob can be converted to dict"""
        job = LamodaJob(
            id="lamoda-123",
            title="Python Developer",
            description="Seeking experienced Python developer",
            company="TechCorp",
            salary_from=80000,
            salary_to=120000
        )
        job_dict = job.to_dict()
        assert job_dict["id"] == "lamoda-123"
        assert job_dict["title"] == "Python Developer"
        assert job_dict["salary_from"] == 80000


class TestCandidateProfile:
    """Test CandidateProfile data structure"""
    
    def test_candidate_profile_creation(self):
        """Test CandidateProfile can be created with required fields"""
        candidate = CandidateProfile(
            id="cand-456",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            experience_years=5,
            skills=["Python", "FastAPI"],
            match_score=0.85
        )
        assert candidate.id == "cand-456"
        assert candidate.match_score == 0.85
        assert "Python" in candidate.skills


class TestPlacementModel:
    """Test Placement data structure"""
    
    def test_placement_creation(self):
        """Test Placement can track submissions and results"""
        now = datetime.utcnow()
        placement = Placement(
            id="plac-789",
            job_id="lamoda-123",
            candidate_id="cand-456",
            status="submitted",
            created_at=now,
            updated_at=now
        )
        assert placement.id == "plac-789"
        assert placement.status == "submitted"


class TestLamodaAPIError:
    """Test error handling"""
    
    def test_error_with_status_code(self):
        """Test LamodaAPIError captures status codes"""
        error = LamodaAPIError("Unauthorized", 401)
        assert error.status_code == 401
        assert "Unauthorized" in str(error)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
