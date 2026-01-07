"""Load testing with Locust"""
from locust import HttpUser, task, between, events
import random
import time

class CandidateUser(HttpUser):
    """Simulates candidate browsing and applying"""
    wait_time = between(1, 3)
    
    @task(5)
    def get_candidates(self):
        """Browse candidates list"""
        self.client.get("/api/candidates", name="/api/candidates")
    
    @task(3)
    def get_candidate_detail(self):
        """View single candidate"""
        candidate_id = random.randint(1, 100)
        self.client.get(f"/api/candidates/{candidate_id}", name="/api/candidates/[id]")
    
    @task(2)
    def create_match(self):
        """Create a match"""
        self.client.post(
            "/api/matches",
            json={
                "candidate_id": random.randint(1, 100),
                "job_id": random.randint(1, 50)
            },
            name="/api/matches"
        )
    
    @task(1)
    def health_check(self):
        """Check server health"""
        self.client.get("/health", name="/health")


class RecruiterUser(HttpUser):
    """Simulates recruiter managing jobs"""
    wait_time = between(2, 5)
    
    @task(4)
    def get_jobs(self):
        """Browse jobs"""
        self.client.get("/api/jobs", name="/api/jobs")
    
    @task(3)
    def get_job_detail(self):
        """View single job"""
        job_id = random.randint(1, 50)
        self.client.get(f"/api/jobs/{job_id}", name="/api/jobs/[id]")
    
    @task(2)
    def create_job(self):
        """Post new job"""
        self.client.post(
            "/api/jobs",
            json={
                "title": f"Job {random.randint(1, 1000)}",
                "description": "Test job",
                "salary_min": 50000,
                "salary_max": 150000,
                "required_skills": ["Python", "React"]
            },
            name="/api/jobs POST"
        )
    
    @task(1)
    def get_matches(self):
        """View matches"""
        self.client.get("/api/matches", name="/api/matches")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("
🚀 Load testing started!")
    print(f"Target: {environment.host}")
    print(f"Users: {environment.runner.target_user_count}")

@events.test_stop.add_listener  
def on_test_stop(environment, **kwargs):
    print("
✅ Load testing completed!")
    print(f"Total requests: {environment.stats.total.num_requests}")
    print(f"Total failures: {environment.stats.total.num_failures}")
    print(f"Average response time: {environment.stats.total.avg_response_time}ms")
