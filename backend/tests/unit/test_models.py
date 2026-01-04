import pytest
from app.models import User, Candidate, Job, Match
from werkzeug.security import check_password_hash

class TestUserModel:
    """Test cases for User model"""
    
    def test_user_creation(self, app):
        """Test user creation"""
        with app.app_context():
            user = User(email='test@example.com', name='Test User')
            user.set_password('password123')
            assert user.email == 'test@example.com'
            assert user.name == 'Test User'
            assert check_password_hash(user.password, 'password123')
    
    def test_password_hashing(self, app):
        """Test password is properly hashed"""
        with app.app_context():
            user = User(email='test@example.com')
            user.set_password('secret')
            assert user.password != 'secret'
            assert user.check_password('secret')
            assert not user.check_password('wrong')
    
    def test_user_email_required(self, app, test_user):
        """Test user requires email"""
        with app.app_context():
            assert test_user.email is not None

class TestCandidateModel:
    """Test cases for Candidate model"""
    
    def test_candidate_creation(self, app, test_user):
        """Test candidate creation"""
        with app.app_context():
            candidate = Candidate(
                user_id=test_user.id,
                skills=['Python', 'SQL'],
                experience_years=3
            )
            assert candidate.user_id == test_user.id
            assert 'Python' in candidate.skills
            assert candidate.experience_years == 3
    
    def test_candidate_skills(self, app, test_candidate):
        """Test candidate skills"""
        with app.app_context():
            assert isinstance(test_candidate.skills, list)
            assert len(test_candidate.skills) > 0

class TestJobModel:
    """Test cases for Job model"""
    
    def test_job_creation(self, app, test_user):
        """Test job creation"""
        with app.app_context():
            job = Job(
                user_id=test_user.id,
                title='Python Developer',
                description='Needed',
                required_skills=['Python'],
                salary_min=50000
            )
            assert job.title == 'Python Developer'
            assert job.user_id == test_user.id
            assert 'Python' in job.required_skills
    
    def test_job_salary_range(self, app, test_job):
        """Test job salary fields"""
        with app.app_context():
            assert test_job.salary_min is not None
            assert test_job.salary_max >= test_job.salary_min or test_job.salary_max is None

class TestMatchModel:
    """Test cases for Match model"""
    
    def test_match_creation(self, app, test_candidate, test_job):
        """Test match creation"""
        with app.app_context():
            match = Match(
                candidate_id=test_candidate.id,
                job_id=test_job.id,
                score=0.85
            )
            assert match.candidate_id == test_candidate.id
            assert match.job_id == test_job.id
            assert match.score == 0.85
    
    def test_match_score_validation(self, app, test_candidate, test_job):
        """Test match score is between 0 and 1"""
        with app.app_context():
            match = Match(
                candidate_id=test_candidate.id,
                job_id=test_job.id,
                score=0.75
            )
            assert 0 <= match.score <= 1

