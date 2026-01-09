"""Configuration module for MisMatch Recruiter application."""

import os
from .development import Config as DevelopmentConfig
from .production import Config as ProductionConfig
from .staging import Config as StagingConfig
from .testing import Config as TestingConfig

# Get environment from FLASK_ENV variable
ENV = os.getenv('FLASK_ENV', 'development').lower()

# Export appropriate configuration based on environment
if ENV == 'production':
    Config = ProductionConfig
elif ENV == 'staging':
    Config = StagingConfig
elif ENV == 'testing':
    Config = TestingConfig
else:
    Config = DevelopmentConfig

# Export all config classes for direct access if needed
__all__ = [
    'Config',
    'DevelopmentConfig',
    'ProductionConfig',
    'StagingConfig',
    'TestingConfig',
]
