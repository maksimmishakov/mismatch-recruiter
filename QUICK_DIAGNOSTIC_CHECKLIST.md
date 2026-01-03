# ✅ MisMatch Quick Diagnostic Checklist

**Last Updated:** 2026-01-03  
**Status:** 🔍 System Check Required  
**Time to Complete:** ~15 minutes

---

## 🚀 PHASE 1: QUICK START (2 min)

### ☑️ Check 1: You Have Everything
```
☐ Open VS Code
☐ Terminal is open (Ctrl + `)
☐ You're in /mismatch-recruiter folder
☐ You can see app.py in the folder
```

**What to do:**
```bash
ls -la
# Should show:
# app.py
# requirements.txt
# .git/
# app/
```

**Status:** ✅ / ⚠️ / ❌

---

## 📦 PHASE 2: PYTHON ENVIRONMENT (3 min)

### ☑️ Check 2: Python Version
```bash
python --version
```
**Expected:** `Python 3.9.x` or higher  
**Status:** ✅ / ⚠️ / ❌

**If ❌:** Download Python 3.11 from python.org

---

### ☑️ Check 3: Virtual Environment
```bash
# Activate it
source venv/bin/activate  # Mac/Linux
# or
.\venv\Scripts\Activate.ps1  # Windows
```

**Look for:** `(venv)` at the start of your terminal line  
**Status:** ✅ / ⚠️ / ❌

**If ❌:** Run this:
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
```

---

### ☑️ Check 4: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected:** No error messages, all packages installed successfully  
**Status:** ✅ / ⚠️ / ❌

**If slow or fails:** Run these:
```bash
pip install --upgrade pip
pip install Flask==2.3.0 Flask-CORS==4.0.0 psycopg2-binary==2.9.0
```

---

## 🚀 PHASE 3: FLASK STARTUP (2 min)

### ☑️ Check 5: Start Flask Server
```bash
python app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**Status:** ✅ / ⚠️ / ❌

**If ❌ "Address already in use":**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :5000   # Windows (then taskkill)

# Try again
python app.py
```

**If ❌ "ModuleNotFoundError":**
```bash
# Virtual environment issue
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔏 PHASE 4: API TESTING (3 min)

### ☑️ Check 6: Test Health Endpoint

**Open NEW terminal (keep Flask running!)**

```bash
curl http://localhost:5000/health
```

**Expected:**
```json
{
  "status": "ok",
  "service": "mismatch-recruiter",
  "timestamp": "2026-01-03T15:35:00"
}
```

**Status:** ✅ / ⚠️ / ❌

**If ❌ "Connection refused":**
- Is Flask still running in first terminal?
- Check that you see `Running on http://127.0.0.1:5000`
- Try: `curl http://localhost:5000/` (without /health)

---

### ☑️ Check 7: Test All Main Endpoints

Copy-paste this into terminal:

```bash
echo "🐍 Testing endpoints..."; \
curl -s http://localhost:5000/health | python -m json.tool && echo "[✅ /health]" && \
curl -s http://localhost:5000/api/status | python -m json.tool && echo "[✅ /api/status]" && \
curl -s http://localhost:5000/api/job-profiles | python -m json.tool && echo "[✅ /api/job-profiles]" && \
curl -s http://localhost:5000/api/candidates | python -m json.tool && echo "[✅ /api/candidates]" && \
curl -s http://localhost:5000/api/hiring-dna | python -m json.tool && echo "[✅ /api/hiring-dna]" && \
curl -s http://localhost:5000/api/signals | python -m json.tool && echo "[✅ /api/signals]" && \
echo "✍️ Testing complete!"
```

**Status:**
- [ ] /health working
- [ ] /api/status working
- [ ] /api/job-profiles working
- [ ] /api/candidates working
- [ ] /api/hiring-dna working
- [ ] /api/signals working

**If ANY ❌:**
1. Check Flask terminal for errors
2. Look for red text or "Traceback"
3. Share the error message

---

## 🐳 PHASE 5: DOCKER VERIFICATION (Optional, 3 min)

### ☑️ Check 8: Docker Installed
```bash
docker --version
```

**Expected:** `Docker version 20.x` or higher  
**Status:** ✅ / ⚠️ / ❌

**If ❌:** Download Docker Desktop from docker.com

---

### ☑️ Check 9: Build Docker Image
```bash
docker build -t mismatch:dev .
```

**Expected:** Successfully tagged mismatch:dev  
**Status:** ✅ / ⚠️ / ❌

---

### ☑️ Check 10: Run Docker Container
```bash
docker run -p 5000:5000 mismatch:dev
```

**Expected:**
```
 * Running on http://0.0.0.0:5000
```

**Status:** ✅ / ⚠️ / ❌

**Test in another terminal:**
```bash
curl http://localhost:5000/health
```

---

## 🔂 PHASE 6: GIT & VERSION CONTROL (2 min)

### ☑️ Check 11: Git Status
```bash
git status
```

**Expected:**
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**Status:** ✅ / ⚠️ / ❌

**If you have changes:**
```bash
git add .
git commit -m "fix: system diagnostic checks"
git push
```

---

### ☑️ Check 12: Recent Commits
```bash
git log --oneline -5
```

**Expected:** Shows your recent commits  
**Status:** ✅ / ⚠️ / ❌

---

## 📊 PHASE 7: LOGS ANALYSIS (2 min)

### ☑️ Check 13: Flask Logs (from Flask terminal)

Look for these patterns:

✅ **Good signs:**
```
 * Running on http://127.0.0.1:5000
 * Restarting with reloader
 * Debugger is active!
 GET /health 200
 POST /api/candidates 201
```

❌ **Bad signs:**
```
ModuleNotFoundError: No module named 'flask'
Address already in use
Connection refused
Traceback (most recent call last):
```

**Action:** If bad signs, go back to Phase 2

---

### ☑️ Check 14: Python Errors

Create test file:

```bash
cat > quick_test.py << 'EOF'
import sys
print(f"Python: {sys.version}")
print(f"Executable: {sys.executable}")

try:
    import flask
    print(f"Flask: {flask.__version__} ✅")
except:
    print("Flask: ❌ NOT INSTALLED")

try:
    from app import app
    print("App load: ✅")
except Exception as e:
    print(f"App load: ❌ {str(e)}")

print("\nDone!")
EOF

python quick_test.py
```

**Status:** ✅ / ⚠️ / ❌

---

## 📊 PHASE 8: PERFORMANCE CHECK (2 min)

### ☑️ Check 15: Response Speed

```bash
cat > speed_test.py << 'EOF'
import requests
import time

for i in range(3):
    start = time.time()
    response = requests.get('http://localhost:5000/health')
    elapsed = (time.time() - start) * 1000
    print(f"Request {i+1}: {elapsed:.1f}ms [{response.status_code}]")
EOF

python speed_test.py
```

**Expected:** All requests <100ms  
**Status:** ✅ / ⚠️ / ❌

**If slow:**
- Check CPU usage: `top` (Mac/Linux)
- Check if Flask is the only process running

---

## 📊 FINAL SUMMARY

Count your checkmarks:

```
Phase 1 (Quick Start):      ___ / 4
Phase 2 (Python):           ___ / 3
Phase 3 (Flask):            ___ / 2
Phase 4 (API Testing):      ___ / 2
Phase 5 (Docker):           ___ / 3 (optional)
Phase 6 (Git):              ___ / 2
Phase 7 (Logs):             ___ / 2
Phase 8 (Performance):      ___ / 1

TOTAL:                      ___ / 19 ✅
```

---

## 📚 DIAGNOSIS MATRIX

### All checks passed (19/19) ✅
```
🎉 SYSTEM READY FOR PRODUCTION
✅ All endpoints working
✅ Performance acceptable
✅ No errors in logs
✅ Ready for Lamoda integration
```

**Next:** Proceed to Phase 2 features (see SYSTEM_DIAGNOSTICS.md)

---

### Most checks passed (15-18/19) ⚠️
```
🚀 SYSTEM MOSTLY WORKING
⚠️ Some components need attention
⚠️ But core functionality is fine
```

**Action:**
1. Identify which checks failed
2. Look at Phase description
3. Run suggested fixes
4. Re-test

---

### Many checks failed (<15/19) ❌
```
🚪 SYSTEM NEEDS ATTENTION
❌ Multiple critical issues
❌ Start from Phase 1 again
```

**Emergency fix:**
```bash
# Complete reset
rm -rf venv __pycache__
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

---

## 📧 DIAGNOSTIC REPORT TEMPLATE

When reporting issues, include:

```
## System Info
- OS: [Windows/Mac/Linux]
- Python: [version]
- Docker: [version or N/A]

## Failed Checks
- Check #X: [description]
- Check #Y: [description]

## Error Messages
```
[paste full error here]
```

## Steps Attempted
1. ...
2. ...
3. ...

## Current Status
- Endpoints working: Y/N
- Flask running: Y/N
- Port 5000 available: Y/N
```

---

## 🏗️ MAINTENANCE CHECKLIST

Do these weekly:

```
☐ Run SYSTEM_CHECK.py (see SYSTEM_DIAGNOSTICS.md)
☐ Check Flask logs for errors
☐ Test all 6 main endpoints
☐ Monitor response times (target: <100ms)
☐ Check Docker images are up to date
☐ Review git commits
```

---

## 📄 USEFUL COMMANDS REFERENCE

```bash
# Activate environment
source venv/bin/activate

# Start Flask
python app.py

# Test endpoint
curl http://localhost:5000/health

# Check running processes
lsof -i :5000

# Kill process
lsof -ti:5000 | xargs kill -9

# Full system check
python SYSTEM_CHECK.py

# View Flask logs
tail -f mismatch.log

# Restart Docker
docker restart mismatch:dev
```

---

**Created:** 2026-01-03  
**Last Updated:** 2026-01-03  
**Status:** Complete Diagnostic Suite Ready  

✅ **You have everything needed to diagnose any issue!**
