"""Tests for database models."""
import pytest
from app.models import User, Candidate, Job, Match
from werkzeug.security import check_password_hash


class TestUserModel:
    """Test User model functionality."""
    
    def test_user_creation(self, db_session):
        """Test creating a new user."""
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash='hashed_password'
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == 'user'
        assert user.is_active is True
    
    def test_user_unique_email(self, db_session):
        """Test that email must be unique."""
        user1 = User(
            username='user1',
            email='duplicate@example.com',
            password_hash='hash1'
        )
        user2 = User(
            username='user2',
            email='duplicate@example.com',
            password_hash='hash2'
        )
        db_session.add(user1)
        db_session.commit()
        db_session.add(user2)
        
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()


class TestCandidateModel:
    """Test Candidate model functionality."""
    
    def test_candidate_creation(self, db_session):
        """Test creating a new candidate."""
        candidate = Candidate(
            name='John Doe',
            email='john@example.com',
            phone='+1234567890',
            experience_years=5,
            skills=['Python', 'JavaScript', 'React']
        )
        db_session.add(candidate)
        db_session.commit()
        
        assert candidate.id is not None
        assert candidate.name == 'John Doe'
        assert candidate.experience_years == 5
        assert 'Python' in candidate.skills
    
    def test_candidate_optional_fields(self, db_session):
        """Test that optional fields can be null."""
        candidate = Candidate(
            name='Jane Doe',
            email='jane@example.com'
        )
        db_session.add(candidate)
        db_session.commit()
        
        assert candidate.phone is None
        assert candidate.resume_url is None


class TestJobModel:
    """Test Job model functionality."""
    
    def test_job_creation(self, db_session):
        """Test creating a new job posting."""
        job = Job(
            title='Senior Python Developer',
            description='We are looking for a senior Python developer...',
            required_skills=['Python', 'Flask', 'PostgreSQL'],
            salary_min=100000,
            salary_max=150000
        )
        db_session.add(job)
        db_session.commit()
        
        assert job.id is not None
        assert job.title == 'Senior Python Developer'
        assert job.status == 'open'
        assert job.salary_min == 100000
    
    def test_job_status_default(self, db_session):
        """Test that job status defaults to 'open'."""
        job = Job(
            title='Test Job',
            description='Test description'
        )
        db_session.add(job)
        db_session.commit()
        
        assert job.status == 'open'


class TestMatchModel:
    """Test Match model functionality."""
    
    def test_match_creation(self, db_session):
        """Test creating a match between candidate and job."""
        candidate = Candidate(name='Test', email='test@example.com')
        job = Job(title='Test Job', description='Test')
        
        db_session.add(candidate)
        db_session.add(job)
        db_session.flush()
        
        match = Match(
            candidate_id=candidate.id,
            job_id=job.id,
            score=0.85,
            status='pending'
        )
        db_session.add(match)
        db_session.commit()
        
        assert match.id is not None
        assert match.score == 0.85
        assert match.status == 'pending'
    
    def test_match_unique_constraint(self, db_session):
        """Test that candidate-job pair must be unique."""
        candidate = Candidate(name='Test', email='test@example.com')
        job = Job(title='Test Job', description='Test')
        
        db_session.add(candidate)
        db_session.add(job)
        db_session.flush()
        
        match1 = Match(candidate_id=candidate.id, job_id=job.id, score=0.8)
        match2 = Match(candidate_id=candidate.id, job_id=job.id, score=0.9)
        
        db_session.add(match1)
        db_session.commit()
        db_session.add(match2)
        
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
