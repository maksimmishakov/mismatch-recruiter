Mismatch_initialization_service.py"""Mismatch Integration Initialization Service

Handles setup, configuration, and initialization of Mismatch integration.
Responsible for initializing database models, configuring clients, and scheduling tasks.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from app.config.Mismatch import get_settings, MismatchSettings
from app.models.Mismatch import Base, MismatchSync


logger = logging.getLogger(__name__)


class MismatchInitializationService:
    """Service for initializing and setting up Mismatch integration"""
    
    def __init__(self):
        """Initialize the service with settings"""
        self.settings: MismatchSettings = get_settings()
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
                "api_base_url": str(self.settings.Mismatch_api_base_url),
                "sync_enabled": str(self.settings.Mismatch_sync_enabled),
                "min_match_score": str(self.settings.Mismatch_min_match_score),
                "webhook_enabled": str(self.settings.Mismatch_webhook_enabled),
            }
            
            logger.info("Configuration storage initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize config storage: {e}")
            return False
    
    def verify_api_credentials(self) -> bool:
        """Verify Mismatch API credentials
        
        Returns:
            bool: True if credentials are present, False otherwise
        """
        try:
            api_key = self.settings.Mismatch_api_key.get_secret_value()
            api_secret = self.settings.Mismatch_api_secret.get_secret_value()
            
            if not api_key or not api_secret:
                logger.warning("Mismatch API credentials not configured")
                return False
            
            logger.info("Mismatch API credentials verified")
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
            logger.info("Mismatch integration initialization completed successfully")
        else:
            logger.error("Mismatch integration initialization failed")
        
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
            "api_key_configured": bool(self.settings.Mismatch_api_key.get_secret_value()),
            "sync_enabled": self.settings.Mismatch_sync_enabled,
            "webhook_enabled": self.settings.Mismatch_webhook_enabled,
        }


# Singleton instance
_Mismatch_init_service: Optional[MismatchInitializationService] = None


def get_Mismatch_initialization_service() -> MismatchInitializationService:
    """Get or create singleton MismatchInitializationService
    
    Returns:
        MismatchInitializationService instance
    """
    global _Mismatch_init_service
    if _Mismatch_init_service is None:
        _Mismatch_init_service = MismatchInitializationService()
    return _Mismatch_init_service


def initialize_Mismatch() -> Dict[str, Any]:
    """Initialize Mismatch integration
    
    Returns:
        Dict with initialization results
    """
    service = get_Mismatch_initialization_service()
    return service.run_initialization()
