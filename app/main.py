"""Main application initialization module.

Integrates all Flask application components including:
- Routes and blueprints
- Middleware (rate limiting, request validation)
- Database optimization and caching
- Logging and monitoring
- API documentation (Swagger/OpenAPI)
- Security features
"""

from flask import Flask
from app.routes import matching_v2, analytics
from app.middleware.rate_limiter import limiter
from app.middleware.request_validator import request_validator
from app.logger import setup_application_logger, get_logger
from app.cache import cache
from app.swagger import setup_swagger
from app.security import SecurityManager, security_headers
from app.database_optimization import DatabaseOptimizer

# Initialize logger
app_logger = get_logger(__name__)

def create_app(config_name='development'):
    """Application factory pattern.
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Setup logging
    setup_application_logger(app)
    app_logger.info(f"Initializing MisMatch Recruiter application in {config_name} mode")
    
    # Initialize extensions
    limiter.init_app(app)
    cache.init_app(app)
    request_validator.init_app(app)
    
    # Apply security headers
    app.after_request(security_headers)
    
    # Register blueprints
    app.include_router(matching_v2.router)
    app.include_router(analytics.router)
    
    # Setup Swagger documentation
    setup_swagger(app)
    
    # Initialize database optimization
    db_optimizer = DatabaseOptimizer(app)
    db_optimizer.create_indexes()
    
    app_logger.info("Application initialization completed successfully")
    return appfrom app.routes import analytics
app.include_router(matching_v2.router)
app.include_router(analytics.router)
