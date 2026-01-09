# Lamoda API Client - OAuth2 and job/candidate integration

import logging
import requests
from typing import Optional, Dict, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class LamodaAPIClient:
    """Client for Lamoda API integration."""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.api_base = 'https://api.lamoda.ru'
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
    def get_open_positions(self, limit: int = 50) -> Optional[List[Dict]]:
        """Fetch all open positions from Lamoda."""
        try:
            response = requests.get(
                f'{self.api_base}/v1/jobs',
                headers=self.headers,
                params={'limit': limit, 'status': 'open'}
            )
            if response.status_code == 200:
                jobs = response.json().get('data', [])
                logger.info(f'Fetched {len(jobs)} open positions from Lamoda')
                return jobs
            else:
                logger.error(f'Failed to fetch positions: {response.text}')
                return None
        except Exception as e:
            logger.error(f'Error fetching positions: {e}')
            return None
    
    def get_position_by_id(self, position_id: str) -> Optional[Dict]:
        """Fetch specific position details."""
        try:
            response = requests.get(
                f'{self.api_base}/v1/jobs/{position_id}',
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json().get('data')
            else:
                logger.error(f'Failed to fetch position {position_id}')
                return None
        except Exception as e:
            logger.error(f'Error fetching position: {e}')
            return None
    
    def get_candidates_for_position(self, position_id: str) -> Optional[List[Dict]]:
        """Fetch candidates applied to specific position."""
        try:
            response = requests.get(
                f'{self.api_base}/v1/jobs/{position_id}/applications',
                headers=self.headers
            )
            if response.status_code == 200:
                candidates = response.json().get('data', [])
                logger.info(f'Fetched {len(candidates)} candidates for position {position_id}')
                return candidates
            else:
                logger.error(f'Failed to fetch candidates: {response.text}')
                return None
        except Exception as e:
            logger.error(f'Error fetching candidates: {e}')
            return None
    
    def update_application_status(
        self,
        application_id: str,
        status: str,
        notes: str = ''
    ) -> bool:
        """Update application status in Lamoda."""
        try:
            response = requests.patch(
                f'{self.api_base}/v1/applications/{application_id}',
                headers=self.headers,
                json={'status': status, 'notes': notes}
            )
            if response.status_code in [200, 204]:
                logger.info(f'Updated application {application_id} to {status}')
                return True
            else:
                logger.error(f'Failed to update application: {response.text}')
                return False
        except Exception as e:
            logger.error(f'Error updating application: {e}')
            return False
