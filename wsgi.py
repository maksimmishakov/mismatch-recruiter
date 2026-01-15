"""
WSGI entry point for Gunicorn deployment
Used by: gunicorn wsgi:app
Recommended deployment: gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 4 --timeout 60
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
