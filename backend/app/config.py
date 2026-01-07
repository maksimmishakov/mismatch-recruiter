import os

class DevelopmentConfig:
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://mismatch:dev-password@localhost:5432/mismatch_dev')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change')
    JSON_SORT_KEYS = False
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5173']
    LOG_LEVEL = 'DEBUG'
    SENTRY_DSN = os.getenv('SENTRY_DSN', '')

class TestingConfig(DevelopmentConfig):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

class ProductionConfig:
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URL = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')
    LOG_LEVEL = 'INFO'
    SENTRY_DSN = os.getenv('SENTRY_DSN', '')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
