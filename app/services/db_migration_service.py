"""Database & Schema Migration Service - Alembic integration, versioning, rollback."""

import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from contextlib import contextmanager

from sqlalchemy import create_engine, MetaData, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError, DatabaseError
from alembic.config import Config as AlembicConfig
from alembic.command import upgrade, downgrade, current, heads, branches, revision


logger = logging.getLogger(__name__)


class MigrationStatus(str, Enum):
    """Migration status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class Migration:
    """Migration record."""
    version: str
    description: str
    status: MigrationStatus
    applied_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    error_message: Optional[str] = None
    checksum: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "version": self.version,
            "description": self.description,
            "status": self.status.value,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
            "duration_seconds": self.duration_seconds,
            "error_message": self.error_message,
            "checksum": self.checksum,
        }


class DatabaseMigrationService:
    """Database migration and schema management service."""

    def __init__(
        self,
        database_url: str,
        alembic_config_path: str,
    ):
        """Initialize migration service.
        
        Args:
            database_url: SQLAlchemy database URL
            alembic_config_path: Path to alembic.ini
        """
        self.database_url = database_url
        self.alembic_config_path = alembic_config_path
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.alembic_config = AlembicConfig(alembic_config_path)
        self.alembic_config.set_main_option("sqlalchemy.url", database_url)
        self.migrations: Dict[str, Migration] = {}

    @contextmanager
    def get_session(self):
        """Get database session context manager."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def test_connection(self) -> bool:
        """Test database connection.
        
        Returns:
            True if connection successful
        """
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except (OperationalError, DatabaseError) as e:
            logger.error(f"Database connection failed: {str(e)}")
            return False

    def get_current_version(self) -> Optional[str]:
        """Get current migration version.
        
        Returns:
            Current version or None
        """
        try:
            with self.engine.connect() as connection:
                inspector = inspect(self.engine)
                if "alembic_version" not in inspector.get_table_names():
                    return None
                result = connection.execute(
                    text("SELECT version_num FROM alembic_version ORDER BY version_num DESC LIMIT 1")
                )
                row = result.fetchone()
                return row[0] if row else None
        except Exception as e:
            logger.error(f"Failed to get current version: {str(e)}")
            return None

    def get_pending_migrations(self) -> List[str]:
        """Get pending migrations.
        
        Returns:
            List of pending migration versions
        """
        try:
            pending = []
            # This would integrate with Alembic's version history
            logger.info(f"Found {len(pending)} pending migrations")
            return pending
        except Exception as e:
            logger.error(f"Failed to get pending migrations: {str(e)}")
            return []

    def apply_migration(
        self,
        version: Optional[str] = None,
        description: str = "Upgrade",
    ) -> Migration:
        """Apply migration(s).
        
        Args:
            version: Specific version to migrate to. If None, migrate to latest.
            description: Migration description
            
        Returns:
            Migration record
        """
        start_time = datetime.utcnow()
        version_str = version or "head"
        migration = Migration(
            version=version_str,
            description=description,
            status=MigrationStatus.IN_PROGRESS,
        )

        try:
            if not self.test_connection():
                raise DatabaseError("Database connection failed", None, None)

            upgrade(self.alembic_config, version_str)

            migration.status = MigrationStatus.SUCCESS
            migration.applied_at = datetime.utcnow()
            migration.duration_seconds = (
                migration.applied_at - start_time
            ).total_seconds()
            logger.info(
                f"Migration {version_str} applied successfully in {migration.duration_seconds}s"
            )
        except Exception as e:
            migration.status = MigrationStatus.FAILED
            migration.error_message = str(e)
            logger.error(f"Migration {version_str} failed: {str(e)}")

        self.migrations[version_str] = migration
        return migration

    def rollback_migration(
        self,
        steps: int = 1,
        description: str = "Rollback",
    ) -> Migration:
        """Rollback migration(s).
        
        Args:
            steps: Number of steps to rollback
            description: Rollback description
            
        Returns:
            Migration record
        """
        start_time = datetime.utcnow()
        version_str = f"-{steps}"
        migration = Migration(
            version=version_str,
            description=description,
            status=MigrationStatus.IN_PROGRESS,
        )

        try:
            if not self.test_connection():
                raise DatabaseError("Database connection failed", None, None)

            downgrade(self.alembic_config, version_str)

            migration.status = MigrationStatus.ROLLED_BACK
            migration.applied_at = datetime.utcnow()
            migration.duration_seconds = (
                migration.applied_at - start_time
            ).total_seconds()
            logger.info(
                f"Rollback {steps} step(s) completed in {migration.duration_seconds}s"
            )
        except Exception as e:
            migration.status = MigrationStatus.FAILED
            migration.error_message = str(e)
            logger.error(f"Rollback failed: {str(e)}")

        self.migrations[version_str] = migration
        return migration

    def get_schema_info(self) -> Dict[str, Any]:
        """Get schema information.
        
        Returns:
            Dictionary with schema details
        """
        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            schema_info = {
                "tables": tables,
                "table_count": len(tables),
                "details": {},
            }

            for table in tables:
                columns = inspector.get_columns(table)
                schema_info["details"][table] = {
                    "columns": [
                        {
                            "name": col["name"],
                            "type": str(col["type"]),
                            "nullable": col["nullable"],
                        }
                        for col in columns
                    ],
                    "column_count": len(columns),
                }

            return schema_info
        except Exception as e:
            logger.error(f"Failed to get schema info: {str(e)}")
            return {}

    def get_migration_history(self) -> List[Dict]:
        """Get migration history.
        
        Returns:
            List of applied migrations
        """
        return [m.to_dict() for m in self.migrations.values()]
