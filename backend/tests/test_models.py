from app.models import User, Candidate, Job, Match
from app import db

def test_user_model(app):
    """Test User model"""
    user = User(
        email='test@example.com',
        username='testuser',
        first_name='Test', last_name='User'
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    
    assert user.id is not None
    assert user.verify_password('password123')
    assert not user.verify_password('wrongpassword')

def test_candidate_model(app):
    """Test Candidate model"""
    candidate = Candidate(
        first_name='John',
        last_name='Doe',
        email='john@example.com',
        skills=['Python', 'Flask'],
        experience_years=5
    )
    db.session.add(candidate)
    db.session.commit()
    
    assert candidate.id is not None
    assert candidate.first_name == 'John'
    assert 'Python' in candidate.skills

def test_job_posting_model(app):
    """Test Job model"""
    job = Job(
        title='Python Developer',
        description='We are looking for a Python developer',
        company='TechCorp',
        required_skills=['Python', 'Flask'],
        experience_level='mid'
    )
    db.session.add(job)
    db.session.commit()
    
    assert job.id is not None
    assert job.title == 'Python Developer'
    assert job.is_active is True

def test_match_model(app, test_candidate, test_job):
    """Test Match model"""
    match = Match(
        candidate_id=test_candidate.id,
        job_posting_id=test_job.id,
        match_score=0.85,
        skill_match=0.9,
        experience_match=0.8,
        status='pending'
    )
    db.session.add(match)
    db.session.commit()
    
    assert match.id is not None
    assert match.match_score == 0.85
    assert match.status == 'pending'
