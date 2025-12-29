"""Test Mismatch Database Models"""
import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


@pytest.fixture
def db_session():
    """Create in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    from app.database import Base
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = pytest.importorskip('sqlalchemy').sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


class TestMismatchJobModel:
    """Test MismatchJob model"""
    
    def test_create_job_model(self, db_session: Session):
        """Test creating a MismatchJob instance"""
        from app.models.Mismatch import MismatchJob
        
        job = MismatchJob(
            Mismatch_id="job-123",
            title="Python Developer",
            company="TechCorp",
            description="Build scalable backend systems",
            location="Moscow",
            salary_min=150000,
            salary_max=200000,
            currency="RUB",
            employment_type="full_time",
            experience_level="mid",
            skills=["Python", "Django", "PostgreSQL"],
            requirements="5+ years of experience",
            benefits="Remote, Health Insurance",
            posted_at=datetime.utcnow(),
            external_url="https://Mismatch.ru/jobs/123"
        )
        
        db_session.add(job)
        db_session.commit()
        
        retrieved = db_session.query(MismatchJob).filter_by(Mismatch_id="job-123").first()
        assert retrieved is not None
        assert retrieved.title == "Python Developer"
        assert retrieved.company == "TechCorp"
    
    def test_job_salary_range(self, db_session: Session):
        """Test job salary range validation"""
        from app.models.Mismatch import MismatchJob
        
        job = MismatchJob(
            Mismatch_id="job-456",
            title="Senior Developer",
            company="StartUp",
            salary_min=300000,
            salary_max=400000
        )
        
        db_session.add(job)
        db_session.commit()
        
        retrieved = db_session.query(MismatchJob).filter_by(Mismatch_id="job-456").first()
        assert retrieved.salary_min <= retrieved.salary_max


class TestMismatchCandidateModel:
    """Test MismatchCandidate model"""
    
    def test_create_candidate_model(self, db_session: Session):
        """Test creating a MismatchCandidate instance"""
        from app.models.Mismatch import MismatchCandidate
        
        candidate = MismatchCandidate(
            Mismatch_id="cand-789",
            first_name="Ivan",
            last_name="Petrov",
            email="ivan@example.com",
            phone="+7 999 123 45 67",
            location="Moscow",
            title="Backend Developer",
            summary="Experienced Python developer",
            skills=["Python", "Django", "PostgreSQL", "Docker"],
            experience_years=5,
            education="Computer Science, MSU",
            languages=["Russian", "English"],
            available_from=datetime.utcnow(),
            external_url="https://Mismatch.ru/candidates/789"
        )
        
        db_session.add(candidate)
        db_session.commit()
        
        retrieved = db_session.query(MismatchCandidate).filter_by(Mismatch_id="cand-789").first()
        assert retrieved is not None
        assert retrieved.first_name == "Ivan"
        assert retrieved.last_name == "Petrov"
        assert "Python" in retrieved.skills
    
    def test_candidate_contact_info(self, db_session: Session):
        """Test candidate contact information validation"""
        from app.models.Mismatch import MismatchCandidate
        
        candidate = MismatchCandidate(
            Mismatch_id="cand-new",
            email="maria@example.com",
            phone="+7 888 555 12 34"
        )
        
        db_session.add(candidate)
        db_session.commit()
        
        retrieved = db_session.query(MismatchCandidate).filter_by(Mismatch_id="cand-new").first()
        assert "@" in retrieved.email
        assert "+7" in retrieved.phone


class TestMismatchPlacementModel:
    """Test MismatchPlacement model"""
    
    def test_create_placement_model(self, db_session: Session):
        """Test creating a MismatchPlacement instance"""
        from app.models.Mismatch import MismatchPlacement
        
        placement = MismatchPlacement(
            Mismatch_id="plac-123",
            job_id="job-123",
            candidate_id="cand-789",
            status="submitted",
            match_score=0.87,
            submitted_at=datetime.utcnow(),
            feedback="Great match"
        )
        
        db_session.add(placement)
        db_session.commit()
        
        retrieved = db_session.query(MismatchPlacement).filter_by(Mismatch_id="plac-123").first()
        assert retrieved is not None
        assert retrieved.status == "submitted"
        assert retrieved.match_score > 0.8
    
    def test_placement_status_tracking(self, db_session: Session):
        """Test placement status transitions"""
        from app.models.Mismatch import MismatchPlacement
        
        placement = MismatchPlacement(
            Mismatch_id="plac-456",
            job_id="job-456",
            candidate_id="cand-456",
            status="submitted"
        )
        
        db_session.add(placement)
        db_session.commit()
        
        # Simulate status update
        placement.status = "viewed"
        db_session.commit()
        
        retrieved = db_session.query(MismatchPlacement).filter_by(Mismatch_id="plac-456").first()
        assert retrieved.status == "viewed"


class TestMismatchSyncModel:
    """Test MismatchSync model for tracking sync operations"""
    
    def test_create_sync_record(self, db_session: Session):
        """Test creating a MismatchSync tracking record"""
        from app.models.Mismatch import MismatchSync
        
        sync = MismatchSync(
            sync_type="full",
            status="completed",
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            jobs_synced=1000,
            candidates_synced=500,
            errors=5,
            error_log="5 minor sync errors"
        )
        
        db_session.add(sync)
        db_session.commit()
        
        retrieved = db_session.query(MismatchSync).filter_by(sync_type="full").first()
        assert retrieved is not None
        assert retrieved.status == "completed"
        assert retrieved.jobs_synced == 1000
    
    def test_sync_progress_tracking(self, db_session: Session):
        """Test sync progress tracking"""
        from app.models.Mismatch import MismatchSync
        
        sync = MismatchSync(
            sync_type="incremental",
            status="running",
            started_at=datetime.utcnow()
        )
        
        db_session.add(sync)
        db_session.commit()
        
        retrieved = db_session.query(MismatchSync).filter_by(sync_type="incremental").first()
        assert retrieved.status == "running"
        assert retrieved.started_at is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
