import os
import json

# Create necessary directories
os.makedirs('.github/workflows', exist_ok=True)
os.makedirs('backend/migrations/versions', exist_ok=True)
os.makedirs('docker', exist_ok=True)

# Create docker compose file
docker_compose = '''version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: mismatch_db
      POSTGRES_USER: mismatch
      POSTGRES_PASSWORD: mismatch123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://mismatch:mismatch123@postgres:5432/mismatch_db
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app

volumes:
  postgres_data:
  redis_data:
'''

with open('docker-compose.yml', 'w') as f:
    f.write(docker_compose)
print('Created docker-compose.yml')

# Create .dockerignore
dockerignore = '''__pycache__
*.pyc
.git
.gitignore
.env
*.log
node_modules
.pytest_cache
.coverage
'''

with open('.dockerignore', 'w') as f:
    f.write(dockerignore)
print('Created .dockerignore')

# Create backend Dockerfile
backend_dockerfile = '''FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:create_app()"]
'''

with open('backend/Dockerfile', 'w') as f:
    f.write(backend_dockerfile)
print('Created backend/Dockerfile')

# Create amvera.yml
amvera_yml = '''project: mismatch-recruiter

env:
  - name: DATABASE_URL
    value: postgresql://user:pass@db:5432/mismatch_db
  - name: REDIS_URL
    value: redis://redis:6379/0
  - name: FLASK_ENV
    value: production

services:
  - name: backend
    image: mismatch-recruiter:backend
    port: 5000
    healthcheck:
      path: /health
      timeout: 10
    autoscaling:
      minInstances: 1
      maxInstances: 3
'''

with open('amvera.yml', 'w') as f:
    f.write(amvera_yml)
print('Created amvera.yml')

# Create locustfile
locustfile = '''from locust import HttpUser, task, between

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
'''

with open('backend/locustfile.py', 'w') as f:
    f.write(locustfile)
print('Created backend/locustfile.py')

print('\\n✓ All CI/CD configuration files created successfully!')
