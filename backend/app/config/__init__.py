# Get environment from FLASK_ENV variable
import os

FLASK_ENV = os.getenv('FLASK_ENV', 'development').lower()

# Export appropriate configuration based on environment
if FLASK_ENV == 'production':
    from .production import ProductionConfig as Config
elif FLASK_ENV == 'staging':
    from .staging import StagingConfig as Config
elif FLASK_ENV == 'testing':
    from .testing import TestingConfig as Config
else:
    from .development import DevelopmentConfig as Config

# Also export all config classes for direct access if needed
from .development import DevelopmentConfig
from .production import ProductionConfig
from .staging import StagingConfig
from .testing import TestingConfig

__all__ = [
    'Config',
    'DevelopmentConfig',
    'ProductionConfig',
    'StagingConfig',
    'TestingConfig',
]
