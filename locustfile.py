from locust import HttpUser, task, between
import random

class CandidateUser(HttpUser):
    """Simulates users interacting with candidates API"""
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a user starts, login here if needed"""
        self.candidate_ids = []
    
    @task(3)
    def get_health(self):
        """Get health status - 3x more frequent"""
        self.client.get('/health')
    
    @task(2)
    def get_candidates(self):
        """Get list of candidates - 2x frequent"""
        response = self.client.get('/api/candidates')
        if response.status_code == 200:
            try:
                self.candidate_ids = response.json()
            except:
                pass
    
    @task(1)
    def create_candidate(self):
        """Create a new candidate - 1x frequent"""
        candidate_data = {
            'name': f'Test Candidate {random.randint(1, 1000)}',
            'email': f'candidate{random.randint(1, 10000)}@test.com',
            'position': random.choice(['Python Dev', 'Node Dev', 'DevOps', 'QA']),
            'status': 'pending'
        }
        self.client.post('/api/candidates', json=candidate_data)
    
    @task(1)
    def get_candidate_detail(self):
        """Get candidate details if any exist"""
        if self.candidate_ids:
            candidate_id = random.choice(self.candidate_ids)
            self.client.get(f'/api/candidates/{candidate_id}')
