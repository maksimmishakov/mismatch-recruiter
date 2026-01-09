# Lazy loading of configuration based on FLASK_ENV
import os

FLASK_ENV = os.getenv('FLASK_ENV', 'development').lower()

def get_config():
    """Get the appropriate configuration based on FLASK_ENV."""
    if FLASK_ENV == 'production':
        from .production import ProductionConfig
        return ProductionConfig()
    elif FLASK_ENV == 'staging':
        from .staging import StagingConfig
        return StagingConfig()
    elif FLASK_ENV == 'testing':
        from .testing import TestingConfig
        return TestingConfig()
    else:
        from .development import DevelopmentConfig
        return DevelopmentConfig()

# For backward compatibility with 'from app.config import Config' style imports
# We'll import based on the FLASK_ENV at initialization time
try:
    if FLASK_ENV == 'production':
        from .production import ProductionConfig as Config
    elif FLASK_ENV == 'staging':
        from .staging import StagingConfig as Config
    elif FLASK_ENV == 'testing':
        from .testing import TestingConfig as Config
    else:
        from .development import DevelopmentConfig as Config
except ValueError:
    # If environment variables are not set, default to DevelopmentConfig
    from .development import DevelopmentConfig as Config

# Also export all config classes for direct access if needed
try:
    from .development import DevelopmentConfig
except ImportError:
    DevelopmentConfig = None

try:
    from .production import ProductionConfig
except (ImportError, ValueError):
    ProductionConfig = None

try:
    from .staging import StagingConfig
except (ImportError, ValueError):
    StagingConfig = None

try:
    from .testing import TestingConfig
except (ImportError, ValueError):
    TestingConfig = None

__all__ = [
    'Config',
    'get_config',
    'DevelopmentConfig',
    'ProductionConfig',
    'StagingConfig',
    'TestingConfig',
]
