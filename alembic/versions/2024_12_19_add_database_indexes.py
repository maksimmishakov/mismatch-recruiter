"""Add database indexes for performance optimization.

Revision ID: 001_add_database_indexes
Revises: None
Create Date: 2024-12-19
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_add_database_indexes'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply database indexes."""
    # Users table indexes
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index('idx_users_created_at', 'users', ['created_at'])
    op.create_index('idx_users_is_active', 'users', ['is_active'])
    
    # Resumes table indexes
    op.create_index('idx_resumes_user_id', 'resumes', ['user_id'])
    op.create_index('idx_resumes_created_at', 'resumes', ['created_at'])
    op.create_index('idx_resumes_skills', 'resumes', ['skills'])
    op.create_index('idx_resumes_experience', 'resumes', ['experience'])
    
    # Jobs table indexes
    op.create_index('idx_jobs_company_id', 'jobs', ['company_id'])
    op.create_index('idx_jobs_created_at', 'jobs', ['created_at'])
    op.create_index('idx_jobs_status', 'jobs', ['status'])
    op.create_index('idx_jobs_salary_range', 'jobs', ['min_salary', 'max_salary'])
    
    # Matches table indexes
    op.create_index('idx_matches_resume_id', 'matches', ['resume_id'])
    op.create_index('idx_matches_job_id', 'matches', ['job_id'])
    op.create_index('idx_matches_score', 'matches', ['match_score'])
    op.create_index('idx_matches_created_at', 'matches', ['created_at'])
    op.create_index('idx_matches_resume_job', 'matches', ['resume_id', 'job_id'], unique=True)
    op.create_index('idx_matches_composite', 'matches', ['job_id', 'match_score', 'created_at'])


def downgrade() -> None:
    """Remove database indexes."""
    # Remove composite and unique indexes first
    op.drop_index('idx_matches_composite')
    op.drop_index('idx_matches_resume_job')
    
    # Matches table indexes
    op.drop_index('idx_matches_created_at')
    op.drop_index('idx_matches_score')
    op.drop_index('idx_matches_job_id')
    op.drop_index('idx_matches_resume_id')
    
    # Jobs table indexes
    op.drop_index('idx_jobs_salary_range')
    op.drop_index('idx_jobs_status')
    op.drop_index('idx_jobs_created_at')
    op.drop_index('idx_jobs_company_id')
    
    # Resumes table indexes
    op.drop_index('idx_resumes_experience')
    op.drop_index('idx_resumes_skills')
    op.drop_index('idx_resumes_created_at')
    op.drop_index('idx_resumes_user_id')
    
    # Users table indexes
    op.drop_index('idx_users_is_active')
    op.drop_index('idx_users_created_at')
    op.drop_index('idx_users_email')
