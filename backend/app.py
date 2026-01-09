#!/usr/bin/env python3
"""Main entry point for the Flask application."""

from app import create_app
import os

if __name__ == '__main__':
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name=config_name)
    
    # Get port from environment or use default
    port = int(os.getenv('PORT', 5000))
    debug = config_name == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
