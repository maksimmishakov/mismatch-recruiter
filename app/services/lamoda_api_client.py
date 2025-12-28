"""Lamoda API Client - Integration with Lamoda job portal
Phase 5 Step 4 - Job import, candidate submission, placement tracking
Supports: Job import, candidate sync, placement results, error handling
"""
import logging
import hmac
import hashlib
import json
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import aiohttp
import time

logger = logging.getLogger(__name__)


class LamodaJobStatus(Enum):
    """Lamoda job statuses"""
    OPEN = "open"
    CLOSED = "closed"
    ON_REVIEW = "on_review"
    ARCHIVED = "archived"


class PlacementStatus(Enum):
    """Placement statuses"""
    SUBMITTED = "submitted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEW_PASSED = "interview_passed"
    REJECTED = "rejected"
    HIRED = "hired"
    OFFER_SENT = "offer_sent"
    CANCELLED = "cancelled"


@dataclass
class LamodaJob:
    """Lamoda job data structure"""
    id: str
    title: str
    description: str
    company: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    currency: str = "RUB"
    location: str = ""
    job_type: str = "full_time"
    status: str = LamodaJobStatus.OPEN.value
    created_at: datetime = None
    updated_at: datetime = None
    category: str = ""
    experience_level: str = ""
    required_skills: List[str] = None
    experience_years: int = 0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
        if self.required_skills is None:
            self.required_skills = []

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data


@dataclass
class CandidateProfile:
    """Candidate profile for submission"""
    id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    experience_years: int = 0
    skills: List[str] = None
    education: str = ""
    resume_text: str = ""
    match_score: float = 0.0
    explanation: str = ""

    def __post_init__(self):
        if self.skills is None:
            self.skills = []


@dataclass
class Placement:
    """Placement data structure"""
    id: str
    job_id: str
    candidate_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None
    interview_date: Optional[datetime] = None
    feedback: Optional[str] = None


class LamodaAPIError(Exception):
    """Lamoda API error"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class LamodaAPIClient:
    """Client for Lamoda API integration"""
    def __init__(self, api_key: str, api_secret: str, api_url: str, 
                 environment: str = "sandbox", timeout: int = 30):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = api_url
        self.environment = environment
        self.timeout = timeout
        self.rate_limit_remaining = 1000
        self.rate_limit_reset = None
        self.session = None

    def _generate_signature(self, method: str, path: str, body: str = "") -> str:
        """Generate HMAC-SHA256 signature for request"""
        timestamp = int(time.time())
        signature_string = f"{method}\n{path}\n{timestamp}\n{body}"
        signature = hmac.new(
            self.api_secret.encode(),
            signature_string.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"Lamoda {self.api_key}:{signature}:{timestamp}"

    async def _make_request(self, method: str, endpoint: str, 
                           data: Optional[Dict] = None,
                           params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to Lamoda API"""
        url = f"{self.api_url}{endpoint}"
        body = json.dumps(data) if data else ""
        signature = self._generate_signature(method, endpoint, body)

        headers = {
            "Authorization": signature,
            "Content-Type": "application/json",
            "User-Agent": "LamodaAIRecruiter/1.0"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method,
                    url,
                    headers=headers,
                    json=data,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    # Update rate limit info
                    if "X-RateLimit-Remaining" in response.headers:
                        self.rate_limit_remaining = int(
                            response.headers["X-RateLimit-Remaining"]
                        )
                    if "X-RateLimit-Reset" in response.headers:
                        self.rate_limit_reset = int(
                            response.headers["X-RateLimit-Reset"]
                        )

                    if response.status == 429:
                        # Rate limited - implement exponential backoff
                        wait_time = int(response.headers.get(
                            "Retry-After", 60
                        ))
                        logger.warning(f"Rate limited, waiting {wait_time}s")
                        await asyncio.sleep(wait_time)
                        return await self._make_request(method, endpoint, data, params)

                    if response.status >= 400:
                        error_text = await response.text()
                        logger.error(f"API Error: {response.status} - {error_text}")
                        raise LamodaAPIError(error_text, response.status)

                    return await response.json()
        except asyncio.TimeoutError:
            logger.error("API request timeout")
            raise LamodaAPIError("API request timeout")
        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise

    async def get_jobs(self, skip: int = 0, limit: int = 50,
                      status: Optional[str] = None,
                      created_after: Optional[datetime] = None) -> List[LamodaJob]:
        """Get jobs from Lamoda"""
        params = {
            "skip": skip,
            "limit": min(limit, 100)  # Lamoda max limit is 100
        }
        if status:
            params["status"] = status
        if created_after:
            params["created_after"] = created_after.isoformat()

        response = await self._make_request("GET", "/jobs", params=params)
        jobs = []
        for job_data in response.get("jobs", []):
            job = LamodaJob(
                id=job_data["id"],
                title=job_data["title"],
                description=job_data["description"],
                company=job_data["company"],
                salary_from=job_data.get("salary_from"),
                salary_to=job_data.get("salary_to"),
                location=job_data.get("location", ""),
                status=job_data.get("status", "open"),
                category=job_data.get("category", ""),
                experience_level=job_data.get("experience_level", ""),
                required_skills=job_data.get("required_skills", []),
                experience_years=job_data.get("experience_years", 0)
            )
            jobs.append(job)
        return jobs

    async def get_job(self, job_id: str) -> LamodaJob:
        """Get job details"""
        response = await self._make_request("GET", f"/jobs/{job_id}")
        job_data = response["job"]
        return LamodaJob(
            id=job_data["id"],
            title=job_data["title"],
            description=job_data["description"],
            company=job_data["company"],
            salary_from=job_data.get("salary_from"),
            salary_to=job_data.get("salary_to"),
            location=job_data.get("location", ""),
            status=job_data.get("status", "open")
        )

    async def submit_candidates(self, job_id: str, 
                               candidates: List[CandidateProfile]) -> Dict[str, Any]:
        """Submit candidates for a job"""
        candidate_data = [{
            "candidate_id": c.id,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "email": c.email,
            "phone": c.phone,
            "experience_years": c.experience_years,
            "skills": c.skills,
            "match_score": c.match_score,
            "explanation": c.explanation
        } for c in candidates]

        payload = {
            "job_id": job_id,
            "candidates": candidate_data
        }

        response = await self._make_request(
            "POST",
            "/placements",
            data=payload
        )
        logger.info(f"Submitted {len(candidates)} candidates for job {job_id}")
        return response

    async def get_placements(self, job_id: Optional[str] = None,
                            date_from: Optional[datetime] = None,
                            date_to: Optional[datetime] = None) -> List[Placement]:
        """Get placement results"""
        params = {}
        if job_id:
            params["job_id"] = job_id
        if date_from:
            params["date_from"] = date_from.isoformat()
        if date_to:
            params["date_to"] = date_to.isoformat()

        response = await self._make_request("GET", "/placements", params=params)
        placements = []
        for placement_data in response.get("placements", []):
            placement = Placement(
                id=placement_data["id"],
                job_id=placement_data["job_id"],
                candidate_id=placement_data["candidate_id"],
                status=placement_data["status"],
                created_at=datetime.fromisoformat(placement_data["created_at"]),
                updated_at=datetime.fromisoformat(placement_data["updated_at"]),
                notes=placement_data.get("notes"),
                interview_date=datetime.fromisoformat(placement_data["interview_date"]) 
                                if placement_data.get("interview_date") else None,
                feedback=placement_data.get("feedback")
            )
            placements.append(placement)
        return placements

    async def update_placement(self, placement_id: str, status: str,
                              notes: Optional[str] = None) -> Dict[str, Any]:
        """Update placement status"""
        payload = {
            "status": status,
            "notes": notes,
            "updated_at": datetime.utcnow().isoformat()
        }
        response = await self._make_request(
            "PUT",
            f"/placements/{placement_id}",
            data=payload
        )
        logger.info(f"Updated placement {placement_id} to {status}")
        return response

    async def verify_connection(self) -> bool:
        """Verify API connection with test call"""
        try:
            await self.get_jobs(limit=1)
            logger.info("✅ Connected to Lamoda API")
            return True
        except Exception as e:
            logger.error(f"❌ Connection failed: {str(e)}")
            return False

    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Get current rate limit info"""
        return {
            "remaining": self.rate_limit_remaining,
            "reset_at": datetime.fromtimestamp(self.rate_limit_reset) 
                        if self.rate_limit_reset else None
        }


if __name__ == "__main__":
    logger.info("Lamoda API Client initialized")
