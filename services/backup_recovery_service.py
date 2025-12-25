import logging
import json
import shutil
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class Backup:
    backup_id: str
    name: str
    size_mb: float
    created_at: datetime
    location: str
    status: str
    checksum: Optional[str] = None

class BackupRecoveryService:
    def __init__(self, backup_path: str = '/backups'):
        self.backup_path = Path(backup_path)
        self.backup_path.mkdir(parents=True, exist_ok=True)
        self.backups = {}
        self.recovery_history = []
    
    def create_backup(self, source_path: str, backup_name: str) -> Optional[str]:
        """Create a backup of specified path"""
        try:
            source = Path(source_path)
            if not source.exists():
                logger.error(f'Source path not found: {source_path}')
                return None
            
            backup_id = f'bkp_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
            backup_dir = self.backup_path / backup_id
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy source to backup
            if source.is_dir():
                shutil.copytree(source, backup_dir / source.name)
            else:
                shutil.copy2(source, backup_dir)
            
            # Calculate size
            size_mb = sum(f.stat().st_size for f in backup_dir.rglob('*')) / (1024 * 1024)
            
            backup = Backup(
                backup_id=backup_id,
                name=backup_name,
                size_mb=round(size_mb, 2),
                created_at=datetime.now(),
                location=str(backup_dir),
                status='completed'
            )
            
            self.backups[backup_id] = backup
            logger.info(f'Backup created: {backup_id}, size: {size_mb:.2f} MB')
            return backup_id
        except Exception as e:
            logger.error(f'Backup creation error: {str(e)}')
            return None
    
    def restore_backup(self, backup_id: str, restore_path: str) -> bool:
        """Restore from a backup"""
        try:
            if backup_id not in self.backups:
                logger.error(f'Backup not found: {backup_id}')
                return False
            
            backup = self.backups[backup_id]
            source = Path(backup.location)
            destination = Path(restore_path)
            
            # Clear destination if exists
            if destination.exists():
                if destination.is_dir():
                    shutil.rmtree(destination)
                else:
                    destination.unlink()
            
            # Restore backup
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
            
            # Record recovery
            self.recovery_history.append({
                'backup_id': backup_id,
                'restore_path': restore_path,
                'timestamp': datetime.now().isoformat(),
                'status': 'success'
            })
            
            logger.info(f'Backup restored: {backup_id} to {restore_path}')
            return True
        except Exception as e:
            logger.error(f'Restore error: {str(e)}')
            return False
    
    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        return [
            {
                'backup_id': b.backup_id,
                'name': b.name,
                'size_mb': b.size_mb,
                'created_at': b.created_at.isoformat(),
                'status': b.status
            }
            for b in self.backups.values()
        ]
    
    def delete_backup(self, backup_id: str) -> bool:
        """Delete a backup"""
        try:
            if backup_id not in self.backups:
                return False
            
            backup = self.backups[backup_id]
            backup_dir = Path(backup.location)
            
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            
            del self.backups[backup_id]
            logger.info(f'Backup deleted: {backup_id}')
            return True
        except Exception as e:
            logger.error(f'Delete backup error: {str(e)}')
            return False
    
    def verify_backup(self, backup_id: str) -> bool:
        """Verify backup integrity"""
        try:
            if backup_id not in self.backups:
                return False
            
            backup = self.backups[backup_id]
            backup_dir = Path(backup.location)
            
            if not backup_dir.exists():
                logger.error(f'Backup location not found: {backup.location}')
                return False
            
            logger.info(f'Backup verified: {backup_id}')
            return True
        except Exception as e:
            logger.error(f'Verification error: {str(e)}')
            return False
    
    def get_recovery_stats(self) -> Dict:
        """Get recovery statistics"""
        total_size = sum(b.size_mb for b in self.backups.values())
        recent_backups = sorted(self.backups.values(), key=lambda x: x.created_at, reverse=True)[:5]
        
        return {
            'total_backups': len(self.backups),
            'total_size_mb': round(total_size, 2),
            'recovery_operations': len(self.recovery_history),
            'recent_backups': [b.backup_id for b in recent_backups],
            'last_recovery': self.recovery_history[-1] if self.recovery_history else None
        }
