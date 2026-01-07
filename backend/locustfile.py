from locust import HttpUser, task, between

class MismatchUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def view_candidates(self):
        self.client.get("/api/candidates")

    @task(2)
    def search_jobs(self):
        self.client.get("/api/jobs?query=python")

    @task(1)
    def get_matches(self):
        self.client.post("/api/matches", json={"user_id": 1})
