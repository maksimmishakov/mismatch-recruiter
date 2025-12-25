"""Create resume parsing tables migration.

Revision ID: 001
Creates: ParsedResume, ResumeSkill, ResumeEducation, ResumeExperience tables
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
    # Create ParsedResume table
    op.create_table('parsed_resume',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('raw_text', sa.Text(), nullable=True),
        sa.Column('parsing_status', sa.String(20), nullable=True),
        sa.Column('parsing_metadata', postgresql.JSON(), nullable=True),
        sa.Column('error_message', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['job_id'], ['job.id'], )
    )
    op.create_index('ix_parsed_resume_job_id', 'parsed_resume', ['job_id'])
    op.create_index('ix_parsed_resume_status', 'parsed_resume', ['parsing_status'])

    # Create ResumeSkill table
    op.create_table('resume_skill',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('skill_name', sa.String(100), nullable=False),
        sa.Column('skill_category', sa.String(50), nullable=True),
        sa.Column('proficiency_level', sa.String(20), nullable=True),
        sa.Column('years_experience', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['resume_id'], ['parsed_resume.id'], )
    )
    op.create_index('ix_resume_skill_resume_id', 'resume_skill', ['resume_id'])
    op.create_index('ix_resume_skill_name', 'resume_skill', ['skill_name'])

    # Create ResumeEducation table
    op.create_table('resume_education',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('school_name', sa.String(200), nullable=True),
        sa.Column('degree', sa.String(100), nullable=True),
        sa.Column('field_of_study', sa.String(100), nullable=True),
        sa.Column('start_date', sa.String(20), nullable=True),
        sa.Column('end_date', sa.String(20), nullable=True),
        sa.Column('gpa', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['resume_id'], ['parsed_resume.id'], )
    )
    op.create_index('ix_resume_education_resume_id', 'resume_education', ['resume_id'])

    # Create ResumeExperience table
    op.create_table('resume_experience',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('company_name', sa.String(200), nullable=True),
        sa.Column('job_title', sa.String(100), nullable=True),
        sa.Column('start_date', sa.String(20), nullable=True),
        sa.Column('end_date', sa.String(20), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('duration_months', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['resume_id'], ['parsed_resume.id'], )
    )
    op.create_index('ix_resume_experience_resume_id', 'resume_experience', ['resume_id'])


def downgrade():
    op.drop_index('ix_resume_experience_resume_id')
    op.drop_table('resume_experience')
    op.drop_index('ix_resume_education_resume_id')
    op.drop_table('resume_education')
    op.drop_index('ix_resume_skill_name')
    op.drop_index('ix_resume_skill_resume_id')
    op.drop_table('resume_skill')
    op.drop_index('ix_parsed_resume_status')
    op.drop_index('ix_parsed_resume_job_id')
    op.drop_table('parsed_resume')
