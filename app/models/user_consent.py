from datetime import datetime
from app import db

class UserConsent(db.Model):
    """GDPR user consent model for tracking user permissions"""
    __tablename__ = 'user_consent'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    
    # GDPR consent fields
    consent_processing = db.Column(db.Boolean, default=False)  # Data processing
    consent_ml = db.Column(db.Boolean, default=False)  # ML training
    consent_analytics = db.Column(db.Boolean, default=False)  # Analytics
    consent_third_party = db.Column(db.Boolean, default=False)  # Third-party sharing
    consent_marketing = db.Column(db.Boolean, default=False)  # Marketing
    
    # Versions and dates
    privacy_policy_version = db.Column(db.String(20), default='1.0')
    terms_version = db.Column(db.String(20), default='1.0')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    accepted_ip = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f'<UserConsent user_id={self.user_id}>'
    
    @classmethod
    def get_or_create(cls, user_id):
        """Get or create consent record for user"""
        consent = cls.query.filter_by(user_id=user_id).first()
        if not consent:
            consent = cls(user_id=user_id)
            db.session.add(consent)
            db.session.commit()
        return consent
    
    def update_from_dict(self, data):
        """Update consent from dictionary"""
        for key in ['consent_processing', 'consent_ml', 'consent_analytics', 'consent_third_party', 'consent_marketing']:
            if key in data:
                setattr(self, key, data[key])
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
