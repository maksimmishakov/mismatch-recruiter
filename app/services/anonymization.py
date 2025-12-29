"""Data anonymization service for GDPR compliance"""
from datetime import datetime
from app import db
from app.models.audit_log import AuditLog

def anonymize_resume(resume_id, reason='gdpr_request'):
    """Anonymize resume data while preserving ML vectors"""
    from app.models import Resume  # Delayed import to avoid circular imports
    
    resume = Resume.query.get(resume_id)
    if not resume:
        raise ValueError(f'Resume {resume_id} not found')
    
    # Log the anonymization action
    AuditLog.create(
        action='anonymize',
        resource_type='resume',
        resource_id=resume_id,
        user_id=resume.user_id,
        details={'reason': reason, 'timestamp': datetime.utcnow().isoformat()}
    )
    
    # Store skill vectors for ML training before anonymization
    skill_vector = getattr(resume, 'skill_vector', None)
    
    # Anonymize PII (Personally Identifiable Information)
    resume.name = f'AnonymousResume_{resume_id}'
    resume.email = None
    resume.phone = None
    resume.location = None
    resume.location_code = None
    resume.linkedin_url = None
    resume.github_url = None
    resume.portfolio_url = None
    
    # Preserve non-PII data
    # resume.skill_vector = skill_vector  # Keep for ML
    resume.anonymized = True
    resume.anonymized_at = datetime.utcnow()
    
    db.session.commit()
    return resume

def anonymize_user(user_id, reason='gdpr_request'):
    """Anonymize user profile"""
    from app.models import User
    
    user = User.query.get(user_id)
    if not user:
        raise ValueError(f'User {user_id} not found')
    
    # Log the action
    AuditLog.create(
        action='anonymize',
        resource_type='user',
        resource_id=user_id,
        details={'reason': reason}
    )
    
    # Anonymize fields
    user.email = f'deleted_{user_id}@anonymous.local'
    user.name = f'AnonymousUser_{user_id}'
    user.phone = None
    user.location = None
    user.profile_picture = None
    
    db.session.commit()
    return user

def anonymize_candidate(candidate_id, reason='gdpr_request'):
    """Anonymize candidate data"""
    from app.models import Candidate
    
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        raise ValueError(f'Candidate {candidate_id} not found')
    
    AuditLog.create(
        action='anonymize',
        resource_type='candidate',
        resource_id=candidate_id,
        details={'reason': reason}
    )
    
    candidate.name = f'AnonymousCandidate_{candidate_id}'
    candidate.email = None
    candidate.phone = None
    candidate.location = None
    
    db.session.commit()
    return candidate
