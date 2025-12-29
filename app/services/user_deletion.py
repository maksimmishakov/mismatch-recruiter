"""User data deletion service - GDPR Right to be Forgotten (Article 17)"""
from datetime import datetime
from app import db
from app.models.audit_log import AuditLog
from app.services.anonymization import anonymize_user, anonymize_resume

def delete_user_data(user_id, reason='user_request'):
    """
    Complete deletion of user data and related resources.
    GDPR Compliant: Right to be Forgotten
    """
    from app.models import User, Resume, JobApplication, Candidate
    
    user = User.query.get(user_id)
    if not user:
        return {'status': 'error', 'message': f'User {user_id} not found'}
    
    try:
        # 1. Log the deletion request
        deletion_log = AuditLog.create(
            action='full_deletion_request',
            resource_type='user',
            resource_id=user_id,
            details={
                'reason': reason,
                'timestamp': datetime.utcnow().isoformat(),
                'email': user.email  # Store before deletion
            }
        )
        
        # 2. Delete associated resumes
        resumes = Resume.query.filter_by(user_id=user_id).all()
        for resume in resumes:
            db.session.delete(resume)
            AuditLog.create(
                action='delete',
                resource_type='resume',
                resource_id=resume.id,
                user_id=user_id,
                details={'reason': 'parent_user_deletion'}
            )
        
        # 3. Delete job applications
        applications = JobApplication.query.filter_by(user_id=user_id).all()
        for app in applications:
            db.session.delete(app)
            AuditLog.create(
                action='delete',
                resource_type='job_application',
                resource_id=app.id,
                user_id=user_id
            )
        
        # 4. Delete candidates associated with user
        candidates = Candidate.query.filter_by(user_id=user_id).all()
        for candidate in candidates:
            db.session.delete(candidate)
            AuditLog.create(
                action='delete',
                resource_type='candidate',
                resource_id=candidate.id,
                user_id=user_id
            )
        
        # 5. Anonymize user profile (keep account but remove PII)
        anonymize_user(user_id, reason='gdpr_deletion')
        
        # 6. Mark user as deleted
        user.is_active = False
        user.deleted_at = datetime.utcnow()
        user.deleted_reason = reason
        
        db.session.commit()
        
        # 7. Final audit log
        AuditLog.create(
            action='full_deletion_completed',
            resource_type='user',
            resource_id=user_id,
            details={'completed_at': datetime.utcnow().isoformat()}
        )
        
        return {
            'status': 'success',
            'message': f'User {user_id} data deleted successfully',
            'user_id': user_id,
            'deleted_at': datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        db.session.rollback()
        AuditLog.create(
            action='full_deletion_failed',
            resource_type='user',
            resource_id=user_id,
            status='failed',
            details={'error': str(e)}
        )
        return {'status': 'error', 'message': str(e)}

def request_data_export(user_id):
    """
    Generate a data export for user (GDPR Article 15 - Right to Access)
    """
    from app.models import User, Resume, JobApplication
    
    user = User.query.get(user_id)
    if not user:
        return None
    
    # Log the export request
    AuditLog.create(
        action='data_export_requested',
        resource_type='user',
        resource_id=user_id,
        details={'timestamp': datetime.utcnow().isoformat()}
    )
    
    export_data = {
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') else None
        },
        'resumes': [],
        'applications': []
    }
    
    # Collect resumes
    resumes = Resume.query.filter_by(user_id=user_id).all()
    for resume in resumes:
        export_data['resumes'].append({
            'id': resume.id,
            'title': getattr(resume, 'title', None),
            'created_at': getattr(resume, 'created_at', None)
        })
    
    # Collect job applications
    applications = JobApplication.query.filter_by(user_id=user_id).all()
    for app in applications:
        export_data['applications'].append({
            'id': app.id,
            'status': getattr(app, 'status', None),
            'created_at': getattr(app, 'created_at', None)
        })
    
    return export_data
