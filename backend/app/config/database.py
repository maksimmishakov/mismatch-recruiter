import os
from sqlalchemy import create_engine, event
from sqlalchemy.pool import QueuePool
from urllib.parse import quote_plus

class DatabaseConfig:
    @staticmethod
    def create_engine():
        """Create SQLAlchemy engine with optimized connection pooling"""
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'password')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'mismatch')
        
        # URL with proper escaping
        db_url = f'postgresql://{quote_plus(db_user)}:{quote_plus(db_password)}@{db_host}:{db_port}/{db_name}'
        
        engine = create_engine(
            db_url,
            poolclass=QueuePool,
            pool_size=20,  # Number of connections to keep in pool
            max_overflow=40,  # Max additional connections
            pool_timeout=30,  # Wait 30 seconds for connection
            pool_recycle=1800,  # Recycle connections after 30 min
            pool_pre_ping=True,  # Test connection before using
            echo=False,
            connect_args={
                'connect_timeout': 10,
                'keepalives': 1,
                'keepalives_idle': 30,
            },
            execution_options={
                'isolation_level': 'READ COMMITTED',  # Prevent expensive locking
            }
        )
        
        return engine
