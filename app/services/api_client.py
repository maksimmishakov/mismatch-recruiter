"""API Client for MisMatch Recruitment Platform

Provides abstraction layer for communicating with the backend API.
"""

import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class Resume:
    """Resume data model"""
    id: int
    user_id: str
    filename: str
    full_name: str
    email: str
    phone: str
    skills: List[str]
    years_experience: int
    current_job_title: str
    location: str
    uploaded_at: str
    confidence: float  # 0-1


@dataclass
class Job:
    """Job listing data model"""
    id: int
    title: str
    company: str
    location: str
    salary_min: int
    salary_max: int
    description: str
    required_skills: List[str]
    years_experience_required: int
    published_at: str
    status: str  # 'active', 'closed', 'archived'


@dataclass
class Match:
    """Job-Resume match data model"""
    id: int
    resume_id: int
    job_id: int
    score: int  # 0-100
    skills_match: int
    experience_match: int
    seniority_match: int
    match_details: Dict[str, Any]
    created_at: str


@dataclass
class KPIStats:
    """KPI statistics"""
    total_candidates: int
    total_jobs: int
    excellent_matches: int  # >= 90
    average_score: float
    matched_candidates: int
    conversion_rate: float


class APIClient:
    """MisMatch API Client"""

    def __init__(self, base_url: str = 'http://localhost:5000', timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """Make HTTP request to API"""
        url = f'{self.base_url}/api{endpoint}'
        kwargs['timeout'] = kwargs.get('timeout', self.timeout)

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f'API request failed: {e}')
            raise

    # RESUME ENDPOINTS
    def upload_resume(self, file_path: str) -> Resume:
        """Upload and parse resume"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self._make_request('POST', '/resumes/upload', files=files)
        return Resume(**response.json())

    def list_resumes(self) -> List[Resume]:
        """Get all resumes"""
        response = self._make_request('GET', '/resumes')
        return [Resume(**r) for r in response.json()]

    def get_resume(self, resume_id: int) -> Resume:
        """Get resume by ID"""
        response = self._make_request('GET', f'/resumes/{resume_id}')
        return Resume(**response.json())

    def delete_resume(self, resume_id: int) -> None:
        """Delete resume"""
        self._make_request('DELETE', f'/resumes/{resume_id}')

    # JOB ENDPOINTS
    def list_jobs(
        self,
        company: Optional[str] = None,
        location: Optional[str] = None,
        min_salary: Optional[int] = None,
        max_salary: Optional[int] = None
    ) -> List[Job]:
        """Get jobs with optional filters"""
        params = {}
        if company:
            params['company'] = company
        if location:
            params['location'] = location
        if min_salary:
            params['min_salary'] = min_salary
        if max_salary:
            params['max_salary'] = max_salary

        response = self._make_request('GET', '/jobs', params=params)
        return [Job(**j) for j in response.json()]

    def get_job(self, job_id: int) -> Job:
        """Get job by ID"""
        response = self._make_request('GET', f'/jobs/{job_id}')
        return Job(**response.json())

    def search_jobs(self, query: str) -> List[Job]:
        """Search jobs by query"""
        response = self._make_request('GET', '/jobs/search', params={'q': query})
        return [Job(**j) for j in response.json()]

    def create_job(self, job_data: Dict[str, Any]) -> Job:
        """Create new job"""
        response = self._make_request(
            'POST',
            '/jobs',
            json=job_data,
            headers={'Content-Type': 'application/json'}
        )
        return Job(**response.json())

    def sync_jobs(self) -> Dict[str, int]:
        """Sync jobs from external sources"""
        response = self._make_request('POST', '/jobs/sync')
        return response.json()

    # MATCHING ENDPOINTS
    def create_matches(self, job_id: int) -> List[Match]:
        """Generate matches for job"""
        response = self._make_request(
            'POST',
            '/matches',
            json={'job_id': job_id},
            headers={'Content-Type': 'application/json'}
        )
        return [Match(**m) for m in response.json()]

    def get_matches_by_job(self, job_id: int, limit: int = 50) -> List[Match]:
        """Get matches for job"""
        response = self._make_request(
            'GET',
            f'/matches/by-job/{job_id}',
            params={'limit': limit}
        )
        return [Match(**m) for m in response.json()]

    def get_matches_by_resume(self, resume_id: int) -> List[Match]:
        """Get matches for resume"""
        response = self._make_request('GET', f'/matches/by-resume/{resume_id}')
        return [Match(**m) for m in response.json()]

    def update_match_status(self, match_id: int, status: str) -> Match:
        """Update match status"""
        response = self._make_request(
            'PATCH',
            f'/matches/{match_id}',
            json={'status': status},
            headers={'Content-Type': 'application/json'}
        )
        return Match(**response.json())

    # ANALYTICS ENDPOINTS
    def get_kpi_stats(self) -> KPIStats:
        """Get KPI statistics"""
        response = self._make_request('GET', '/stats/kpis')
        return KPIStats(**response.json())

    def get_match_trends(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get matching trends"""
        response = self._make_request('GET', '/stats/trends', params={'days': days})
        return response.json()

    def get_skill_analysis(self) -> Dict[str, Any]:
        """Get skill demand analysis"""
        response = self._make_request('GET', '/stats/skills')
        return response.json()

    # EXPORT ENDPOINTS
    def export_matches(self, job_id: int, format: str = 'csv') -> bytes:
        """Export matches to CSV or Excel"""
        response = self._make_request(
            'GET',
            f'/export/matches/{job_id}',
            params={'format': format}
        )
        return response.content

    def export_candidates(self, format: str = 'csv') -> bytes:
        """Export candidates to CSV or Excel"""
        response = self._make_request(
            'GET',
            '/export/candidates',
            params={'format': format}
        )
        return response.content
