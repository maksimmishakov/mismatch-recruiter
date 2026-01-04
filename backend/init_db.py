from app import create_app, db
from app.models import User, Candidate, Job, Match
from werkzeug.security import generate_password_hash
import json

def init_db():
    """Initialize database with test data"""
    app = create_app('development')
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Create test candidates
        candidates = [
            Candidate(
                first_name='Aleksandr',
                last_name='Ivanov',
                email='alex@example.com',
                phone='+79991234567',
                bio='Senior Backend Developer with 5+ years of experience',
                location='Moscow'
            ),
            Candidate(
                first_name='Maria',
                last_name='Petrova',
                email='maria@example.com',
                phone='+79997654321',
                bio='Frontend Developer specializing in React',
                location='SPB'
            ),
            Candidate(
                first_name='Ivan',
                last_name='Sidorov',
                email='ivan@example.com',
                phone='+79995555555',
                bio='Full Stack Developer with AWS expertise',
                location='Moscow'
            ),
            Candidate(
                first_name='Elena',
                last_name='Volkova',
                email='elena@example.com',
                phone='+79992222222',
                bio='Machine Learning Engineer',
                location='Remote'
            ),
        ]
        for candidate in candidates:
            db.session.add(candidate)
        
        db.session.commit()
        print(f"✅ {len(candidates)} candidates created")
        
        # Create test jobs
        jobs = [
            Job(
                title='Senior Python Developer',
                description='Looking for experienced Python developer with FastAPI knowledge',
                company='TechCorp',
                location='Moscow',
                salary_min=150000,
                salary_max=200000,
                job_type='full-time',
                required_skills=json.dumps(['Python', 'FastAPI', 'PostgreSQL', 'Docker'])
            ),
            Job(
                title='React Developer',
                description='Seeking Frontend developer with React and TypeScript expertise',
                company='WebStudio',
                location='SPB',
                salary_min=100000,
                salary_max=150000,
                job_type='full-time',
                required_skills=json.dumps(['React', 'TypeScript', 'CSS'])
            ),
            Job(
                title='Full Stack Developer',
                description='Building SaaS applications - need experienced full stack engineer',
                company='StartupXYZ',
                location='Remote',
                salary_min=130000,
                salary_max=180000,
                job_type='full-time',
                required_skills=json.dumps(['Python', 'React', 'PostgreSQL', 'AWS'])
            ),
            Job(
                title='ML Engineer',
                description='Machine learning engineer for computer vision projects',
                company='AILabs',
                location='Moscow',
                salary_min=160000,
                salary_max=220000,
                job_type='full-time',
                required_skills=json.dumps(['Python', 'Machine Learning', 'TensorFlow'])
            ),
        ]
        for job in jobs:
            db.session.add(job)
        
        db.session.commit()
        print(f"✅ {len(jobs)} jobs created")
        
        # Create test matches
        matches = [
            Match(candidate_id=1, job_id=1, match_score=95.0, matched_skills=json.dumps(['Python', 'FastAPI', 'PostgreSQL', 'Docker'])),
            Match(candidate_id=2, job_id=2, match_score=90.0, matched_skills=json.dumps(['React', 'TypeScript'])),
            Match(candidate_id=3, job_id=3, match_score=87.5, matched_skills=json.dumps(['Python', 'React', 'PostgreSQL'])),
            Match(candidate_id=4, job_id=4, match_score=92.0, matched_skills=json.dumps(['Python', 'Machine Learning'])),
        ]
        for match in matches:
            db.session.add(match)
        
        db.session.commit()
        print(f"✅ {len(matches)} matches created")
        print("✅ Database initialized successfully!")

if __name__ == '__main__':
    init_db()
