from datetime import datetime
from app import db

class AuditLog(db.Model):
    """Audit log for tracking all data access and modifications (GDPR compliance)"""
    __tablename__ = 'audit_log'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)  # 'read', 'write', 'delete', 'anonymize', 'export'
    resource_type = db.Column(db.String(50), nullable=False)  # 'resume', 'user', 'job', 'candidate'
    resource_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(100), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    details = db.Column(db.JSON, nullable=True)  # Additional context (reason, changes, etc.)
    status = db.Column(db.String(20), default='success')  # success, failed, warning
    error_message = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<AuditLog {self.action} on {self.resource_type}#{self.resource_id} at {self.timestamp}>'
    
    @classmethod
    def create(cls, action, resource_type, resource_id, user_id=None, ip_address=None, details=None, status='success'):
        """Create and save an audit log entry"""
        log = cls(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            ip_address=ip_address,
            details=details,
            status=status
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    @classmethod
    def log_action(cls, action, resource_type, resource_id, user_id=None, ip_address=None, **kwargs):
        """Convenience method for logging actions"""
        return cls.create(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            ip_address=ip_address,
            details=kwargs
        )
