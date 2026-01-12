#!/usr/bin/env python3
"""
Demo Data Generation Script
Generates sample data for LAMODA Recruiter application demonstrations
"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_demo_data():
    """Generate demo data for the application"""
    print("🎯 LAMODA Recruiter - Demo Data Generation")
    print("=" * 50)
    
    # Sample candidate data
    candidates = [
        {
            'first_name': 'Александр',
            'last_name': 'Петров',
            'email': 'alexander.petrov@example.com',
            'skills': ['Python', 'JavaScript', 'React', 'PostgreSQL'],
            'experience_years': 5,
            'location': 'Москва',
            'specialization': 'Full Stack Developer'
        },
        {
            'first_name': 'Мария',
            'last_name': 'Иванова',
            'email': 'maria.ivanova@example.com',
            'skills': ['Python', 'Django', 'Data Science', 'Machine Learning'],
            'experience_years': 4,
            'location': 'Санкт-Петербург',
            'specialization': 'Backend Developer'
        },
        {
            'first_name': 'Иван',
            'last_name': 'Сидоров',
            'email': 'ivan.sidorov@example.com',
            'skills': ['React', 'TypeScript', 'CSS', 'HTML'],
            'experience_years': 3,
            'location': 'Москва',
            'specialization': 'Frontend Developer'
        },
        {
            'first_name': 'Елена',
            'last_name': 'Смирнова',
            'email': 'elena.smirnova@example.com',
            'skills': ['Java', 'Spring Boot', 'Microservices'],
            'experience_years': 6,
            'location': 'Екатеринбург',
            'specialization': 'Java Developer'
        },
        {
            'first_name': 'Денис',
            'last_name': 'Козлов',
            'email': 'denis.kozlov@example.com',
            'skills': ['DevOps', 'Docker', 'Kubernetes', 'AWS'],
            'experience_years': 4,
            'location': 'Москва',
            'specialization': 'DevOps Engineer'
        },
    ]
    
    # Sample job postings
    jobs = [
        {
            'title': 'Senior Python Developer',
            'description': 'Требуется опытный Python разработчик для проекта LAMODA',
            'company': 'LAMODA',
            'location': 'Москва',
            'salary_min': 150000,
            'salary_max': 250000,
            'required_skills': ['Python', 'PostgreSQL', 'Django'],
            'experience_years': 5
        },
        {
            'title': 'Frontend Developer (React)',
            'description': 'Ищем Frontend разработчика с опытом React',
            'company': 'LAMODA',
            'location': 'Москва',
            'salary_min': 120000,
            'salary_max': 180000,
            'required_skills': ['React', 'JavaScript', 'TypeScript'],
            'experience_years': 3
        },
        {
            'title': 'Data Scientist',
            'description': 'Приглашаем Data Scientist для аналитики',
            'company': 'LAMODA',
            'location': 'Санкт-Петербург',
            'salary_min': 140000,
            'salary_max': 220000,
            'required_skills': ['Python', 'Machine Learning', 'Data Science'],
            'experience_years': 4
        },
        {
            'title': 'DevOps Engineer',
            'description': 'Требуется DevOps специалист',
            'company': 'LAMODA',
            'location': 'Москва',
            'salary_min': 130000,
            'salary_max': 200000,
            'required_skills': ['Docker', 'Kubernetes', 'AWS'],
            'experience_years': 4
        },
        {
            'title': 'Java Backend Developer',
            'description': 'Java разработчик для микросервисов',
            'company': 'LAMODA',
            'location': 'Екатеринбург',
            'salary_min': 140000,
            'salary_max': 210000,
            'required_skills': ['Java', 'Spring Boot', 'Microservices'],
            'experience_years': 5
        },
    ]
    
    print(f"\n📊 Demo Data Overview")
    print(f"  Candidates: {len(candidates)}")
    print(f"  Job Postings: {len(jobs)}")
    print(f"  Total Potential Matches: {len(candidates) * len(jobs)}")
    
    print(f"\n✅ Sample Candidates:")
    for candidate in candidates:
        print(f"  • {candidate['first_name']} {candidate['last_name']} ({candidate['specialization']})")
    
    print(f"\n✅ Sample Job Postings:")
    for job in jobs:
        print(f"  • {job['title']} @ {job['company']} ({job['location']})")
    
    print(f"\n✅ Salary Range Analysis:")
    salary_ranges = [(j['salary_min'], j['salary_max']) for j in jobs]
    min_salary = min(r[0] for r in salary_ranges)
    max_salary = max(r[1] for r in salary_ranges)
    print(f"  Min Salary: ₽{min_salary:,.0f}")
    print(f"  Max Salary: ₽{max_salary:,.0f}")
    print(f"  Average Min: ₽{sum(r[0] for r in salary_ranges) // len(salary_ranges):,.0f}")
    print(f"  Average Max: ₽{sum(r[1] for r in salary_ranges) // len(salary_ranges):,.0f}")
    
    print(f"\n✅ Location Distribution:")
    locations = set()
    for candidate in candidates:
        locations.add(candidate['location'])
    for location in sorted(locations):
        count = sum(1 for c in candidates if c['location'] == location)
        print(f"  • {location}: {count} candidates")
    
    print(f"\n🎉 Demo Data Generation Complete!")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Status: ✅ Ready for demonstration")
    return candidates, jobs

if __name__ == '__main__':
    try:
        candidates, jobs = generate_demo_data()
        print("\n📈 LAMODA Demo Data Ready for Presentation")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error generating demo data: {e}")
        sys.exit(1)

