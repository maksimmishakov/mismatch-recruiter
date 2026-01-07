"""Load testing with Locust."""
from locust import HttpUser, task, between
import random

class MisMatchUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a Locust user starts executing those tasks."""
        self.access_token = None
    
    @task(3)
    def view_health(self):
        """Check health endpoint."""
        self.client.get("/health")
    
    @task(2)
    def view_candidates(self):
        """View list of candidates with pagination."""
        page = random.randint(1, 5)
        self.client.get(f"/api/candidates?page={page}&per_page=20")
    
    @task(2)
    def view_jobs(self):
        """View list of jobs."""
        page = random.randint(1, 5)
        self.client.get(f"/api/jobs?page={page}&per_page=20")
    
    @task(1)
    def view_matches(self):
        """View list of matches."""
        self.client.get("/api/matches")
