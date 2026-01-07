import logging
import logging.handlers
import os
import json
from datetime import datetime

def setup_logging(app):
    """Setup logging with ELK stack support""    
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    
    # JSON formatter for ELK
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_obj = {
                'timestamp': datetime.utcnow().isoformat(),
                'level': record.levelname,
                'logger': record.name,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno,
            }
            if record.exc_info:
                log_obj['exception'] = self.formatException(record.exc_info)
            return json.dumps(log_obj)
    
    # File handler
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    file_handler = logging.handlers.RotatingFileHandler(
        f"logs/mismatch_{datetime.now().strftime('%Y%m%d')}.log",
        maxBytes=10485760,
        backupCount=10
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(JSONFormatter())
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(JSONFormatter())
    
    # UDP handler for ELK (if enabled)
    if app.config.get('ENABLE_ELK_LOGGING', False):
        elk_handler = logging.handlers.SysLogHandler(
            address=('localhost', 5000),
            facility=logging.handlers.SysLogHandler.LOG_LOCAL0
        )
        elk_handler.setLevel(log_level)
        elk_handler.setFormatter(JSONFormatter())
        app.logger.addHandler(elk_handler)
    
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    
    return app.logger
