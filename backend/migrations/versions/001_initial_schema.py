"""Initial schema creation.

Revision ID: 001
Revises: 
Create Date: 2026-01-07
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create candidates table
    op.create_table(
        'candidates',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('skills', sa.JSON, nullable=True),
        sa.Column('experience_years', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now()),
    )
    
    # Create jobs table
    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('required_skills', sa.JSON, nullable=True),
        sa.Column('salary_min', sa.Numeric(10, 2), nullable=True),
        sa.Column('salary_max', sa.Numeric(10, 2), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now()),
    )
    
    # Create matches table
    op.create_table(
        'matches',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('candidate_id', sa.Integer, sa.ForeignKey('candidates.id'), nullable=False),
        sa.Column('job_id', sa.Integer, sa.ForeignKey('jobs.id'), nullable=False),
        sa.Column('match_score', sa.Numeric(5, 2), nullable=False),
        sa.Column('status', sa.String(50), default='pending', nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now()),
    )
    
    # Create indices
    op.create_index('ix_candidates_email', 'candidates', ['email'])
    op.create_index('ix_matches_candidate_id', 'matches', ['candidate_id'])
    op.create_index('ix_matches_job_id', 'matches', ['job_id'])

def downgrade():
    op.drop_index('ix_matches_job_id')
    op.drop_index('ix_matches_candidate_id')
    op.drop_index('ix_candidates_email')
    op.drop_table('matches')
    op.drop_table('jobs')
    op.drop_table('candidates')
