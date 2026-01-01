"""Load Testing Script for MisMatch Recruiter
Uses Locust framework to simulate concurrent users
"""

from locust import HttpUser, task, between, events
import json
import time
import random
from datetime import datetime


class MismatchUser(HttpUser):
    """Simulates a typical MisMatch user behavior"""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    def on_start(self):
        """Called when a simulated user starts"""
        self.authenticate()
    
    def authenticate(self):
        """Login and get JWT token"""
        response = self.client.post("/api/v1/auth/login", 
            json={
                "email": "testuser@example.com",
                "password": "TestPassword123!"
            }
        )
        if response.status_code == 200:
            try:
                self.token = response.json().get("access_token")
                self.headers = {"Authorization": f"Bearer {self.token}"}
            except:
                self.token = None
        else:
            self.token = None
    
    @task(10)  # Weight: 10 (will run 10 times for every 1 time other tasks run)
    def get_candidates(self):
        """List candidates with pagination"""
        page = random.randint(1, 50)
        limit = random.choice([10, 20, 50])
        
        self.client.get(
            f"/api/v1/candidates?page={page}&limit={limit}",
            headers=self.headers,
            name="/api/v1/candidates"
        )
    
    @task(8)  # Weight: 8
    def search_candidates(self):
        """Search candidates by skills"""
        skills = ["python", "javascript", "java", "golang", "rust"]
        payload = {
            "skills": random.sample(skills, k=random.randint(1, 3)),
            "experience_years_min": random.randint(1, 8),
            "limit": random.choice([10, 20])
        }
        
        self.client.post(
            "/api/v1/candidates/search",
            json=payload,
            headers=self.headers,
            name="/api/v1/candidates/search"
        )
    
    @task(6)  # Weight: 6
    def get_candidate_detail(self):
        """Get detailed candidate information"""
        candidate_id = random.randint(1, 1000)
        
        self.client.get(
            f"/api/v1/candidates/{candidate_id}",
            headers=self.headers,
            name="/api/v1/candidates/{id}"
        )
    
    @task(8)  # Weight: 8
    def get_matching_results(self):
        """Find matching candidates for a job"""
        job_id = random.randint(1, 100)
        payload = {
            "job_id": job_id,
            "limit": random.choice([5, 10, 20])
        }
        
        self.client.post(
            "/api/v1/matching/search",
            json=payload,
            headers=self.headers,
            name="/api/v1/matching/search"
        )
    
    @task(4)  # Weight: 4
    def rate_match(self):
        """Rate a candidate-job match"""
        match_id = random.randint(1, 5000)
        rating = random.choice([1, 2, 3, 4, 5])
        
        self.client.post(
            f"/api/v1/matches/{match_id}/rate",
            json={"rating": rating},
            headers=self.headers,
            name="/api/v1/matches/{id}/rate"
        )
    
    @task(2)  # Weight: 2
    def create_candidate(self):
        """Create a new candidate"""
        timestamp = str(int(time.time()))
        payload = {
            "email": f"candidate_{timestamp}@example.com",
            "first_name": f"Test{timestamp}",
            "last_name": "Candidate",
            "phone": "+1234567890",
            "location": "San Francisco, CA",
            "skills": ["python", "javascript", "react"],
            "experience_years": random.randint(1, 15),
            "bio": "Professional software developer"
        }
        
        self.client.post(
            "/api/v1/candidates",
            json=payload,
            headers=self.headers,
            name="/api/v1/candidates [POST]"
        )
    
    @task(1)  # Weight: 1
    def health_check(self):
        """Check API health"""
        self.client.get("/health", name="/health")


# Event handlers for reporting
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("\n" + "="*60)
    print("Starting Load Test for MisMatch Recruiter")
    print("="*60)
    print(f"Start time: {datetime.now()}")
    print()


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("\n" + "="*60)
    print("Load Test Results")
    print("="*60)
    
    stats = environment.stats
    
    print(f"\nTotal requests: {stats.total.num_requests}")
    print(f"Total failures: {stats.total.num_failures}")
    print(f"Success rate: {((stats.total.num_requests - stats.total.num_failures) / stats.total.num_requests * 100):.2f}%")
    print(f"\nResponse Times (ms):")
    print(f"  Min: {stats.total.min_response_time:.2f}")
    print(f"  Max: {stats.total.max_response_time:.2f}")
    print(f"  Avg: {stats.total.avg_response_time:.2f}")
    print(f"  Median: {stats.total.median_response_time:.2f}")
    print(f"  P95: {stats.total.get_response_time_percentile(0.95):.2f}")
    print(f"  P99: {stats.total.get_response_time_percentile(0.99):.2f}")
    
    print(f"\nRequests per second: {stats.total.total_rps:.2f}")
    print(f"Test duration: {stats.total.get_total_response_time() / 1000 / stats.total.num_requests:.2f}s average per request")
    
    print(f"\nEndpoint Performance:")
    for name, stat in stats.entries.items():
        if stat.num_requests > 0:
            error_pct = stat.num_failures / stat.num_requests * 100 if stat.num_requests > 0 else 0
            print(f"  {name}")
            print(f"    Requests: {stat.num_requests} | Failures: {stat.num_failures} ({error_pct:.1f}%)")
            print(f"    Avg: {stat.avg_response_time:.2f}ms | P95: {stat.get_response_time_percentile(0.95):.2f}ms")
    
    print(f"\nEnd time: {datetime.now()}")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Run with: locust -f locustfile.py --host=http://localhost:5000
    pass
