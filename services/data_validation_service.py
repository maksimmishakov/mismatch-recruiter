import re
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class ValidationType(Enum):
    EMAIL = 'email'
    PHONE = 'phone'
    URL = 'url'
    NUMERIC = 'numeric'
    ALPHANUMERIC = 'alphanumeric'
    DATE = 'date'
    CUSTOM = 'custom'

@dataclass
class ValidationError:
    field: str
    message: str
    error_code: str
    value: Any = None

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[ValidationError]
    timestamp: datetime
    processed_data: Optional[Dict] = None

class DataValidationService:
    def __init__(self):
        self.validators = {}
        self.validation_rules = {}
        self._setup_default_validators()
    
    def _setup_default_validators(self):
        """Setup default validators for common types"""
        self.validators = {
            ValidationType.EMAIL: self._validate_email,
            ValidationType.PHONE: self._validate_phone,
            ValidationType.URL: self._validate_url,
            ValidationType.NUMERIC: self._validate_numeric,
            ValidationType.ALPHANUMERIC: self._validate_alphanumeric,
            ValidationType.DATE: self._validate_date,
        }
    
    def _validate_email(self, value: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, value))
    
    def _validate_phone(self, value: str) -> bool:
        """Validate phone number format"""
        pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
        return bool(re.match(pattern, value))
    
    def _validate_url(self, value: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)$'
        return bool(re.match(pattern, value))
    
    def _validate_numeric(self, value: Any) -> bool:
        """Validate numeric value"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False
    
    def _validate_alphanumeric(self, value: str) -> bool:
        """Validate alphanumeric string"""
        return value.replace(' ', '').replace('_', '').isalnum()
    
    def _validate_date(self, value: str, format: str = '%Y-%m-%d') -> bool:
        """Validate date format"""
        try:
            datetime.strptime(value, format)
            return True
        except (ValueError, TypeError):
            return False
    
    def add_custom_validator(self, 
                           name: str,
                           validator_func: Callable[[Any], bool]) -> None:
        """Add custom validator function"""
        self.validators[name] = validator_func
        logger.info(f'Custom validator added: {name}')
    
    def add_validation_rule(self,
                          field: str,
                          rules: Dict[str, Any]) -> None:
        """Add validation rule for a field"""
        self.validation_rules[field] = rules
        logger.info(f'Validation rule added for field: {field}')
    
    def validate_field(self,
                      field_name: str,
                      value: Any,
                      validation_type: ValidationType) -> Optional[ValidationError]:
        """Validate a single field"""
        if value is None:
            return ValidationError(
                field=field_name,
                message='Field cannot be None',
                error_code='NULL_VALUE'
            )
        
        if validation_type in self.validators:
            if not self.validators[validation_type](value):
                return ValidationError(
                    field=field_name,
                    message=f'Invalid {validation_type.value}',
                    error_code=f'INVALID_{validation_type.value.upper()}',
                    value=value
                )
        
        return None
    
    def validate_object(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate entire object based on rules"""
        errors = []
        processed_data = {}
        
        for field, value in data.items():
            if field in self.validation_rules:
                rule = self.validation_rules[field]
                
                # Check required
                if rule.get('required', False) and value is None:
                    errors.append(ValidationError(
                        field=field,
                        message='Field is required',
                        error_code='REQUIRED_FIELD'
                    ))
                    continue
                
                # Check type
                if 'type' in rule:
                    error = self.validate_field(field, value, rule['type'])
                    if error:
                        errors.append(error)
                        continue
                
                # Check length
                if 'min_length' in rule and isinstance(value, str):
                    if len(value) < rule['min_length']:
                        errors.append(ValidationError(
                            field=field,
                            message=f'Minimum length is {rule["min_length"]}',
                            error_code='MIN_LENGTH_VIOLATION',
                            value=value
                        ))
                
                if 'max_length' in rule and isinstance(value, str):
                    if len(value) > rule['max_length']:
                        errors.append(ValidationError(
                            field=field,
                            message=f'Maximum length is {rule["max_length"]}',
                            error_code='MAX_LENGTH_VIOLATION',
                            value=value
                        ))
                
                # Check range
                if 'min_value' in rule and isinstance(value, (int, float)):
                    if value < rule['min_value']:
                        errors.append(ValidationError(
                            field=field,
                            message=f'Minimum value is {rule["min_value"]}',
                            error_code='MIN_VALUE_VIOLATION',
                            value=value
                        ))
                
                if 'max_value' in rule and isinstance(value, (int, float)):
                    if value > rule['max_value']:
                        errors.append(ValidationError(
                            field=field,
                            message=f'Maximum value is {rule["max_value"]}',
                            error_code='MAX_VALUE_VIOLATION',
                            value=value
                        ))
            
            processed_data[field] = value
        
        is_valid = len(errors) == 0
        logger.info(f'Object validation: {"valid" if is_valid else "invalid"}')
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            timestamp=datetime.now(),
            processed_data=processed_data if is_valid else None
        )
    
    def validate_batch(self, 
                      data_list: List[Dict[str, Any]]) -> List[ValidationResult]:
        """Validate multiple objects"""
        results = []
        for data in data_list:
            results.append(self.validate_object(data))
        
        logger.info(f'Batch validation completed: {len(data_list)} objects')
        return results
    
    def get_validation_stats(self) -> Dict:
        """Get validation statistics"""
        return {
            'registered_validators': len(self.validators),
            'registered_rules': len(self.validation_rules),
            'custom_validators': sum(1 for v in self.validators.keys() 
                                    if isinstance(v, str))
        }
