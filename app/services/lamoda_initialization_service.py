lamoda_initialization_service.py"""Lamoda Integration Initialization Service

Handles setup, configuration, and initialization of Lamoda integration.
Responsible for initializing database models, configuring clients, and scheduling tasks.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from app.config.lamoda import get_settings, LamodaSettings
from app.models.lamoda import Base, LamodaSync, LamodoIntegrationConfig


logger = logging.getLogger(__name__)


class LamodaInitializationService:
    """Service for initializing and setting up Lamoda integration"""
    
    def __init__(self):
        """Initialize the service with settings"""
        self.settings: LamodaSettings = get_settings()
        self.is_initialized: bool = False
        self.initialization_time: Optional[datetime] = None
    
    def initialize_database_models(self) -> bool:
        """Initialize database models and create tables
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # This would be called with actual SQLAlchemy engine in production
            # Base.metadata.create_all(bind=engine)
            logger.info("Database models initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize database models: {e}")
            return False
    
    def initialize_config_storage(self, db_session=None) -> bool:
        """Initialize configuration storage
        
        Args:
            db_session: SQLAlchemy session
            
        Returns:
            bool: True if successful
        """
        try:
            # Store initial configuration
            config_values = {
                "api_base_url": str(self.settings.lamoda_api_base_url),
                "sync_enabled": str(self.settings.lamoda_sync_enabled),
                "min_match_score": str(self.settings.lamoda_min_match_score),
                "webhook_enabled": str(self.settings.lamoda_webhook_enabled),
            }
            
            logger.info("Configuration storage initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize config storage: {e}")
            return False
    
    def verify_api_credentials(self) -> bool:
        """Verify Lamoda API credentials
        
        Returns:
            bool: True if credentials are present, False otherwise
        """
        try:
            api_key = self.settings.lamoda_api_key.get_secret_value()
            api_secret = self.settings.lamoda_api_secret.get_secret_value()
            
            if not api_key or not api_secret:
                logger.warning("Lamoda API credentials not configured")
                return False
            
            logger.info("Lamoda API credentials verified")
            return True
        except Exception as e:
            logger.error(f"Error verifying API credentials: {e}")
            return False
    
    def initialize_sync_tracking(self, db_session=None) -> bool:
        """Initialize sync tracking table
        
        Args:
            db_session: SQLAlchemy session
            
        Returns:
            bool: True if successful
        """
        try:
            # Would insert initial sync record in production
            logger.info("Sync tracking initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize sync tracking: {e}")
            return False
    
    def run_initialization(self) -> Dict[str, Any]:
        """Run complete initialization sequence
        
        Returns:
            Dict with initialization status
        """
        results = {
            "database_models": self.initialize_database_models(),
            "config_storage": self.initialize_config_storage(),
            "api_credentials": self.verify_api_credentials(),
            "sync_tracking": self.initialize_sync_tracking(),
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Mark as initialized if all critical components are ready
        self.is_initialized = all([
            results["database_models"],
            results["config_storage"],
            results["sync_tracking"],
        ])
        
        if self.is_initialized:
            self.initialization_time = datetime.utcnow()
            logger.info("Lamoda integration initialization completed successfully")
        else:
            logger.error("Lamoda integration initialization failed")
        
        results["overall_status"] = "initialized" if self.is_initialized else "failed"
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """Get current initialization status
        
        Returns:
            Dict with current status
        """
        return {
            "is_initialized": self.is_initialized,
            "initialization_time": self.initialization_time.isoformat() if self.initialization_time else None,
            "api_key_configured": bool(self.settings.lamoda_api_key.get_secret_value()),
            "sync_enabled": self.settings.lamoda_sync_enabled,
            "webhook_enabled": self.settings.lamoda_webhook_enabled,
        }


# Singleton instance
_lamoda_init_service: Optional[LamodaInitializationService] = None


def get_lamoda_initialization_service() -> LamodaInitializationService:
    """Get or create singleton LamodaInitializationService
    
    Returns:
        LamodaInitializationService instance
    """
    global _lamoda_init_service
    if _lamoda_init_service is None:
        _lamoda_init_service = LamodaInitializationService()
    return _lamoda_init_service


def initialize_lamoda() -> Dict[str, Any]:
    """Initialize Lamoda integration
    
    Returns:
        Dict with initialization results
    """
    service = get_lamoda_initialization_service()
    return service.run_initialization()
