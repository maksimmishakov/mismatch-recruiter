# LAMODA Recruiter - Pre-Demo Checklist
## January 15, 2026 at 14:00 MSK

### 🔍 System Verification (Run Day Before)

- [ ] **API Health Check**
  ```bash
  curl http://localhost:5000/api/health
  # Expected: {"status": "healthy", "message": "LAMODA Recruiter API is running"}
  ```

- [ ] **Database Connectivity**
  ```bash
  python -c "from app import db; print('✅ Database OK')"
  ```

- [ ] **Models Loaded**
  ```bash
  python -c "from app.models import User, Candidate, Job, Match; print('✅ All models loaded')"
  ```

- [ ] **Routes Registered**
  ```bash
  python -c "from app import create_app; app = create_app(); print(f'✅ {len([r for r in app.url_map.iter_rules() if "api" in r.rule])} API endpoints registered')"
  ```

- [ ] **Test Data Loaded**
  ```bash
  curl http://localhost:5000/api/candidates
  # Should return: [{"id": 1, ...}, ...]
  ```

- [ ] **Git Status Clean**
  ```bash
  git status
  # Should show: "On branch main, nothing to commit"
  ```

### 🎬 Demo Preparation

- [ ] **Demo Script Executable**
  ```bash
  ls -la DEMO_SCRIPT.sh
  # Should be: -rwxr-xr-x (executable)
  ```

- [ ] **Test Run Demo**
  ```bash
  ./DEMO_SCRIPT.sh
  # All 6 steps should complete successfully
  ```

- [ ] **Documentation Ready**
  - [ ] PRODUCTION_READY_REPORT.md
  - [ ] FINAL_SUMMARY.txt
  - [ ] QUICKSTART.md
  - [ ] API_DOCUMENTATION.md

- [ ] **Create Additional Test Data**
  ```bash
  # Create 2-3 more candidates and jobs for demo variety
  curl -X POST http://localhost:5000/api/candidates -H 'Content-Type: application/json' -d '{...}'
  ```

### 🖥️  Environment Setup

- [ ] **Development Environment**
  - [ ] Python 3.12+ installed
  - [ ] All dependencies in requirements.txt installed
  - [ ] .env file configured
  - [ ] Database initialized

- [ ] **Docker Environment (Alternative)**
  - [ ] Docker & Docker Compose installed
  - [ ] All services can start: `docker-compose up -d`
  - [ ] Services health: `docker-compose ps`

- [ ] **Network Configuration**
  - [ ] Port 5000 available for API
  - [ ] Port 80 available for Nginx
  - [ ] Port 3000 available for Frontend (if deploying)

### 🔐 Security Check

- [ ] **No Hardcoded Secrets**
  ```bash
  grep -r "password\|secret\|key" app/ --include="*.py" | grep -v test
  # Should return: only references to os.environ
  ```

- [ ] **Environment Variables Set**
  ```bash
  echo $SECRET_KEY $DATABASE_URL
  # Should show values (not empty)
  ```

- [ ] **.gitignore Configured**
  - [ ] node_modules is ignored
  - [ ] .env is ignored
  - [ ] __pycache__ is ignored
  - [ ] *.db is ignored

### 📊 Data Preparation

- [ ] **Sample Data Created**
  - [ ] 5+ candidates with diverse skills
  - [ ] 5+ job postings with various requirements
  - [ ] 5+ matches showing good/bad matches

- [ ] **Demo Scenarios Prepared**
  1. Show API health check
  2. Create new candidate in real-time
  3. Create new job posting in real-time
  4. Create match and show match score
  5. List and filter candidates
  6. List and filter jobs

### 📱 Hardware/Software Ready

- [ ] **Laptop/Computer**
  - [ ] 8GB+ RAM available
  - [ ] 10GB+ free disk space
  - [ ] Battery: 50%+ or plugged in
  - [ ] WiFi/Network working

- [ ] **Display**
  - [ ] External monitor ready (1080p+)
  - [ ] HDMI/USB-C adapter available
  - [ ] Screen sharing tested

- [ ] **Browser**
  - [ ] Chrome/Firefox open and ready
  - [ ] Localhost:5000 bookmarked
  - [ ] API Testing tool ready (Postman/curl)

### 📝 Presentation Materials

- [ ] **Slides Prepared**
  - [ ] Introduction (1 min)
  - [ ] System Architecture (2 min)
  - [ ] Live Demo (15 min)
  - [ ] Results & Future Plans (2 min)

- [ ] **Talking Points**
  - [ ] Explain the problem we solved (10 critical issues)
  - [ ] Show the solution architecture
  - [ ] Demonstrate key features
  - [ ] Discuss performance metrics
  - [ ] Show security measures

- [ ] **Backup Plans**
  - [ ] Have pre-recorded demo video
  - [ ] Have screenshots of all endpoints
  - [ ] Have API response examples written down

### 🚀 Deployment Ready

- [ ] **Production Checklist**
  - [ ] Docker images build successfully
  - [ ] docker-compose.yaml validated
  - [ ] All services start and respond
  - [ ] Database migrations ready
  - [ ] Backup strategy documented

- [ ] **Monitoring & Logging**
  - [ ] Logs directory created: `logs/`
  - [ ] Log rotation configured
  - [ ] Error tracking ready

### ✅ Final Checks

- [ ] **Code Quality**
  ```bash
  python -m py_compile app/*.py app/**/*.py
  # Should compile without errors
  ```

- [ ] **No Warnings or Errors**
  ```bash
  python -m pylint app/ --disable=all --enable=E
  # Should show: no errors
  ```

- [ ] **Git Commits**
  ```bash
  git log --oneline | head -5
  # All commits should have meaningful messages
  ```

- [ ] **Documentation Complete**
  ```bash
  ls -la *.md *.txt *.sh
  # Should show all documentation files
  ```

### 🎯 Day-of Demo

**Morning (2-3 hours before demo):**
- [ ] Start API: `python -m flask --app app run`
- [ ] Test all endpoints with DEMO_SCRIPT.sh
- [ ] Verify all test data is present
- [ ] Have backup terminal open
- [ ] Have logs open in another window

**30 minutes before:**
- [ ] Do one final health check
- [ ] Close unnecessary applications (reduce RAM usage)
- [ ] Have water nearby
- [ ] Mute notifications
- [ ] Charge all devices 100%

**Just before presentation:**
- [ ] Do final connectivity test
- [ ] Show system architecture slide
- [ ] Start demo from clean state
- [ ] Have phone number of technical support ready

### 🎉 Success Criteria

- [ ] API responds to all 6 test endpoints
- [ ] Demo runs smoothly without errors
- [ ] All CRUD operations work (Create, Read, Update, Delete)
- [ ] Data persists correctly
- [ ] Response times are < 500ms
- [ ] No security issues or warnings
- [ ] Team understands the system fully

---

## Notes

**API Endpoints to Test:**
1. GET /api/health - ✅ Should return 200 OK
2. GET /api/candidates - ✅ Should return list
3. POST /api/candidates - ✅ Should create and return 201
4. GET /api/jobs - ✅ Should return list
5. POST /api/jobs - ✅ Should create and return 201
6. GET /api/matches - ✅ Should return list
7. POST /api/matches - ✅ Should create and return 201

**Key Files to Have Ready:**
- [ ] app/__init__.py (Flask app)
- [ ] app/models/*.py (Database models)
- [ ] app/routes/__init__.py (API endpoints)
- [ ] wsgi.py (Production entry point)
- [ ] docker-compose.yaml (Deployment)
- [ ] DEMO_SCRIPT.sh (Automated demo)
- [ ] QUICKSTART.md (Quick reference)

**Emergency Contacts:**
- [ ] Team lead phone: ____________
- [ ] Technical support: ____________
- [ ] LAMODA contact: ____________

---

✅ **Status:** Ready for January 15, 2026 Demo  
📅 **Created:** January 12, 2026  
🎯 **Target:** 100% Success Rate
