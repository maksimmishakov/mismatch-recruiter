from app import create_app, db
from app.models import User, Candidate, Job, Match
from datetime import datetime
import json

def init_db():
    """
    Initialize database with test data for development
    """
    app = create_app('development')
    
    with app.app_context():
        # Drop all tables (WARNING: This will delete all data!)
        print("Dropping all tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating all tables...")
        db.create_all()
        print("✅ Database tables created")
        
        # Create test users
        users = [
            User(
                username='recruiter1',
                email='recruiter@mismatch.ai',
                full_name='Ivan Recruiter',
                role='recruiter',
                is_active=True
            ),
            User(
                username='admin',
                email='admin@mismatch.ai',
                full_name='Admin User',
                role='admin',
                is_active=True
            ),
        ]
        
        # Set passwords (using the set_password method for hashing)
        users[0].set_password('recruiter_pass_123')
        users[1].set_password('admin_pass_456')
        
        for user in users:
            db.session.add(user)
        
        db.session.commit()
        print(f"✅ {len(users)} users created")
        
        # Create test candidates
        candidates = [
            Candidate(
                name='Aleksandr Ivanov',
                email='alex.ivanov@example.com',
                phone='+79991234567',
                skills=['Python', 'FastAPI', 'PostgreSQL', 'Docker'],
                experience_years=5,
                current_position='Senior Backend Developer',
                status='active'
            ),
            Candidate(
                name='Maria Petrova',
                email='maria.petrova@example.com',
                phone='+79997654321',
                skills=['React', 'TypeScript', 'Node.js', 'GraphQL'],
                experience_years=4,
                current_position='Frontend Developer',
                status='active'
            ),
            Candidate(
                name='Ivan Sidorov',
                email='ivan.sidorov@example.com',
                phone='+79995555555',
                skills=['Python', 'Django', 'React', 'AWS'],
                experience_years=3,
                current_position='Full Stack Developer',
                status='active'
            ),
            Candidate(
                name='Elena Volkova',
                email='elena.volkova@example.com',
                phone='+79992222222',
                skills=['Python', 'Machine Learning', 'TensorFlow', 'Pandas'],
                experience_years=6,
                current_position='ML Engineer',
                status='active'
            ),
            Candidate(
                name='Dmitry Orlov',
                email='dmitry.orlov@example.com',
                phone='+79993333333',
                skills=['Go', 'Rust', 'C++'],
                experience_years=7,
                current_position='Systems Engineer',
                status='active'
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
                description='Looking for experienced Python developer with FastAPI knowledge and 5+ years experience',
                required_skills=['Python', 'FastAPI', 'PostgreSQL', 'Docker'],
                required_experience=5,
                salary_min=150000,
                salary_max=200000,
                location='Moscow',
                company='TechCorp',
                status='open'
            ),
            Job(
                title='React Frontend Developer',
                description='Seeking Frontend developer with React and TypeScript expertise for modern web apps',
                required_skills=['React', 'TypeScript', 'CSS', 'REST API'],
                required_experience=3,
                salary_min=100000,
                salary_max=150000,
                location='Saint Petersburg',
                company='WebStudio',
                status='open'
            ),
            Job(
                title='Full Stack Developer',
                description='Building SaaS applications - need experienced full stack engineer with diverse skills',
                required_skills=['Python', 'React', 'PostgreSQL', 'AWS'],
                required_experience=4,
                salary_min=130000,
                salary_max=180000,
                location='Remote',
                company='StartupXYZ',
                status='open'
            ),
            Job(
                title='ML Engineer',
                description='Machine learning engineer for computer vision projects and data processing',
                required_skills=['Python', 'Machine Learning', 'TensorFlow', 'OpenCV'],
                required_experience=5,
                salary_min=160000,
                salary_max=220000,
                location='Moscow',
                company='AILabs',
                status='open'
            ),
            Job(
                title='Systems Engineer',
                description='Low-level systems programming in Go/Rust for high-performance services',
                required_skills=['Go', 'Rust', 'C++', 'Linux'],
                required_experience=6,
                salary_min=170000,
                salary_max=240000,
                location='Remote',
                company='SystemsCo',
                status='open'
            ),
        ]
        
        for job in jobs:
            db.session.add(job)
        
        db.session.commit()
        print(f"✅ {len(jobs)} jobs created")
        
        # Create test matches
        matches = [
            Match(candidate_id=1, job_id=1, match_score=95.0, status='pending'),
            Match(candidate_id=2, job_id=2, match_score=90.0, status='pending'),
            Match(candidate_id=3, job_id=3, match_score=87.5, status='pending'),
            Match(candidate_id=4, job_id=4, match_score=92.0, status='pending'),
            Match(candidate_id=5, job_id=5, match_score=94.0, status='pending'),
            Match(candidate_id=1, job_id=3, match_score=78.0, status='declined'),
            Match(candidate_id=2, job_id=1, match_score=65.0, status='declined'),
        ]
        
        for match in matches:
            db.session.add(match)
        
        db.session.commit()
        print(f"✅ {len(matches)} matches created")
        
        print("✅\n Database initialized successfully!")
        print(f"✅ Total records:")
        print(f"  - Users: {User.query.count()}")
        print(f"  - Candidates: {Candidate.query.count()}")
        print(f"  - Jobs: {Job.query.count()}")
        print(f"  - Matches: {Match.query.count()}")

if __name__ == '__main__':
    init_db()
