"""Resume Parsing API endpoints.

Provides REST endpoints for:
- Triggering resume parsing tasks
- Retrieving parsed resume data
- Managing resume parsing workflows
"""

from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from app.models import (
    Job, ParsedResume, ResumeSkill, ResumeEducation, ResumeExperience
)
from app.services.parsing.resume_parser_advanced import ResumeParserAdvanced
from app.tasks.resume_parse import parse_resume_task
from app.instance import db
from app.logger import logger

# Create blueprint
resume_parsing_bp = Blueprint('resume_parsing', __name__, url_prefix='/api/resumes')


@resume_parsing_bp.route('/<int:job_id>/parse', methods=['POST'])
def trigger_resume_parsing(job_id):
    """Trigger resume parsing for a job's resumes.
    
    Args:
        job_id: Job ID to parse resumes for
        
    Returns:
        JSON with parsing task info
    """
    try:
        # Verify job exists
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # Create parsed resume record
        resume_text = request.get_json().get('resume_text', '')
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
        
        # Create ParsedResume instance
        parsed_resume = ParsedResume(
            job_id=job_id,
            raw_text=resume_text,
            parsing_status='pending'
        )
        db.session.add(parsed_resume)
        db.session.commit()
        
        # Trigger async parsing task
        task = parse_resume_task.delay(parsed_resume.id, resume_text)
        
        logger.info(f'Resume parsing triggered for job {job_id}, resume {parsed_resume.id}')
        
        return jsonify({
            'resume_id': parsed_resume.id,
            'task_id': task.id,
            'status': 'pending'
        }), 202
        
    except Exception as e:
        logger.error(f'Error triggering resume parsing: {str(e)}')
        return jsonify({'error': str(e)}), 500


@resume_parsing_bp.route('/<int:resume_id>', methods=['GET'])
def get_parsed_resume(resume_id):
    """Get parsed resume data.
    
    Args:
        resume_id: Parsed resume ID
        
    Returns:
        JSON with resume data
    """
    try:
        resume = ParsedResume.query.options(
            joinedload(ParsedResume.skills),
            joinedload(ParsedResume.education),
            joinedload(ParsedResume.experience)
        ).get(resume_id)
        
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        return jsonify(resume.to_dict()), 200
        
    except Exception as e:
        logger.error(f'Error retrieving resume: {str(e)}')
        return jsonify({'error': str(e)}), 500


@resume_parsing_bp.route('/<int:resume_id>/skills', methods=['GET'])
def get_resume_skills(resume_id):
    """Get extracted skills from resume.
    
    Args:
        resume_id: Parsed resume ID
        
    Returns:
        JSON list of skills
    """
    try:
        resume = ParsedResume.query.get(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        skills = [skill.to_dict() for skill in resume.skills]
        return jsonify({
            'resume_id': resume_id,
            'skills': skills,
            'total': len(skills)
        }), 200
        
    except Exception as e:
        logger.error(f'Error retrieving skills: {str(e)}')
        return jsonify({'error': str(e)}), 500


@resume_parsing_bp.route('/<int:resume_id>/education', methods=['GET'])
def get_resume_education(resume_id):
    """Get educational history from resume.
    
    Args:
        resume_id: Parsed resume ID
        
    Returns:
        JSON list of education entries
    """
    try:
        resume = ParsedResume.query.get(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        education = [edu.to_dict() for edu in resume.education]
        return jsonify({
            'resume_id': resume_id,
            'education': education,
            'total': len(education)
        }), 200
        
    except Exception as e:
        logger.error(f'Error retrieving education: {str(e)}')
        return jsonify({'error': str(e)}), 500


@resume_parsing_bp.route('/<int:resume_id>/experience', methods=['GET'])
def get_resume_experience(resume_id):
    """Get work experience from resume.
    
    Args:
        resume_id: Parsed resume ID
        
    Returns:
        JSON list of experience entries
    """
    try:
        resume = ParsedResume.query.get(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        experience = [exp.to_dict() for exp in resume.experience]
        return jsonify({
            'resume_id': resume_id,
            'experience': experience,
            'total': len(experience)
        }), 200
        
    except Exception as e:
        logger.error(f'Error retrieving experience: {str(e)}')
        return jsonify({'error': str(e)}), 500


@resume_parsing_bp.route('/<int:resume_id>', methods=['DELETE'])
def delete_parsed_resume(resume_id):
    """Delete parsed resume and all related data.
    
    Args:
        resume_id: Parsed resume ID
        
    Returns:
        JSON confirmation
    """
    try:
        resume = ParsedResume.query.get(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        db.session.delete(resume)
        db.session.commit()
        
        logger.info(f'Resume {resume_id} deleted')
        
        return jsonify({'message': 'Resume deleted successfully'}), 200
        
    except Exception as e:
        logger.error(f'Error deleting resume: {str(e)}')
        return jsonify({'error': str(e)}), 500
