"""Data Validation Service for data integrity and business rule enforcement.

Provides validation for candidates, jobs, salary predictions, and matches
ensuring data consistency across the application.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime


class DataValidationService:
    """Service for validating candidate, job, and salary data."""

    # Validation rules
    MIN_SALARY = 15000
    MAX_SALARY = 500000
    MIN_EXPERIENCE = 0
    MAX_EXPERIENCE = 60
    VALID_JOB_TYPES = ['Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship']
    VALID_SKILL_LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Expert']

    def __init__(self):
        """Initialize the validation service."""
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_candidate(self, candidate_data: Dict[str, Any]) -> bool:
        """Validate candidate data for completeness and correctness.
        
        Args:
            candidate_data: Dictionary containing candidate information
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        self.errors = []
        self.warnings = []

        if not candidate_data:
            self.errors.append('Candidate data cannot be empty')
            return False

        # Required fields
        required_fields = ['name', 'email', 'phone']
        for field in required_fields:
            if field not in candidate_data or not candidate_data[field]:
                self.errors.append(f'Required field missing: {field}')

        # Email validation
        if 'email' in candidate_data:
            if '@' not in candidate_data['email']:
                self.errors.append('Invalid email format')

        # Experience validation
        if 'experience_years' in candidate_data:
            exp = candidate_data['experience_years']
            if not isinstance(exp, (int, float)) or exp < self.MIN_EXPERIENCE or exp > self.MAX_EXPERIENCE:
                self.errors.append(
                    f'Experience must be between {self.MIN_EXPERIENCE} and {self.MAX_EXPERIENCE} years'
                )

        # Skills validation
        if 'skills' in candidate_data and candidate_data['skills']:
            if not isinstance(candidate_data['skills'], list):
                self.errors.append('Skills must be a list')
            elif len(candidate_data['skills']) > 50:
                self.warnings.append('Candidate has an unusual number of skills (>50)')

        return len(self.errors) == 0

    def validate_job(self, job_data: Dict[str, Any]) -> bool:
        """Validate job posting data.
        
        Args:
            job_data: Dictionary containing job information
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        self.errors = []
        self.warnings = []

        if not job_data:
            self.errors.append('Job data cannot be empty')
            return False

        # Required fields
        required_fields = ['title', 'company', 'description']
        for field in required_fields:
            if field not in job_data or not job_data[field]:
                self.errors.append(f'Required field missing: {field}')

        # Title validation
        if 'title' in job_data and len(str(job_data['title'])) < 3:
            self.errors.append('Job title must be at least 3 characters')

        # Job type validation
        if 'job_type' in job_data and job_data['job_type'] not in self.VALID_JOB_TYPES:
            self.warnings.append(
                f'Unusual job type: {job_data["job_type"]}. Expected one of {self.VALID_JOB_TYPES}'
            )

        # Required experience validation
        if 'required_experience' in job_data:
            exp = job_data['required_experience']
            if not isinstance(exp, (int, float)) or exp < 0:
                self.errors.append('Required experience must be a non-negative number')

        # Salary validation
        if 'salary_min' in job_data or 'salary_max' in job_data:
            self.validate_salary_range(
                job_data.get('salary_min'),
                job_data.get('salary_max')
            )

        return len(self.errors) == 0

    def validate_salary(self, salary: float) -> bool:
        """Validate salary value.
        
        Args:
            salary: Salary amount to validate
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        self.errors = []
        self.warnings = []

        if not isinstance(salary, (int, float)):
            self.errors.append('Salary must be a number')
            return False

        if salary < self.MIN_SALARY:
            self.warnings.append(f'Salary is below minimum threshold ({self.MIN_SALARY})')
            return True

        if salary > self.MAX_SALARY:
            self.warnings.append(f'Salary exceeds maximum threshold ({self.MAX_SALARY})')
            return True

        return True

    def validate_salary_range(self, min_salary: Optional[float], max_salary: Optional[float]) -> bool:
        """Validate salary range.
        
        Args:
            min_salary: Minimum salary
            max_salary: Maximum salary
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        if min_salary is None or max_salary is None:
            return True

        if not isinstance(min_salary, (int, float)) or not isinstance(max_salary, (int, float)):
            self.errors.append('Salary values must be numbers')
            return False

        if min_salary < 0 or max_salary < 0:
            self.errors.append('Salary values cannot be negative')
            return False

        if min_salary > max_salary:
            self.errors.append('Minimum salary cannot be greater than maximum salary')
            return False

        if max_salary - min_salary > 100000:
            self.warnings.append('Large salary range detected')

        return True

    def validate_match(self, match_data: Dict[str, Any]) -> bool:
        """Validate match data (candidate-job pairing).
        
        Args:
            match_data: Dictionary containing match information
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        self.errors = []
        self.warnings = []

        required_fields = ['candidate_id', 'job_id', 'match_score']
        for field in required_fields:
            if field not in match_data or match_data[field] is None:
                self.errors.append(f'Required field missing: {field}')

        if 'match_score' in match_data:
            score = match_data['match_score']
            if not isinstance(score, (int, float)) or score < 0 or score > 100:
                self.errors.append('Match score must be a number between 0 and 100')

        return len(self.errors) == 0

    def get_errors(self) -> List[str]:
        """Get validation errors.
        
        Returns:
            List of error messages
        """
        return self.errors

    def get_warnings(self) -> List[str]:
        """Get validation warnings.
        
        Returns:
            List of warning messages
        """
        return self.warnings

    def clear_messages(self) -> None:
        """Clear error and warning messages."""
        self.errors = []
        self.warnings = []
