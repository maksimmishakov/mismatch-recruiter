# Export blueprints from routes modules
from app.routes.candidates import blueprint as candidates_bp
from app.routes.matches import matches_bp
from app.routes.job_enrichment import job_enrichment_bp
from app.routes.resume_parsing import resume_parsing_bp

__all__ = [
    'candidates_bp',
    'matches_bp',
    'job_enrichment_bp',
    'resume_parsing_bp',
]
