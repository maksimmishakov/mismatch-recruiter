"""API routes aggregation."""
from flask import Blueprint
from app.routes.auth import auth_bp
from app.routes.candidates import candidates_bp
from app.routes.jobs import jobs_bp
from app.routes.matching import matching_bp

# Create the main API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Register sub-blueprints
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(candidates_bp, url_prefix='/candidates')
api_bp.register_blueprint(jobs_bp, url_prefix='/jobs')
api_bp.register_blueprint(matching_bp, url_prefix='/matching')

__all__ = ['api_bp']
