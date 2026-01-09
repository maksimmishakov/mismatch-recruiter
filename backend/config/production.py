# backend/config/production.py
# Production environment configuration - strict and secure

import os
from .base import BaseConfig

class ProductionConfig(BaseConfig):
    """Production configuration - strict and secure."""
    
    # Environment
    ENVIRONMENT = 'production'
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError('DATABASE_URL environment variable not set')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'poolsize': 70,
        'poolrecycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20,
    }
    
    # Redis
    REDIS_URL = os.getenv('REDIS_URL')
    if not REDIS_URL:
        raise ValueError('REDIS_URL environment variable not set')
    
    # Security
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError('JWT_SECRET_KEY environment variable not set')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # CORS
    CORS_ORIGINS = [
        'https://app.mismatch-recruiter.ru',
        'https://mismatch-recruiter.ru',
    ]
    
    # Logging
    LOG_LEVEL = 'WARNING'
    LOG_FORMAT = 'json'
    LOG_FILE = '/var/log/mismatch/app.log'
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL')
    
    # Celery
    CELERY_BROKER_URL = os.getenv('REDIS_URL')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL')
    CELERY_TASK_TIME_LIMIT = (30 * 60)  # 30 minutes
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv(
        'MAIL_DEFAULT_SENDER',
        'noreply@mismatch-recruiter.ru'
    )
    
    # API
    API_RATE_LIMIT = '50/hour'
    
    # Sentry
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    SENTRY_ENVIRONMENT = 'production'
    SENTRY_TRACES_SAMPLE_RATE = 0.1  # 10% sampling
    
    # Features
    ENABLE_ANALYTICS = True
    ENABLE_MONITORING = True
    ENABLE_PROFILING = False
    
    # Security Headers
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_SECURITY_POLICY = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' cdn.jsdelivr.net",
        'style-src': "'self' 'unsafe-inline' fonts.googleapis.com",
        'font-src': "'self' fonts.gstatic.com",
        'img-src': "'self' data: https:",
        'connect-src': "'self' api.mismatch-recruiter.ru",
    }
