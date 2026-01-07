from locust import HttpUser, task, between, events
import json
import random

class RecruitmentUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Setup: login before running tasks""        self.token = None
    
    @task(3)
    def get_candidates(self):
        """Load test GET /api/candidates""        response = self.client.get(
            "/api/candidates",
            params={"page": 1, "per_page": 20}
        )
        if response.status_code == 200:
            print(f"✅ GET candidates: {response.status_code}")
    
    @task(2)
    def get_jobs(self):
        """Load test GET /api/jobs""        response = self.client.get(
            "/api/jobs",
            params={"page": 1, "per_page": 20}
        )
        if response.status_code == 200:
            print(f"✅ GET jobs: {response.status_code}")
    
    @task(2)
    def get_matches(self):
        """Load test GET /api/matches""        response = self.client.get(
            "/api/matches",
            params={"page": 1, "per_page": 20}
        )
        if response.status_code == 200:
            print(f"✅ GET matches: {response.status_code}")
    
    @task(1)
    def create_candidate(self):
        """Load test POST /api/candidates""        data = {
            "name": f"Test Candidate {random.randint(1, 1000)}",
            "email": f"test{random.randint(1, 100000)}@example.com",
            "skills": ["Python", "React"],
            "experience_years": random.randint(1, 10)
        }
        response = self.client.post(
            "/api/candidates",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code in [201, 400]:
            print(f"✅ POST candidate: {response.status_code}")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("🚀 Load testing started!")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("✅ Load testing completed!")
