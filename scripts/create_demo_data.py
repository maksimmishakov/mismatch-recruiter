#!/usr/bin/env python
"""Script to create demo data for MisMatch Recruiter"""
import sys
sys.path.insert(0, '/workspaces/mismatch-recruiter')

from app import create_app, db
from app.models import User, Candidate, Job, Match
from datetime import datetime

def create_demo_data():
    """Create demo data for testing and demo purposes"""
    app = create_app('production')
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.session.query(Match).delete()
        db.session.query(Candidate).delete()
        db.session.query(Job).delete()
        db.session.query(User).delete()
        db.session.commit()
        print("✓ Cleared existing data")
        
        # Create demo recruiter
        print("\nCreating demo recruiter...")
        recruiter = User(
            email='recruiter@mismatch.io',
            name='John Smith (Demo)',
        )
        recruiter.set_password('demo123456')
        db.session.add(recruiter)
        db.session.commit()
        print(f"✓ Created recruiter: {recruiter.email}")
        
        # Create demo candidates
        print("\nCreating demo candidates...")
        candidates_data = [
            {
                'name': 'Alice Johnson',
                'email': 'alice@example.com',
                'experience_years': 7,
                'skills': ['Python', 'Django', 'PostgreSQL', 'Redis'],
                'languages': ['English', 'Russian']
            },
            {
                'name': 'Bob Williams',
                'email': 'bob@example.com',
                'experience_years': 5,
                'skills': ['JavaScript', 'React', 'Node.js', 'MongoDB'],
                'languages': ['English']
            },
            {
                'name': 'Carol Chen',
                'email': 'carol@example.com',
                'experience_years': 8,
                'skills': ['Python', 'Go', 'Kubernetes', 'AWS'],
                'languages': ['English', 'Mandarin']
            },
            {
                'name': 'David Brown',
                'email': 'david@example.com',
                'experience_years': 3,
                'skills': ['Java', 'Spring Boot', 'Docker'],
                'languages': ['English']
            },
        ]
        
        candidates = []
        for data in candidates_data:
            candidate = Candidate(
                name=data['name'],
                email=data['email'],
                experience_years=data['experience_years'],
                skills=data['skills'],
                languages=data['languages'],
                recruiter_id=recruiter.id
            )
            db.session.add(candidate)
            candidates.append(candidate)
            print(f"  ✓ {data['name']} ({data['experience_years']} years)")
        
        db.session.commit()
        print(f"✓ Created {len(candidates)} candidates")
        
        # Create demo jobs
        print("\nCreating demo jobs...")
        jobs_data = [
            {
                'title': 'Senior Python Developer',
                'description': 'Looking for experienced Python developer with Django expertise',
                'required_skills': ['Python', 'Django', 'PostgreSQL'],
                'salary_range': '180k-220k RUB',
                'location': 'Moscow'
            },
            {
                'title': 'Frontend React Developer',
                'description': 'We need skilled React developer for exciting web project',
                'required_skills': ['JavaScript', 'React', 'CSS'],
                'salary_range': '150k-190k RUB',
                'location': 'Remote'
            },
            {
                'title': 'DevOps Engineer',
                'description': 'Kubernetes and cloud infrastructure specialist needed',
                'required_skills': ['Kubernetes', 'Docker', 'AWS'],
                'salary_range': '200k-250k RUB',
                'location': 'Moscow'
            },
            {
                'title': 'Backend Java Developer',
                'description': 'Java Spring Boot developer for enterprise application',
                'required_skills': ['Java', 'Spring Boot', 'Microservices'],
                'salary_range': '170k-210k RUB',
                'location': 'Saint Petersburg'
            },
        ]
        
        jobs = []
        for data in jobs_data:
            job = Job(
                title=data['title'],
                description=data['description'],
                required_skills=data['required_skills'],
                salary_range=data['salary_range'],
                location=data['location'],
                recruiter_id=recruiter.id
            )
            db.session.add(job)
            jobs.append(job)
            print(f"  ✓ {data['title']}")
        
        db.session.commit()
        print(f"✓ Created {len(jobs)} job positions")
        
        # Create demo matches
        print("\nCreating demo matches...")
        match_count = 0
        for job in jobs:
            for candidate in candidates:
                # Simple matching based on skill overlap
                job_skills = set(job.required_skills)
                candidate_skills = set(candidate.skills)
                matching_skills = job_skills.intersection(candidate_skills)
                
                if matching_skills:
                    match_score = len(matching_skills) / len(job_skills)
                    match = Match(
                        candidate_id=candidate.id,
                        job_id=job.id,
                        match_score=match_score,
                        reasoning=f"Matches {len(matching_skills)}/{len(job_skills)} required skills: {', '.join(matching_skills)}",
                        status='pending'
                    )
                    db.session.add(match)
                    match_count += 1
        
        db.session.commit()
        print(f"✓ Created {match_count} candidate-job matches")
        
        # Print summary
        print("\n" + "="*60)
        print("DEMO DATA CREATED SUCCESSFULLY")
        print("="*60)
        print(f"Recruiter: {recruiter.email} (password: demo123456)")
        print(f"Candidates: {len(candidates)}")
        print(f"Job Positions: {len(jobs)}")
        print(f"Matches: {match_count}")
        print("\nReady for staging demo!")
        print("="*60)

if __name__ == '__main__':
    create_demo_data()
