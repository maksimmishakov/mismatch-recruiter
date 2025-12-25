"""Tests for Resume Parsing functionality.

Tests cover:
- Resume parsing model operations
- Resume parsing API endpoints
- Skill extraction
- Data persistence
"""

import pytest
from unittest.mock import Mock, patch
from app.models import ParsedResume, ResumeSkill, ResumeEducation, ResumeExperience, Job
from app.instance import db
from datetime import datetime


class TestParsedResumeModel:
    """Test ParsedResume model."""
    
    def test_create_parsed_resume(self, app):
        """Test creating a parsed resume record."""
        with app.app_context():
            job = Job.query.first()
            resume = ParsedResume(
                job_id=job.id,
                raw_text='Sample resume text',
                parsing_status='pending'
            )
            db.session.add(resume)
            db.session.commit()
            
            assert resume.id is not None
            assert resume.parsing_status == 'pending'
            assert resume.raw_text == 'Sample resume text'
    
    def test_resume_to_dict(self, app):
        """Test resume to_dict serialization."""
        with app.app_context():
            job = Job.query.first()
            resume = ParsedResume(
                job_id=job.id,
                raw_text='Sample resume',
                parsing_status='completed'
            )
            db.session.add(resume)
            db.session.commit()
            
            result = resume.to_dict()
            assert 'id' in result
            assert 'job_id' in result
            assert 'parsing_status' in result
            assert 'skills' in result
            assert isinstance(result['skills'], list)


class TestResumeSkillModel:
    """Test ResumeSkill model."""
    
    def test_create_resume_skill(self, app):
        """Test creating a resume skill."""
        with app.app_context():
            job = Job.query.first()
            resume = ParsedResume(
                job_id=job.id,
                raw_text='Sample resume',
                parsing_status='completed'
            )
            db.session.add(resume)
            db.session.flush()
            
            skill = ResumeSkill(
                resume_id=resume.id,
                skill_name='Python',
                skill_category='Programming',
                proficiency_level='Advanced',
                years_experience=5.0
            )
            db.session.add(skill)
            db.session.commit()
            
            assert skill.id is not None
            assert skill.skill_name == 'Python'
            assert skill.proficiency_level == 'Advanced'
    
    def test_skill_to_dict(self, app):
        """Test skill to_dict serialization."""
        with app.app_context():
            job = Job.query.first()
            resume = ParsedResume(
                job_id=job.id,
                raw_text='Sample resume',
                parsing_status='completed'
            )
            db.session.add(resume)
            db.session.flush()
            
            skill = ResumeSkill(
                resume_id=resume.id,
                skill_name='JavaScript',
                skill_category='Programming',
                proficiency_level='Intermediate'
            )
            db.session.add(skill)
            db.session.commit()
            
            result = skill.to_dict()
            assert result['skill_name'] == 'JavaScript'
            assert result['skill_category'] == 'Programming'
            assert result['proficiency_level'] == 'Intermediate'


class TestResumeParsingAPI:
    """Test Resume Parsing REST API endpoints."""
    
    def test_get_parsed_resume(self, client, app):
        """Test GET /api/resumes/<resume_id> endpoint."""
        with app.app_context():
            job = Job.query.first()
            resume = ParsedResume(
                job_id=job.id,
                raw_text='Sample resume',
                parsing_status='completed'
            )
            db.session.add(resume)
            db.session.commit()
            resume_id = resume.id
        
        response = client.get(f'/api/resumes/{resume_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == resume_id
        assert 'parsing_status' in data
    
    def test_get_nonexistent_resume(self, client):
        """Test GET endpoint with invalid resume ID."""
        response = client.get('/api/resumes/99999')
        assert response.status_code == 404
    
    def test_get_resume_skills(self, client, app):
        """Test GET /api/resumes/<resume_id>/skills endpoint."""
        with app.app_context():
            job = Job.query.first()
            resume = ParsedResume(
                job_id=job.id,
                raw_text='Sample resume',
                parsing_status='completed'
            )
            db.session.add(resume)
            db.session.flush()
            
            skill = ResumeSkill(
                resume_id=resume.id,
                skill_name='Python',
                skill_category='Programming'
            )
            db.session.add(skill)
            db.session.commit()
            resume_id = resume.id
        
        response = client.get(f'/api/resumes/{resume_id}/skills')
        assert response.status_code == 200
        data = response.get_json()
        assert data['resume_id'] == resume_id
        assert data['total'] == 1
        assert len(data['skills']) == 1
    
    def test_delete_parsed_resume(self, client, app):
        """Test DELETE /api/resumes/<resume_id> endpoint."""
        with app.app_context():
            job = Job.query.first()
            resume = ParsedResume(
                job_id=job.id,
                raw_text='Sample resume',
                parsing_status='completed'
            )
            db.session.add(resume)
            db.session.commit()
            resume_id = resume.id
        
        response = client.delete(f'/api/resumes/{resume_id}')
        assert response.status_code == 200
        
        # Verify it's deleted
        with app.app_context():
            deleted_resume = ParsedResume.query.get(resume_id)
            assert deleted_resume is None


class TestResumeEducationModel:
    """Test ResumeEducation model."""
    
    def test_create_resume_education(self, app):
        """Test creating a resume education record."""
        with app.app_context():
            job = Job.query.first()
            resume = ParsedResume(
                job_id=job.id,
                raw_text='Sample resume',
                parsing_status='completed'
            )
            db.session.add(resume)
            db.session.flush()
            
            education = ResumeEducation(
                resume_id=resume.id,
                school_name='MIT',
                degree='Bachelor',
                field_of_study='Computer Science',
                start_date='2016-09',
                end_date='2020-06',
                gpa=3.8
            )
            db.session.add(education)
            db.session.commit()
            
            assert education.id is not None
            assert education.school_name == 'MIT'
            assert education.gpa == 3.8


class TestResumeExperienceModel:
    """Test ResumeExperience model."""
    
    def test_create_resume_experience(self, app):
        """Test creating a resume experience record."""
        with app.app_context():
            job = Job.query.first()
            resume = ParsedResume(
                job_id=job.id,
                raw_text='Sample resume',
                parsing_status='completed'
            )
            db.session.add(resume)
            db.session.flush()
            
            experience = ResumeExperience(
                resume_id=resume.id,
                company_name='Tech Corp',
                job_title='Software Engineer',
                start_date='2020-07',
                end_date='2023-12',
                duration_months=42,
                description='Developed backend systems'
            )
            db.session.add(experience)
            db.session.commit()
            
            assert experience.id is not None
            assert experience.company_name == 'Tech Corp'
            assert experience.duration_months == 42
