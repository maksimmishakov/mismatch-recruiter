#!/usr/bin/env python
"""Database initialization and migration script"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app, db
from app.models import (
    User, JobProfile, Candidate, Feedback, FeatureRequest,
    Resume, Match, SkillProfile, HiringDNA, HiringSignal
)

def init_db():
    """Initialize the database with all tables"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Initializing database...")
        
        try:
            # Create all tables
            db.create_all()
            print("✓ Database tables created successfully!")
            
            # Log created models
            print("\n📋 Created tables:")
            tables = [
                'users', 'job_profiles', 'candidates', 'feedback',
                'feature_requests', 'resume', 'match', 'skill_profile',
                'hiring_dna', 'hiring_signals'
            ]
            for table in tables:
                print(f"  • {table}")
            
            # Display connection info
            print(f"\n📊 Database Information:")
            print(f"  Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
            print(f"  Echo mode: {app.config.get('SQLALCHEMY_ECHO', False)}")
            
            print("\n✅ Database initialization complete!")
            print("\n🚀 Next steps:")
            print("  1. Run migrations if needed: flask db upgrade")
            print("  2. Create sample data: python create_sample_data.py")
            print("  3. Start the server: python run.py")
            
        except Exception as e:
            print(f"❌ Error during database initialization:")
            print(f"  {type(e).__name__}: {str(e)}")
            sys.exit(1)

def drop_db():
    """Drop all database tables (WARNING: destructive)"""
    app = create_app()
    
    with app.app_context():
        print("⚠️  WARNING: This will delete ALL data from the database!")
        response = input("Type 'yes' to confirm: ")
        
        if response.lower() == 'yes':
            print("🔄 Dropping all tables...")
            db.drop_all()
            print("✓ All tables dropped!")
        else:
            print("Cancelled.")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Database management')
    parser.add_argument(
        'command',
        choices=['init', 'drop'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    if args.command == 'init':
        init_db()
    elif args.command == 'drop':
        drop_db()