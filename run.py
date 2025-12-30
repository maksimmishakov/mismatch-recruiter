import os
import logging
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Get configuration from environment
    config_name = os.getenv('FLASK_ENV', 'development')
    
    # Create app using factory pattern
    app = create_app(config_name)
    
    # Get host and port from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask app on {host}:{port} (debug={debug})")
    
    # Run the app
    app.run(
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug
    )