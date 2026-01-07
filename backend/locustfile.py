from locust import HttpUser, task, between
import random

class APIUser(HttpUser):
    """Simulated user for load testing."""
    wait_time = between(1, 3)

    @task(3)
    def health_check(self):
        """Check health endpoint."""
        self.client.get('/health')

    @task(2)
    def get_candidates(self):
        """Get list of candidates."""
        self.client.get('/api/v1/candidates')

    @task(2)
    def search_candidates(self):
        """Search candidates by skill."""
        skill = random.choice(['Python', 'JavaScript', 'React', 'Node.js', 'PostgreSQL'])
        self.client.get(f'/api/v1/candidates/search?skill={skill}')

    @task(1)
    def create_match(self):
        """Create a new match."""
        payload = {
            'job_id': random.randint(1, 100),
            'candidate_id': random.randint(1, 1000),
            'score': random.uniform(0.5, 1.0)
        }
        self.client.post('/api/v1/matches', json=payload)
