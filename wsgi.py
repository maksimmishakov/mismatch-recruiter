import os
import sys
from backend.app import create_app

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run()
