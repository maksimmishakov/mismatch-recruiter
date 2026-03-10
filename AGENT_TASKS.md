# AGENT_TASKS.md - Perplexity Agent Automation Script

> **Purpose:** Actionable task list for Perplexity/Comet agent + computer tool to audit, fix, test and stabilize MisMatch Recruiter.

---

## ✅ COMPLETED (March 10, 2026)

### Task 1: Repo Audit
- ✅ Read `CRITICAL_ISSUES_REPORT.md`, `FINAL_STATUS.md`, `README.md`
- ✅ Listed all critical issues (IndentationError, port misalignment, missing blueprint registration)
- ✅ Compared README claims ("90%+ test coverage", "99.9% uptime") with actual state

### Task 2: Update README with honest status
- ✅ Created new README.md with accurate "Current Status / Known Limitations" table
- ✅ Removed inflated metrics, added real tech stack (Flask, React, SQLite/Postgres, Vite)
- ✅ Added "Known Technical Debt" section

### Task 3: Fix app/__init__.py
- ✅ Registered `resume_parsing_bp` blueprint (was exported but not registered)
- ✅ Fixed indentation issues
- ✅ Added `SECRET_KEY` config with sensible default

### Task 4: Build System Improvements
- ✅ **Makefile:** Added `coverage`, `install-dev`, `lint`, `format` targets
- ✅ **requirements-dev.txt:** Created with pytest-cov, flake8, black, isort, bandit, safety
- ✅ **.env.example:** Expanded to 65 lines with all env vars (JWT, Telegram, Redis, MisMatch API)

### Task 5: CI/CD Pipeline
- ✅ Created `.github/workflows/ci.yml` with:
  - Lint (flake8, black --check)
  - Test + coverage (pytest with htmlcov upload)
  - Docker build + smoke test on master branch

---

## 🔄 NEXT STEPS (For You or Future Agent)

### Task 6: Sync requirements.txt

- ✅ Removed duplicates (`gunicorn` appears twice, `redis>=5.0.0` and `redis==5.0.1`)
- ✅ Unified stack: kept Flask app (main.py + app/__init__.py), removed FastAPI-related deps from requirements.txt
- ✅ Decision: **Flask** is the primary web framework for this repo
### Task 7: Run Tests Locally
```bash
make install-dev
make test
make coverage
```
- [ ] Fix failing tests (check CRITICAL_ISSUES_REPORT.md for IndentationError references)
- [ ] Update `TESTING_GUIDE.md` with actual coverage percentage
- [ ] Add coverage badge to README

### Task 8: API Consistency Check
- [ ] Compare `docs/API_DOCUMENTATION.md` endpoints with `app/routes/__init__.py` exports
- [ ] Verify:
  - `/api/salary-prediction` exists?
  - `/api/generate-interview-questions` exists?
  - `/api/admin/dashboard-data` exists?
- [ ] Update docs or add TODO comments in code

### Task 9: Frontend Sanity Check
- [ ] `cd frontend && npm install && npm run dev`
- [ ] Check that API calls in `frontend/src/*` match actual backend routes
- [ ] Verify Vite proxy config: does it proxy `/api` to `localhost:5000`?
- [ ] Run `npm run build` and check that output goes to `../static/`

### Task 10: Deployment Alignment
- [ ] Verify `Dockerfile`, `amvera.yaml`, `Procfile` all use same command: `gunicorn wsgi:app --bind=0.0.0.0:5000 --workers 4`
- [ ] Check PORT env var: Dockerfile EXPOSE 5000, .env.example has BACKEND_PORT=8000 — pick one!
- [ ] Test Docker image locally:
```bash
docker build -t mismatch-test .
docker run -p 5000:5000 --env-file .env mismatch-test
curl http://localhost:5000/health
```

---

## 🎯 Agent Execution Format (Perplexity + computer tool)

When running agent tasks, use this format:

### Example: Task 6
```markdown
**Agent:** read requirements.txt
**Computer:** file_read('requirements.txt')
**Agent:** found duplicates: gunicorn==21.2.0 at line 15, gunicorn>=21.2.0 at line 50
**Agent:** create cleaned requirements.txt
**Computer:** file_write('requirements.txt', cleaned_content)
```

---

## 📚 Reference Docs

- `CRITICAL_ISSUES_REPORT.md` — blocker bugs (IndentationError on line 713, GitHub Actions billing)
- `FINAL_STATUS.md`, `PRODUCTION_STATUS.md`, `DEPLOYMENT_STATUS_FINAL.md` — deployment state
- `TESTING_GUIDE.md`, `PHASE2_IMPLEMENTATION.md` — test coverage info
- `API_DOCUMENTATION.md`, `API_ANALYTICS_ENDPOINTS.md`, `ANALYTICS_API_DOCUMENTATION.md` — API specs
- `AMVERA_DEPLOYMENT_GUIDE.md`, `DEPLOYMENT.md`, `PHASE_4_DEPLOYMENT_GUIDE.md` — deploy instructions

---

**Version:** v1.0 (Mar 10, 2026)
**Author:** Comet AI (via Perplexity)
