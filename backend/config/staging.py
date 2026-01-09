# backend/config/staging.py
# Staging environment configuration

import os
from .base import BaseConfig

class StagingConfig(BaseConfig):
    """Staging configuration - production-like but not production."""
    
    # Environment
    ENVIRONMENT = 'staging'
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL_STAGING',
        'postgresql://staging:staging_password@staging-db.internal:5432/mismatch_staging'
    )
    SQLALCHEMY_ECHO = False
    
    # Redis
    REDIS_URL = os.getenv(
        'REDIS_URL_STAGING',
        'redis://staging-redis.internal:6379/0'
    )
    
    # Security
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY_STAGING')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS
    CORS_ORIGINS = [
        'https://staging.mismatch-recruiter.ru',
        'https://app-staging.mismatch-recruiter.ru'
    ]
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = 'json'
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.getenv(
        'REDIS_URL_STAGING',
        'redis://staging-redis.internal:6379/1'
    )
    
    # Celery
    CELERY_BROKER_URL = os.getenv(
        'REDIS_URL_STAGING',
        'redis://staging-redis.internal:6379/2'
    )
    CELERY_RESULT_BACKEND = os.getenv(
        'REDIS_URL_STAGING',
        'redis://staging-redis.internal:6379/3'
    )
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER_STAGING')
    MAIL_PORT = int(os.getenv('MAIL_PORT_STAGING', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME_STAGING')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD_STAGING')
    MAIL_DEFAULT_SENDER = os.getenv(
        'MAIL_DEFAULT_SENDER_STAGING',
        'noreply-staging@mismatch-recruiter.ru'
    )
    
    # API
    API_RATE_LIMIT = '100/hour'
    
    # Sentry error tracking
    SENTRY_DSN = os.getenv('SENTRY_DSN_STAGING')
    SENTRY_ENVIRONMENT = 'staging'
    SENTRY_TRACES_SAMPLE_RATE = 0.1
    
    # Features
    ENABLE_ANALYTICS = True
    ENABLE_MONITORING = True
    ENABLE_PROFILING = True
