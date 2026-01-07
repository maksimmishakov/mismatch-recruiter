import os
from app import create_app, db
from app.models import User, Candidate, JobPosting, Match

app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
