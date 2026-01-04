# Enable CORS for the Flask app
from flask import Flask
from flask_cors import CORS

with open('/workspaces/mismatch-recruiter/app/__init__.py', 'r') as f:
    content = f.read()

# Check if CORS is already enabled
if 'CORS(app)' not in content:
    # Add CORS import
    if 'from flask_cors import CORS' not in content:
        content = content.replace(
            'from flask import Flask',
            'from flask import Flask\nfrom flask_cors import CORS'
        )
    
    # Add CORS initialization
    content = content.replace(
        'def create_app():',
        'def create_app():\n    CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])'
    )
    
    with open('/workspaces/mismatch-recruiter/app/__init__.py', 'w') as f:
        f.write(content)
    
    print('✅ CORS enabled')
else:
    print('✅ CORS already enabled')
