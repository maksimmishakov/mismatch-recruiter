import logging
import requests
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class MismatchClient:
    """Client for Mismatch API integration"""
    
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        api_url: str = "https://api.Mismatch.ru"
    ):
        """Initialize Mismatch client
        
        Args:
            api_key: Mismatch API key
            api_secret: Mismatch API secret
            api_url: Base API URL (default: Mismatch production)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def _build_url(self, endpoint: str) -> str:
        """Build full API URL
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Full URL
        """
        return f"{self.api_url}/{endpoint}"
    
    def get_jobs(
        self,
        filters: Optional[Dict] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get jobs from Mismatch
        
        Args:
            filters: Optional filters (category, region, etc.)
            limit: Maximum number of jobs to retrieve
            
        Returns:
            List of job objects
        """
        try:
            params = {"limit": limit}
            if filters:
                params.update(filters)
            
            response = requests.get(
                self._build_url("jobs"),
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                jobs = response.json().get("data", [])
                logger.info(f"Retrieved {len(jobs)} jobs from Mismatch")
                return jobs
            else:
                logger.error(f"Failed to get jobs: {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving jobs: {str(e)}")
            return []
    
    def submit_candidates(
        self,
        job_id: int,
        candidates: List[int]
    ) -> Dict:
        """Submit candidates for a job
        
        Args:
            job_id: Mismatch job ID
            candidates: List of candidate/resume IDs
            
        Returns:
            Submission result
        """
        try:
            payload = {
                "job_id": job_id,
                "candidate_ids": candidates,
                "submitted_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                self._build_url(f"jobs/{job_id}/candidates"),
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                logger.info(f"Submitted {len(candidates)} candidates for job {job_id}")
                return result
            else:
                logger.error(f"Failed to submit candidates: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Error submitting candidates: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_placements(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """Get placement results from Mismatch
        
        Args:
            start_date: Start date for filtering (ISO format)
            end_date: End date for filtering (ISO format)
            
        Returns:
            List of placements
        """
        try:
            params = {}
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date
            
            response = requests.get(
                self._build_url("placements"),
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                placements = response.json().get("data", [])
                logger.info(f"Retrieved {len(placements)} placements")
                return placements
            else:
                logger.error(f"Failed to get placements: {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving placements: {str(e)}")
            return []
    
    def update_placement_status(
        self,
        placement_id: int,
        status: str,
        notes: Optional[str] = None
    ) -> Dict:
        """Update placement status
        
        Args:
            placement_id: Placement ID
            status: New status (hired, rejected, interview, etc.)
            notes: Optional notes
            
        Returns:
            Update result
        """
        try:
            payload = {
                "status": status,
                "updated_at": datetime.now().isoformat()
            }
            if notes:
                payload["notes"] = notes
            
            response = requests.put(
                self._build_url(f"placements/{placement_id}"),
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Updated placement {placement_id} to {status}")
                return result
            else:
                logger.error(f"Failed to update placement: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Error updating placement: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def sync_matching_results(
        self,
        job_id: int,
        matches: List[Dict]
    ) -> Dict:
        """Sync matching results to Mismatch
        
        Args:
            job_id: Job ID
            matches: List of match results with scores
            
        Returns:
            Sync result
        """
        try:
            # Format matches for Mismatch
            candidates = [
                {
                    "candidate_id": match.get("candidate_id"),
                    "score": match.get("score"),
                    "recommendation": match.get("recommendation")
                }
                for match in matches
            ]
            
            payload = {
                "job_id": job_id,
                "candidates": candidates,
                "synced_at": datetime.now().isoformat()
            }
            
            response = requests.post(
                self._build_url(f"jobs/{job_id}/sync-results"),
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                logger.info(f"Synced {len(candidates)} results for job {job_id}")
                return result
            else:
                logger.error(f"Failed to sync results: {response.text}")
                return {"status": "error", "message": response.text}
                
        except Exception as e:
            logger.error(f"Error syncing results: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def test_connection(self) -> bool:
        """Test Mismatch API connection
        
        Returns:
            True if connection successful
        """
        try:
            response = requests.get(
                self._build_url("health"),
                headers=self.headers,
                timeout=5
            )
            
            if response.status_code == 200:
                logger.info("Mismatch API connection successful")
                return True
            else:
                logger.error(f"Mismatch API error: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to connect to Mismatch API: {str(e)}")
            return False
