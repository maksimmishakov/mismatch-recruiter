"""Test Lamoda Routes Integration"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime


class TestLamodaJobsRoute:
    """Test /api/v1/lamoda/jobs endpoint"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        from app.main import app
        return TestClient(app)
    
    def test_get_jobs_success(self, client):
        """Test successful job retrieval from Lamoda"""
        with patch('app.routes.lamoda.lamoda_client') as mock_client:
            mock_client.get_jobs.return_value = {
                "jobs": [
                    {
                        "id": "job-123",
                        "title": "Python Developer",
                        "company": "TechCorp",
                        "location": "Moscow",
                        "salary_min": 150000,
                        "salary_max": 200000
                    }
                ],
                "total": 1
            }
            
            response = client.get("/api/v1/lamoda/jobs")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data["jobs"]) == 1
            assert data["jobs"][0]["title"] == "Python Developer"
            assert data["jobs"][0]["company"] == "TechCorp"
    
    def test_get_jobs_with_filters(self, client):
        """Test job retrieval with filters"""
        with patch('app.routes.lamoda.lamoda_client') as mock_client:
            mock_client.get_jobs.return_value = {
                "jobs": [
                    {
                        "id": "job-456",
                        "title": "Senior Python Developer",
                        "salary_min": 200000,
                        "salary_max": 300000
                    }
                ],
                "total": 1
            }
            
            response = client.get(
                "/api/v1/lamoda/jobs",
                params={"min_salary": "200000", "experience": "senior"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["jobs"][0]["salary_min"] >= 200000
    
    def test_get_jobs_unauthorized(self, client):
        """Test unauthorized access"""
        response = client.get("/api/v1/lamoda/jobs")
        assert response.status_code == 401


class TestLamodaCandidatesRoute:
    """Test /api/v1/lamoda/candidates endpoint"""
    
    @pytest.fixture
    def client(self):
        from app.main import app
        return TestClient(app)
    
    def test_get_candidates_success(self, client):
        """Test successful candidate retrieval"""
        with patch('app.routes.lamoda.lamoda_client') as mock_client:
            mock_client.get_candidates.return_value = {
                "candidates": [
                    {
                        "id": "cand-789",
                        "name": "Ivan Petrov",
                        "email": "ivan@example.com",
                        "skills": ["Python", "Django", "PostgreSQL"]
                    }
                ],
                "total": 1
            }
            
            response = client.get("/api/v1/lamoda/candidates")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data["candidates"]) == 1
            assert data["candidates"][0]["name"] == "Ivan Petrov"
    
    def test_create_candidate(self, client):
        """Test candidate creation"""
        with patch('app.routes.lamoda.lamoda_client') as mock_client:
            mock_client.create_candidate.return_value = {
                "id": "cand-new",
                "name": "Maria Smirnova",
                "email": "maria@example.com",
                "status": "active"
            }
            
            payload = {
                "name": "Maria Smirnova",
                "email": "maria@example.com",
                "phone": "+7 999 123 45 67"
            }
            
            response = client.post("/api/v1/lamoda/candidates", json=payload)
            
            assert response.status_code == 201
            data = response.json()
            assert data["id"] == "cand-new"


class TestLamodaMatchingRoute:
    """Test /api/v1/lamoda/match endpoint"""
    
    @pytest.fixture
    def client(self):
        from app.main import app
        return TestClient(app)
    
    def test_match_candidate_to_job(self, client):
        """Test matching candidates to jobs"""
        with patch('app.routes.lamoda.matching_service') as mock_service:
            mock_service.calculate_match_score.return_value = {
                "candidate_id": "cand-789",
                "job_id": "job-123",
                "match_score": 0.87,
                "match_details": {
                    "skills_match": 0.95,
                    "experience_match": 0.80,
                    "salary_match": 0.85
                }
            }
            
            payload = {"candidate_id": "cand-789", "job_id": "job-123"}
            response = client.post("/api/v1/lamoda/match", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["match_score"] > 0.8


class TestLamodaSyncRoute:
    """Test /api/v1/lamoda/sync endpoint"""
    
    @pytest.fixture
    def client(self):
        from app.main import app
        return TestClient(app)
    
    def test_trigger_sync(self, client):
        """Test manual sync trigger"""
        with patch('app.routes.lamoda.lamoda_sync_task') as mock_task:
            mock_task.delay.return_value = MagicMock(id="task-sync-001")
            
            response = client.post("/api/v1/lamoda/sync", json={"sync_type": "full"})
            
            assert response.status_code in [200, 202]
            data = response.json()
            assert "task_id" in data or "status" in data
    
    def test_sync_status(self, client):
        """Test sync status endpoint"""
        with patch('app.services.lamoda_sync.get_sync_status') as mock_status:
            mock_status.return_value = {
                "status": "running",
                "progress": 45,
                "jobs_synced": 450,
                "candidates_synced": 320,
                "errors": 2
            }
            
            response = client.get("/api/v1/lamoda/sync/status")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] in ["running", "completed", "error"]


class TestLamodaPlacementsRoute:
    """Test /api/v1/lamoda/placements endpoint"""
    
    @pytest.fixture
    def client(self):
        from app.main import app
        return TestClient(app)
    
    def test_create_placement(self, client):
        """Test placement creation"""
        with patch('app.routes.lamoda.placement_service') as mock_service:
            mock_service.create_placement.return_value = {
                "id": "plac-123",
                "candidate_id": "cand-789",
                "job_id": "job-123",
                "status": "submitted",
                "created_at": datetime.utcnow().isoformat()
            }
            
            payload = {
                "candidate_id": "cand-789",
                "job_id": "job-123",
                "notes": "Strong match, recommended"
            }
            
            response = client.post("/api/v1/lamoda/placements", json=payload)
            
            assert response.status_code == 201
            data = response.json()
            assert data["status"] == "submitted"
    
    def test_get_placements(self, client):
        """Test placement retrieval"""
        with patch('app.routes.lamoda.placement_service') as mock_service:
            mock_service.get_placements.return_value = {
                "placements": [
                    {
                        "id": "plac-123",
                        "candidate_id": "cand-789",
                        "job_id": "job-123",
                        "status": "submitted"
                    }
                ],
                "total": 1
            }
            
            response = client.get("/api/v1/lamoda/placements")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data["placements"]) >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
