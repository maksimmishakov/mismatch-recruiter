# 🔍 MisMatch System Diagnostics & Error Checking Guide

## 📋 TABLE OF CONTENTS
1. [Environment Check](#environment-check)
2. [Dependencies Verification](#dependencies-verification)
3. [Flask Backend Testing](#flask-backend-testing)
4. [Database Connection Tests](#database-connection-tests)
5. [Docker & Container Checks](#docker--container-checks)
6. [Port & Network Diagnostics](#port--network-diagnostics)
7. [Logs Analysis](#logs-analysis)
8. [Performance Metrics](#performance-metrics)
9. [Security Audit](#security-audit)
10. [Final Checklist](#final-checklist)

---

## 1️⃣ ENVIRONMENT CHECK

### Step 1.1: Verify Python Installation
```bash
# Check Python version (need 3.9+)
python --version
python3 --version

# Expected output: Python 3.9.x, 3.10.x, 3.11.x, or 3.12.x
# ✅ If you see 3.9+: PASS
# ❌ If below 3.9: FAIL - Install newer Python
```

### Step 1.2: Check Virtual Environment
```bash
# Mac/Linux
which python
# Should show: /path/to/venv/bin/python

# Windows PowerShell
Get-Command python
# Should show path with \venv\Scripts\

# If NOT in venv:
source venv/bin/activate  # Mac/Linux
.\venv\Scripts\Activate.ps1  # Windows
```

**Check:** Prompt should show `(venv)` at the beginning
```
✅ (venv) C:\Users\maksimmishakov\mismatch-recruiter>
❌ C:\Users\maksimmishakov\mismatch-recruiter>  (no venv)
```

### Step 1.3: Verify Working Directory
```bash
pwd  # Mac/Linux
cd   # Windows - shows current path

# Should be: /Users/.../mismatch-recruiter or C:\...\mismatch-recruiter
# Check if you have these files:
ls -la
# Expected to see:
# - app.py
# - requirements.txt
# - .git/
# - docker-compose.yml
# - app/ (folder)
```

---

## 2️⃣ DEPENDENCIES VERIFICATION

### Step 2.1: Check pip
```bash
pip --version
# Expected: pip 20.x or higher

# Update pip if needed
pip install --upgrade pip
```

### Step 2.2: Install Requirements
```bash
pip install -r requirements.txt

# Expected output:
# Successfully installed Flask-2.3.0
# Successfully installed Flask-CORS-4.0.0
# Successfully installed psycopg2-binary-2.9.0
# ... (no errors)
```

### Step 2.3: Verify Each Dependency
```bash
# Test imports
python -c "import flask; print(f'Flask: {flask.__version__}')"
# Expected: Flask: 2.3.0

python -c "import flask_cors; print('Flask-CORS: OK')"
python -c "import psycopg2; print('psycopg2: OK')"

# All should print OK without errors
```

**If any fail:**
```bash
# Show detailed error
pip install Flask==2.3.0 -v

# Check what's conflicting
pip check

# Nuclear option (clean install)
rm -rf venv/
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3️⃣ FLASK BACKEND TESTING

### Step 3.1: Start Flask Server
```bash
# Activate venv first
source venv/bin/activate  # Mac/Linux
.\venv\Scripts\Activate.ps1  # Windows

# Start Flask
python app.py

# Expected output:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
# WARNING in werkzeug: This is a development server...
```

### Step 3.2: Test Health Endpoint (New Terminal)
```bash
# While Flask is running, open NEW terminal window
# DON'T close the Flask terminal!

# Mac/Linux/Windows
curl http://localhost:5000/health

# Expected response:
# {
#   "status": "ok",
#   "service": "mismatch-recruiter",
#   "timestamp": "2026-01-03T15:35:00"
# }
```

**If CURL not available, use Python:**
```bash
python -c "
import urllib.request
import json

try:
    response = urllib.request.urlopen('http://localhost:5000/health')
    data = json.loads(response.read().decode())
    print('✅ SUCCESS:', data)
except Exception as e:
    print('❌ ERROR:', str(e))
"
```

### Step 3.3: Test All Endpoints
```bash
# Create a test script: test_endpoints.py

cat > test_endpoints.py << 'EOF'
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

endpoints = [
    ("GET", "/health", "Health Check"),
    ("GET", "/api/status", "API Status"),
    ("GET", "/api/job-profiles", "Job Profiles"),
    ("GET", "/api/candidates", "Candidates"),
    ("GET", "/api/hiring-dna", "Hiring DNA"),
    ("POST", "/api/salary/optimize", "Salary Optimize"),
    ("GET", "/api/signals", "Signals"),
]

print("\n" + "="*60)
print("🔍 ENDPOINT DIAGNOSTICS", datetime.now().isoformat())
print("="*60 + "\n")

passed = 0
failed = 0

for method, path, name in endpoints:
    try:
        url = f"{BASE_URL}{path}"
        
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json={}, timeout=5)
        
        status = response.status_code
        
        if 200 <= status < 300:
            print(f"✅ {method:4} {path:30} [{status}] {name}")
            passed += 1
        else:
            print(f"⚠️  {method:4} {path:30} [{status}] {name}")
            failed += 1
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {method:4} {path:30} [FAIL] {name} - Connection refused")
        failed += 1
    except Exception as e:
        print(f"❌ {method:4} {path:30} [ERROR] {name} - {str(e)}")
        failed += 1

print("\n" + "="*60)
print(f"Results: {passed} passed, {failed} failed")
print("="*60 + "\n")

if failed == 0:
    print("🎉 ALL ENDPOINTS WORKING!")
else:
    print(f"⚠️  {failed} endpoint(s) need attention")
EOF

# Run the test
python test_endpoints.py
```

### Step 3.4: Check Flask Logs
```bash
# In Flask terminal, look for any ERROR or WARNING messages
# Should see:
# * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
# * Restarting with reloader
# * Debugger is active!

# If you see errors like:
# ❌ ModuleNotFoundError: No module named 'flask'
# → Run: pip install -r requirements.txt

# ❌ Address already in use
# → Another process using port 5000
# → See "Port & Network Diagnostics" below
```

---

## 4️⃣ DATABASE CONNECTION TESTS

### Step 4.1: Test PostgreSQL Connection (Optional)
```bash
# Check if PostgreSQL is installed
psql --version

# Try to connect (if you have PostgreSQL running)
psql -U postgres

# If it connects, you'll see: psql (15.x)#
# Type: \q to exit

# If NOT installed, that's OK for development
```

### Step 4.2: Test SQLAlchemy Configuration
```bash
# Create test_db.py
cat > test_db.py << 'EOF'
from app import app, db

with app.app_context():
    try:
        # Test database connection
        result = db.session.execute("SELECT 1")
        print("✅ Database connection: SUCCESS")
    except Exception as e:
        print(f"⚠️  Database connection: {type(e).__name__}")
        print(f"   Message: {str(e)}")
        print("   (This is OK if you don't have PostgreSQL running)")
    
    # Check SQLAlchemy version
    from sqlalchemy import __version__
    print(f"SQLAlchemy version: {__version__}")
EOF

python test_db.py
```

---

## 5️⃣ DOCKER & CONTAINER CHECKS

### Step 5.1: Verify Docker Installation
```bash
docker --version
# Expected: Docker version 20.x or higher

docker ps
# Expected: Shows list of running containers (might be empty)

docker images
# Expected: Shows list of available images
```

### Step 5.2: Test Docker Compose
```bash
# Check docker-compose version
docker-compose --version
# Expected: docker-compose version 1.29.x or higher

# Check if docker-compose.yml is valid
docker-compose config

# Should output entire YAML without errors
# If error: Check YAML syntax (indentation, colons, etc.)
```

### Step 5.3: Build Docker Image
```bash
# Build the image
docker build -t mismatch:dev .

# Expected output:
# Sending build context to Docker daemon
# Step 1/X : FROM python:3.11-slim
# ...
# Successfully tagged mismatch:dev

# Verify image was created
docker images | grep mismatch
# Should show: mismatch  dev  SIZE  DATE
```

### Step 5.4: Run Docker Container
```bash
# Run in foreground to see logs
docker run -p 5000:5000 mismatch:dev

# Expected output:
# * Running on http://0.0.0.0:5000

# In another terminal, test
curl http://localhost:5000/health

# Stop with Ctrl+C
```

---

## 6️⃣ PORT & NETWORK DIAGNOSTICS

### Step 6.1: Check Open Ports
```bash
# Mac/Linux
lsof -i :5000
# Shows what's using port 5000

netstat -tuln | grep 5000
# Shows if port is listening

# Windows PowerShell
netstat -ano | findstr :5000
# Shows process using port 5000
```

### Step 6.2: If Port 5000 is Already Used
```bash
# Mac/Linux - Kill process
lsof -ti:5000 | xargs kill -9

# Windows - Find and kill
netstat -ano | findstr :5000
# Note the PID (Process ID)
taskkill /PID <PID> /F

# Or use different port
python app.py --port 5001
# Then test: curl http://localhost:5001/health
```

### Step 6.3: Check Port Accessibility
```bash
# Test if port is open
nc -zv localhost 5000  # Mac/Linux
# Expected: Connection successful

# Windows (use PowerShell)
Test-NetConnection localhost -Port 5000
# Expected: TcpTestSucceeded : True
```

---

## 7️⃣ LOGS ANALYSIS

### Step 7.1: Enable Detailed Logging
```bash
# Add to app.py before app.run():
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Then run
python app.py

# Will show DEBUG messages
```

### Step 7.2: Check Flask Logs for Errors
```bash
# Create logging_test.py
cat > logging_test.py << 'EOF'
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('mismatch.log')
    ]
)

logger = logging.getLogger(__name__)

# Test logging levels
logger.debug("This is a DEBUG message")
logger.info("This is an INFO message")
logger.warning("This is a WARNING message")
logger.error("This is an ERROR message")

print("\n✅ Logs written to mismatch.log")
EOF

python logging_test.py

# Check the log file
cat mismatch.log
```

### Step 7.3: Common Log Patterns
```
✅ Good patterns:
  * Running on http://127.0.0.1:5000
  * GET /health 200
  * POST /api/candidates 201

❌ Bad patterns:
  * ModuleNotFoundError: No module named 'X'
  * Connection refused
  * Address already in use
  * TypeError: object is not callable
  * Traceback (most recent call last):
```

---

## 8️⃣ PERFORMANCE METRICS

### Step 8.1: Test Response Time
```bash
# Create performance_test.py
cat > performance_test.py << 'EOF'
import requests
import time

BASE_URL = "http://localhost:5000"

endpoints = [
    "/health",
    "/api/status",
    "/api/job-profiles",
    "/api/candidates",
]

print("\n" + "="*60)
print("⏱️  PERFORMANCE METRICS")
print("="*60 + "\n")

for endpoint in endpoints:
    times = []
    
    for i in range(5):
        start = time.time()
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            elapsed = (time.time() - start) * 1000  # Convert to ms
            times.append(elapsed)
            status = response.status_code
        except Exception as e:
            print(f"❌ {endpoint}: {str(e)}")
            break
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        # Determine speed
        if avg_time < 100:
            speed = "🚀 Excellent"
        elif avg_time < 500:
            speed = "✅ Good"
        elif avg_time < 1000:
            speed = "⚠️  Slow"
        else:
            speed = "❌ Very Slow"
        
        print(f"{endpoint:30} {speed:15} Avg: {avg_time:.1f}ms (Min: {min_time:.1f}ms, Max: {max_time:.1f}ms)")

print("\n" + "="*60)
print("Target: <100ms for /health, <500ms for API calls")
print("="*60 + "\n")
EOF

python performance_test.py
```

### Step 8.2: Monitor CPU & Memory
```bash
# Mac/Linux
top -p $(pgrep -f "python app.py")
# Shows CPU, Memory, Process info
# Press Q to quit

# Windows
tasklist /v | findstr python
# Shows running Python processes

# Better: Use resource module
cat > resource_monitor.py << 'EOF'
import psutil
import time

process = None
for p in psutil.process_iter(['pid', 'name']):
    if 'python' in p.info['name'] and 'app' in str(p.cmdline()):
        process = p
        break

if process:
    print(f"Process: {process.info['name']} (PID: {process.info['pid']})")
    
    # Monitor for 10 seconds
    for i in range(10):
        mem = process.memory_info().rss / 1024 / 1024  # MB
        cpu = process.cpu_percent(interval=1)
        print(f"Memory: {mem:.1f}MB, CPU: {cpu:.1f}%")
        time.sleep(1)
else:
    print("❌ Process not found. Start Flask first: python app.py")
EOF

pip install psutil
python resource_monitor.py
```

---

## 9️⃣ SECURITY AUDIT

### Step 9.1: Check for Common Vulnerabilities
```bash
# Install safety
pip install safety

# Check requirements for known vulnerabilities
safety check --json

# Expected output:
# ✅ No known security vulnerabilities found
```

### Step 9.2: Verify Environment Variables
```bash
# Check if sensitive data is in code
grep -r "password\|api_key\|secret" app/
# Should NOT find any hardcoded secrets

# Good approach: Use .env file
cat > .env << 'EOF'
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost:5432/mismatch_dev
JWT_SECRET=your-secret-key-here
EOF

# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore

# Never commit .env!
```

### Step 9.3: Check Debug Mode
```bash
# In app.py, ensure debug mode is OFF in production:

# ❌ WRONG for production:
app.run(debug=True)

# ✅ RIGHT:
app.run(debug=os.getenv('FLASK_ENV') == 'development')
```

---

## 🔟 FINAL CHECKLIST

Create `SYSTEM_CHECK.py`:

```python
#!/usr/bin/env python
"""
Comprehensive system check script for MisMatch
Run: python SYSTEM_CHECK.py
"""

import sys
import subprocess
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

checks_passed = 0
checks_failed = 0

def test(name, command, should_contain=None):
    """Run a test and check results"""
    global checks_passed, checks_failed
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            if should_contain and should_contain not in result.stdout:
                print(f"{Colors.RED}❌ {name}{Colors.END}")
                checks_failed += 1
                return False
            else:
                print(f"{Colors.GREEN}✅ {name}{Colors.END}")
                checks_passed += 1
                return True
        else:
            print(f"{Colors.RED}❌ {name}{Colors.END}")
            checks_failed += 1
            return False
    except Exception as e:
        print(f"{Colors.RED}❌ {name} - {str(e)}{Colors.END}")
        checks_failed += 1
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"🔍 MisMatch System Diagnostics")
    print(f"{'='*60}{Colors.END}\n")
    
    # Environment Checks
    print(f"{Colors.BLUE}📦 Environment Checks{Colors.END}")
    test("Python installed", "python --version")
    test("Pip installed", "pip --version")
    test("Git installed", "git --version")
    test("Virtual environment active", "python -c \"import sys; assert '/venv/' in sys.prefix or '\\\\venv\\\\' in sys.prefix\"")
    
    # Dependencies Checks
    print(f"\n{Colors.BLUE}📚 Dependencies Checks{Colors.END}")
    test("Flask installed", "python -c \"import flask; print(flask.__version__)\"")
    test("Flask-CORS installed", "python -c \"import flask_cors\"")
    test("SQLAlchemy installed", "python -c \"import sqlalchemy\"")
    test("Requests installed", "python -c \"import requests\"")
    
    # Flask Checks
    print(f"\n{Colors.BLUE}🚀 Flask Application Checks{Colors.END}")
    test("app.py exists", "test -f app.py")
    test("requirements.txt exists", "test -f requirements.txt")
    test("Flask app loads", "python -c \"from app import app; print('OK')\"")
    
    # Docker Checks
    print(f"\n{Colors.BLUE}🐳 Docker Checks{Colors.END}")
    test("Docker installed", "docker --version")
    test("Docker Compose installed", "docker-compose --version")
    test("Dockerfile exists", "test -f Dockerfile")
    test("docker-compose.yml exists", "test -f docker-compose.yml")
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"📊 Summary{Colors.END}")
    print(f"{Colors.GREEN}✅ Passed: {checks_passed}{Colors.END}")
    print(f"{Colors.RED}❌ Failed: {checks_failed}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    if checks_failed == 0:
        print(f"{Colors.GREEN}🎉 All checks passed! System is ready.{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}⚠️  {checks_failed} check(s) failed. See above for details.{Colors.END}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

Run it:
```bash
python SYSTEM_CHECK.py
```

---

## 📊 QUICK DIAGNOSTIC COMMANDS

```bash
# All-in-one diagnostic
echo "=== Python ===" && python --version && \
echo "=== Flask ===" && python -c "import flask; print(f'Flask {flask.__version__}')" && \
echo "=== Docker ===" && docker --version && \
echo "=== Git ===" && git status && \
echo "=== Port 5000 ===" && (lsof -i :5000 || netstat -ano | findstr :5000) && \
echo "✅ All systems checked"
```

---

## 🆘 EMERGENCY TROUBLESHOOTING

If everything fails:

```bash
# Nuclear reset
rm -rf venv __pycache__ .pytest_cache
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

---

**Created:** 2026-01-03  
**Status:** Complete Diagnostic Suite  
**Next:** Run `python SYSTEM_CHECK.py` for automated diagnostics
