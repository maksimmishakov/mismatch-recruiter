"""Initial migration: Create core tables.

Revision ID: 001
Revises: None
Create Date: 2026-01-04 15:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create initial tables."""
    # Create User table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(80), nullable=False, unique=True),
        sa.Column('email', sa.String(120), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), nullable=False, server_default='user'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_email', 'user', ['email'])
    
    # Create Candidate table
    op.create_table(
        'candidate',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(120), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('resume_url', sa.String(500), nullable=True),
        sa.Column('skills', postgresql.JSON(), nullable=True),
        sa.Column('experience_years', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_candidate_email', 'candidate', ['email'])
    
    # Create Job table
    op.create_table(
        'job',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('required_skills', postgresql.JSON(), nullable=True),
        sa.Column('salary_min', sa.Integer(), nullable=True),
        sa.Column('salary_max', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='open'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_job_status', 'job', ['status'])
    
    # Create Match table
    op.create_table(
        'match',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('candidate_id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Float(), nullable=False, server_default=sa.literal(0.0)),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidate.id']),
        sa.ForeignKeyConstraint(['job_id'], ['job.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('candidate_id', 'job_id')
    )
    op.create_index('ix_match_candidate_id', 'match', ['candidate_id'])
    op.create_index('ix_match_job_id', 'match', ['job_id'])
    op.create_index('ix_match_status', 'match', ['status'])


def downgrade():
    """Drop initial tables."""
    op.drop_index('ix_match_status')
    op.drop_index('ix_match_job_id')
    op.drop_index('ix_match_candidate_id')
    op.drop_table('match')
    op.drop_index('ix_job_status')
    op.drop_table('job')
    op.drop_index('ix_candidate_email')
    op.drop_table('candidate')
    op.drop_index('ix_user_email')
    op.drop_table('user')
