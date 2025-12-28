"""Encryption & Data Protection Service - Symmetric encryption, data masking, secure storage."""

import os
import base64
import hashlib
from typing import Dict, Optional, Any, List, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend


class EncryptionLevel(str, Enum):
    """Encryption security levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class EncryptedData:
    """Encrypted data container."""
    ciphertext: str
    iv: str
    salt: str
    algorithm: str
    timestamp: datetime

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "ciphertext": self.ciphertext,
            "iv": self.iv,
            "salt": self.salt,
            "algorithm": self.algorithm,
            "timestamp": self.timestamp.isoformat(),
        }


class DataMasker:
    """Data masking for PII protection."""

    @staticmethod
    def mask_email(email: str) -> str:
        """Mask email address."""
        if "@" not in email:
            return email
        parts = email.split("@")
        masked_local = parts[0][:2] + "***" + parts[0][-1:]
        return f"{masked_local}@{parts[1]}"

    @staticmethod
    def mask_phone(phone: str) -> str:
        """Mask phone number."""
        cleaned = "".join(c for c in phone if c.isdigit())
        if len(cleaned) < 4:
            return "***"
        return "***" + cleaned[-4:]

    @staticmethod
    def mask_ssn(ssn: str) -> str:
        """Mask SSN."""
        cleaned = "".join(c for c in ssn if c.isdigit())
        if len(cleaned) < 4:
            return "***"
        return "***-**-" + cleaned[-4:]

    @staticmethod
    def mask_credit_card(card: str) -> str:
        """Mask credit card number."""
        cleaned = "".join(c for c in card if c.isdigit())
        if len(cleaned) < 4:
            return "***"
        return "****-****-****-" + cleaned[-4:]


class EncryptionService:
    """Main encryption and data protection service."""

    def __init__(self, master_key: Optional[str] = None):
        """Initialize encryption service.
        
        Args:
            master_key: Base64-encoded master key. If None, generated from env.
        """
        if master_key:
            self.master_key = master_key.encode()
        else:
            env_key = os.getenv("ENCRYPTION_KEY")
            if not env_key:
                # Generate a new key
                self.master_key = Fernet.generate_key()
            else:
                self.master_key = env_key.encode()

        self.cipher_suite = Fernet(self.master_key)
        self.data_masker = DataMasker()

    def encrypt(
        self,
        plaintext: str,
        level: EncryptionLevel = EncryptionLevel.HIGH,
    ) -> str:
        """Encrypt data.
        
        Args:
            plaintext: Data to encrypt
            level: Encryption security level
            
        Returns:
            Base64-encoded ciphertext
        """
        encrypted = self.cipher_suite.encrypt(plaintext.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt(
        self,
        ciphertext: str,
    ) -> str:
        """Decrypt data.
        
        Args:
            ciphertext: Base64-encoded ciphertext
            
        Returns:
            Decrypted plaintext
        """
        try:
            encrypted = base64.b64decode(ciphertext)
            plaintext = self.cipher_suite.decrypt(encrypted)
            return plaintext.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def hash_password(
        self,
        password: str,
        salt: Optional[bytes] = None,
    ) -> Tuple[str, str]:
        """Hash password with PBKDF2.
        
        Args:
            password: Password to hash
            salt: Optional salt. If None, generated.
            
        Returns:
            Tuple of (hashed_password, salt_b64)
        """
        if salt is None:
            salt = os.urandom(32)
        else:
            salt = base64.b64decode(salt)

        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        key = kdf.derive(password.encode())
        hashed = base64.b64encode(key).decode()
        salt_b64 = base64.b64encode(salt).decode()

        return hashed, salt_b64

    def verify_password(
        self,
        password: str,
        hashed: str,
        salt: str,
    ) -> bool:
        """Verify password against hash.
        
        Args:
            password: Password to verify
            hashed: Hashed password
            salt: Base64-encoded salt
            
        Returns:
            True if password matches
        """
        new_hash, _ = self.hash_password(password, salt)
        return new_hash == hashed

    def mask_sensitive_data(
        self,
        data: Dict[str, Any],
        sensitive_fields: List[str],
    ) -> Dict[str, Any]:
        """Mask sensitive fields in data.
        
        Args:
            data: Data dictionary
            sensitive_fields: Fields to mask
            
        Returns:
            Dictionary with masked fields
        """
        masked = data.copy()
        field_type_map = {
            "email": self.data_masker.mask_email,
            "phone": self.data_masker.mask_phone,
            "ssn": self.data_masker.mask_ssn,
            "card": self.data_masker.mask_credit_card,
        }

        for field in sensitive_fields:
            if field in masked:
                for key, masker in field_type_map.items():
                    if key in field.lower():
                        masked[field] = masker(str(masked[field]))
                        break
                else:
                    masked[field] = "***MASKED***"

        return masked

    def generate_secure_token(
        self,
        length: int = 32,
    ) -> str:
        """Generate cryptographically secure token.
        
        Args:
            length: Token length in bytes
            
        Returns:
            Hex-encoded secure token
        """
        return os.urandom(length).hex()
