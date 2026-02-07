"""Comprehensive unit tests for all models."""
import pytest
from datetime import datetime, timedelta
from app.models import User, Resume, Job, Subscription, HealthCheck
from app.database import get_db
from sqlalchemy.exc import IntegrityError


class TestUserModel:
    """Test cases for User model."""
    
    def test_user_creation_valid(self, test_db):
        """Test creating a user with valid data."""
        user = User(
            email="test@example.com",
            name="Test User",
            subscription_plan="free"
        )
        user.set_password("SecurePassword123")
        
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.subscription_plan == "free"
        assert user.is_active is True
        assert user.created_at is not None
        
    def test_user_password_hashing(self, test_db):
        """Test that passwords are properly hashed."""
        user = User(email="hash@test.com", name="Hash Test")
        plain_password = "MyPassword123"
        user.set_password(plain_password)
        
        assert user.password_hash != plain_password
        assert user.password_hash is not None
        assert len(user.password_hash) > 20
        
    def test_user_password_verification(self, test_db):
        """Test password verification method."""
        user = User(email="verify@test.com", name="Verify Test")
        password = "CorrectPassword123"
        user.set_password(password)
        
        assert user.verify_password(password) is True
        assert user.verify_password("WrongPassword") is False
        assert user.verify_password("") is False
        
    def test_user_email_unique_constraint(self, test_db):
        """Test that email must be unique."""
        user1 = User(email="unique@test.com", name="User 1")
        user1.set_password("password")
        test_db.add(user1)
        test_db.commit()
        
        user2 = User(email="unique@test.com", name="User 2")
        user2.set_password("password")
        test_db.add(user2)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_user_email_required(self, test_db):
        """Test that email is required."""
        user = User(name="No Email User")
        test_db.add(user)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_user_default_values(self, test_db):
        """Test default values for user fields."""
        user = User(email="defaults@test.com", name="Default Test")
        user.set_password("password")
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        assert user.subscription_plan == "free"
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None
        
    def test_user_password_max_length(self, test_db):
        """Test that very long passwords are handled correctly."""
        user = User(email="longpass@test.com", name="Long Pass")
        # bcrypt has a 72 byte limit
        long_password = "a" * 100
        
        try:
            user.set_password(long_password)
            # Password should be truncated or handled
            assert user.password_hash is not None
        except Exception as e:
            pytest.fail(f"Password setting failed: {str(e)}")
    
    def test_user_is_active_toggle(self, test_db):
        """Test toggling user active status."""
        user = User(email="active@test.com", name="Active Test")
        user.set_password("password")
        test_db.add(user)
        test_db.commit()
        
        assert user.is_active is True
        
        user.is_active = False
        test_db.commit()
        test_db.refresh(user)
        
        assert user.is_active is False


class TestResumeModel:
    """Test cases for Resume model."""
    
    def test_resume_creation_valid(self, test_db, test_user):
        """Test creating a resume with valid data."""
        resume = Resume(
            user_id=test_user.id,
            file_path="/uploads/resume.pdf",
            parsed_data={"skills": ["Python", "SQL"]}
        )
        
        test_db.add(resume)
        test_db.commit()
        test_db.refresh(resume)
        
        assert resume.id is not None
        assert resume.user_id == test_user.id
        assert resume.file_path == "/uploads/resume.pdf"
        assert resume.parsed_data["skills"] == ["Python", "SQL"]
        assert resume.created_at is not None
        
    def test_resume_user_relationship(self, test_db, test_user):
        """Test resume-user relationship."""
        resume = Resume(
            user_id=test_user.id,
            file_path="/uploads/test.pdf"
        )
        test_db.add(resume)
        test_db.commit()
        test_db.refresh(resume)
        
        assert resume.user is not None
        assert resume.user.id == test_user.id
        assert resume.user.email == test_user.email
        
    def test_resume_cascade_delete(self, test_db):
        """Test that resumes are deleted when user is deleted."""
        user = User(email="cascade@test.com", name="Cascade Test")
        user.set_password("password")
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        resume = Resume(user_id=user.id, file_path="/test.pdf")
        test_db.add(resume)
        test_db.commit()
        resume_id = resume.id
        
        test_db.delete(user)
        test_db.commit()
        
        deleted_resume = test_db.query(Resume).filter_by(id=resume_id).first()
        assert deleted_resume is None


class TestJobModel:
    """Test cases for Job model."""
    
    def test_job_creation_valid(self, test_db, test_user):
        """Test creating a job with valid data."""
        job = Job(
            user_id=test_user.id,
            title="Software Engineer",
            description="Python developer position",
            requirements={"experience": "2+ years", "skills": ["Python"]}
        )
        
        test_db.add(job)
        test_db.commit()
        test_db.refresh(job)
        
        assert job.id is not None
        assert job.user_id == test_user.id
        assert job.title == "Software Engineer"
        assert job.description == "Python developer position"
        assert job.created_at is not None
        
    def test_job_title_required(self, test_db, test_user):
        """Test that job title is required."""
        job = Job(user_id=test_user.id, description="No title job")
        test_db.add(job)
        
        with pytest.raises(IntegrityError):
            test_db.commit()


class TestSubscriptionModel:
    """Test cases for Subscription model."""
    
    def test_subscription_creation_valid(self, test_db, test_user):
        """Test creating a subscription with valid data."""
        subscription = Subscription(
            user_id=test_user.id,
            plan="premium",
            stripe_customer_id="cus_test123",
            status="active"
        )
        
        test_db.add(subscription)
        test_db.commit()
        test_db.refresh(subscription)
        
        assert subscription.id is not None
        assert subscription.user_id == test_user.id
        assert subscription.plan == "premium"
        assert subscription.status == "active"
        
    def test_subscription_expiration_logic(self, test_db, test_user):
        """Test subscription expiration date logic."""
        future_date = datetime.utcnow() + timedelta(days=30)
        subscription = Subscription(
            user_id=test_user.id,
            plan="premium",
            expires_at=future_date
        )
        
        test_db.add(subscription)
        test_db.commit()
        test_db.refresh(subscription)
        
        # Check if subscription is not expired
        assert subscription.expires_at > datetime.utcnow()


class TestHealthCheckModel:
    """Test cases for HealthCheck model."""
    
    def test_healthcheck_creation(self, test_db, test_user):
        """Test creating a health check record."""
        health_check = HealthCheck(
            user_id=test_user.id,
            status="healthy",
            response_time=0.15
        )
        
        test_db.add(health_check)
        test_db.commit()
        test_db.refresh(health_check)
        
        assert health_check.id is not None
        assert health_check.user_id == test_user.id
        assert health_check.status == "healthy"
        assert health_check.response_time == 0.15
        assert health_check.checked_at is not None


# Fixtures
@pytest.fixture
def test_db(monkeypatch):
    """Create a test database session."""
    # This would typically be configured in conftest.py
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture
def test_user(test_db):
    """Create a test user."""
    user = User(
        email="testuser@example.com",
        name="Test User",
        subscription_plan="free"
    )
    user.set_password("TestPassword123")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user
