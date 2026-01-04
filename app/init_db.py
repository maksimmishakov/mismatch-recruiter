#!/usr/bin/env python
"""
Initialize database with schema and seed data
"""
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db
from app.models import User, Candidate, Job, Match, Feedback
from app.main import create_app

def init_db():
    """
    Initialize database:
    1. Drop all existing tables
    2. Create all tables from models
    3. Add seed data
    """
    print("\n" + "="*60)
    print("INITIALIZING DATABASE")
    print("="*60)
    
    # Create app context
    app = create_app()
    
    with app.app_context():
        # Drop all tables
        print("\n[1/3] Dropping existing tables...")
        db.drop_all()
        print("✓ All tables dropped")
        
        # Create all tables
        print("\n[2/3] Creating database schema...")
        db.create_all()
        print("✓ Database schema created")
        print("  - Users table")
        print("  - Candidates table")
        print("  - Jobs table")
        print("  - Matches table")
        print("  - Feedback table")
        
        # Add seed data
        print("\n[3/3] Adding seed data...")
        
        # Create test users
        admin = User(
            username='admin',
            email='admin@mismatch.local',
            password_hash='hashed_password_123',
            role='admin'
        )
        recruiter = User(
            username='recruiter1',
            email='recruiter@mismatch.local',
            password_hash='hashed_password_456',
            role='recruiter'
        )
        
        db.session.add(admin)
        db.session.add(recruiter)
        db.session.commit()
        print("✓ Created 2 test users")
        
        # Create test candidates
        candidate1 = Candidate(
            name='Alice Johnson',
            email='alice@example.com',
            phone='+7-999-123-45-67',
            resume_text='Experienced Python developer with 5 years experience',
            skills='Python,Flask,PostgreSQL,React',
            experience_years=5,
            current_position='Senior Developer',
            current_company='Tech Corp',
            salary_expectation=150000,
            location='Moscow',
            availability='Immediate'
        )
        candidate2 = Candidate(
            name='Bob Smith',
            email='bob@example.com',
            phone='+7-999-234-56-78',
            resume_text='Full-stack developer specializing in MERN stack',
            skills='JavaScript,React,Node.js,MongoDB',
            experience_years=3,
            current_position='Developer',
            current_company='StartUp Inc',
            salary_expectation=120000,
            location='Saint Petersburg',
            availability='2 weeks notice'
        )
        
        db.session.add(candidate1)
        db.session.add(candidate2)
        db.session.commit()
        print("✓ Created 2 test candidates")
        
        # Create test jobs
        job1 = Job(
            title='Senior Python Developer',
            description='Looking for experienced Python developer',
            company='Tech Corp',
            location='Moscow',
            salary_min=140000,
            salary_max=180000,
            required_skills='Python,Flask,PostgreSQL',
            experience_required=5,
            status='active',
            posted_date=datetime.utcnow()
        )
        job2 = Job(
            title='Frontend Developer',
            description='React specialist needed',
            company='Web Solutions',
            location='Remote',
            salary_min=100000,
            salary_max=140000,
            required_skills='React,JavaScript,CSS',
            experience_required=3,
            status='active',
            posted_date=datetime.utcnow()
        )
        
        db.session.add(job1)
        db.session.add(job2)
        db.session.commit()
        print("✓ Created 2 test job postings")
        
        print("\n" + "="*60)
        print("DATABASE INITIALIZED SUCCESSFULLY!")
        print("="*60)
        print("\nSeed Data Summary:")
        print(f"  - Users: {User.query.count()}")
        print(f"  - Candidates: {Candidate.query.count()}")
        print(f"  - Jobs: {Job.query.count()}")
        print(f"  - Matches: {Match.query.count()}")
        print(f"  - Feedback: {Feedback.query.count()}")
        print()

if __name__ == '__main__':
    init_db()
