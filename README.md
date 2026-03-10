# MisMatch - AI Recruiting Platform

**AI-powered resume-job matching for smart hiring decisions**

[![CI - Lint, Test & Coverage](https://github.com/maksimmishakov/mismatch-recruiter/actions/workflows/ci.yml/badge.svg)](https://github.com/maksimmishakov/mismatch-recruiter/actions/workflows/ci.yml)

> **Status:** Work in Progress (MVP / Beta)
> Backend: Flask + SQLAlchemy | Frontend: React (Vite) | DB: SQLite (dev) / PostgreSQL (prod) | Deploy: Amvera Cloud

---

## Current Status / Known Limitations

| Component | Status | Notes |
|-----------|--------|-------|
| **Backend (Flask app)** | ⚠️ Beta | `app/__init__.py` — factory pattern, 3 blueprints registered |
| **main.py** | ✅ Works | Standalone Flask app for legacy/Telegram flow |
| **wsgi.py** | ✅ Works | Entry point for Gunicorn / Amvera |
| **Frontend (React/Vite)** | ⚠️ Beta | Builds to `../static/`, proxy to backend :5000 |
| **Tests** | ⚠️ Partial | Multiple test files exist, coverage not measured yet |
| **CI/CD** | ⚠️ Partial | Only `security.yml` workflow; no lint/test pipeline yet |
| **Deployment (Amvera)** | ⚠️ Unstable | Latest deploy failed (see Deployments panel) |
| **IndentationError** | ❌ Known bug | Was in `app.py` (legacy) — see CRITICAL_ISSUES_REPORT.md |

**Real test coverage:** Unknown — run `make coverage` locally to get actual numbers.
**Uptime claim "99.9%":** Not verified — Amvera deployment is currently failing.

---

## Tech Stack

**Backend:**
- Python 3.11
- Flask 2.3+ (main framework)
- SQLAlchemy 3.0+ via Flask-SQLAlchemy
- SQLite (dev, default) / PostgreSQL (prod via `DATABASE_URL`)
- Gunicorn (WSGI server)
- PyJWT + bcrypt (auth)
- pdfplumber, python-docx (document parsing)
- scikit-learn (salary prediction ML)
- graphene + graphene-flask (GraphQL endpoint)

**Frontend:**
- React 18 + React Router 6
- Vite 5 (bundler, builds to `static/`)
- Axios
- Dev proxy: Vite proxies `/api` → `http://localhost:5000`

**Infrastructure:**
- Amvera Cloud (deployment, runs `gunicorn wsgi:app --bind=0.0.0.0:5000 --workers 4`)
- Docker (port 5000, entry `app:create_app()`)
- GitHub Actions (security scan only, no CI test pipeline yet)

---

## Quick Start (Local Development)

```bash
# 1. Clone
git clone https://github.com/maksimmishakov/mismatch-recruiter
cd mismatch-recruiter

# 2. Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and fill in env vars
cp .env.example .env
# Edit .env: set OPENAI_API_KEY, DATABASE_URL (optional, defaults to SQLite)

# Run backend
python wsgi.py  # or: make run
```

```bash
# 3. Frontend (separate terminal)
cd frontend
npm install
npm run dev  # runs on :3000, proxies /api to :5000
```

```bash
# 4. Build frontend into static/
cd frontend
npm run build  # outputs to ../static/
```


## Quick Demo (HR / Investors)

1. Open the live demo (if available): [https://mismatch-recruiter-maksimisakov.amvera.io/](https://mismatch-recruiter-maksimisakov.amvera.io/)  
2. Upload a sample resume (PDF) and select a target job description.  
3. Check:
   - Match score between candidate and job
   - Highlighted skill gaps / mismatches
   - Suggested follow-up actions (invite / reject / nurture)
4. Use `MISMATCH_DEMO_GUIDE.md` for a step-by-step scenario when presenting to HR teams or investors.
---

## API Endpoints (Implemented)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check (main.py) |
| POST | `/api/analyze-resume` | Upload PDF, extract + parse resume |
| GET/POST | `/graphql` | GraphQL API |
| * | `/api/candidates/*` | Candidates CRUD (Blueprint) |
| * | `/api/matches/*` | Match operations (Blueprint) |
| * | `/api/job-enrichment/*` | Job enrichment (Blueprint) |
| * | `/api/resume-parsing/*` | Resume parsing (Blueprint) |

> **Note:** Endpoints documented in `docs/API_DOCUMENTATION.md` (e.g. `/api/salary-prediction`, `/api/generate-interview-questions`, `/api/admin/dashboard-data`) are planned/partially implemented. Verify in code before relying on them.
> 
**For planned endpoints**, see the "Planned / Not Yet Implemented" section in `docs/API_DOCUMENTATION.md`.


---

## Testing

```bash
# Run tests
make test

**All automated checks (lint, tests, coverage) are executed in GitHub Actions.**

Local runs are optional; you can rely on the **CI - Lint, Test & Coverage** workflow as the single source of truth.



# Run with coverage report
make coverage

# Lint
make lint

# Format
make format
```

Test files in `tests/`:
- `test_api.py`, `test_api_endpoints.py` — API endpoint tests
- `test_analytics.py`, `test_analytics_extended.py` — analytics
- `test_matcher.py`, `test_matching_v2.py` — matching logic
- `test_job_enrichment.py` — job enrichment service
- `test_mismatch_api_client.py`, `test_mismatch_routes.py`, `test_mismatch_models.py` — integration model
- `test_full_integration.py`, `test_integration_complete.py` — E2E
- `tests/integration/` — integration test suite

---

## Environment Variables

See `.env.example`. Required vars:

```env
OPENAI_API_KEY=sk-your-key-here   # For GPT-4o-mini interview questions
LLM_MODEL=gpt-4o-mini
BACKEND_PORT=8000
DATABASE_URL=                     # Optional: postgres://... (defaults to SQLite)
YANDEX_API_KEY=                   # Optional: YandexGPT integration
TELEGRAM_BOT_TOKEN=               # Optional: Telegram notifications
SECRET_KEY=                       # Flask secret key
```

---

## Docker

```bash
docker build -t mismatch .
docker run -p 5000:5000 --env-file .env mismatch
```

Dockerfile uses `gunicorn app:create_app() --bind 0.0.0.0:5000 -w 4`.

> **Port alignment:** Dockerfile EXPOSE 5000, amvera.yaml containerPort 5000, .env.example BACKEND_PORT=8000. Use `PORT` env var if needed — `main.py` reads `os.getenv('PORT', 5000)`.

---

## Deployment (Amvera)

Amvera config (`amvera.yaml`):
- Python 3.11
- Install: `requirements.txt`
- Run: `gunicorn wsgi:app --bind=0.0.0.0:5000 --workers 4`
- Volume: `/data` (1Gb)

See `AMVERA_DEPLOYMENT_GUIDE.md` for full deployment steps.

---

## Project Structure

```
mismatch-recruiter/
├── app/                    # Flask application package
│   ├── __init__.py         # create_app() factory
│   ├── config/             # Settings (MismatchSettings via pydantic)
│   ├── models/             # SQLAlchemy models
│   ├── routes/             # Blueprints: candidates, matches, job_enrichment, resume_parsing
│   ├── services/           # Business logic
│   ├── ml/                 # ML models (salary prediction)
│   ├── graphql/            # GraphQL schema
│   ├── middleware/         # Auth, rate limiting
│   └── tasks/              # Background tasks
├── frontend/               # React/Vite SPA
│   └── src/                # React components
├── static/                 # Built frontend assets (Vite output)
├── templates/              # Jinja2 templates (fallback)
├── tests/                  # pytest test suite
├── alembic/                # DB migrations
├── services/               # Top-level service modules
├── utils/                  # Utilities
├── docs/                   # API docs, deployment guides
├── main.py                 # Standalone Flask app (Telegram + PDF)
├── wsgi.py                 # WSGI entry point
├── Makefile                # Developer commands
├── Dockerfile              # Container build
├── amvera.yaml             # Amvera deployment config
└── requirements.txt        # Python dependencies
```

---

## Known Technical Debt

- `requirements.txt` has duplicates (`gunicorn` appears twice, `redis` with both `>=` and `==`)
- `.env.example` only has 3 vars — needs expanding to cover all used env vars
- No CI pipeline for lint/tests yet (only security scan workflow)
- `app/__init__.py` registers only 3 blueprints but `routes/__init__.py` exports 4 (missing `resume_parsing_bp` registration)
- README previously claimed "90%+ test coverage" — this is unverified; run `make coverage` to get real numbers
- Amvera deployment currently failing (see Deployments panel on GitHub)

---

## License

MIT License — see LICENSE file for details.

---

## Contact

- **GitHub:** [@maksimmishakov](https://github.com/maksimmishakov)
- **Live Demo:** [Mismatch-recruiter-maksimisakov.amvera.io](https://Mismatch-recruiter-maksimisakov.amvera.io) (may be unavailable)


---

## Using GitHub Copilot Workspace

Copilot Workspace — это встроенный в GitHub инструмент для AI-assisted разработки прямо в браузере.

Подробное руководство по работе с Copilot Workspace для этого репозитория находится здесь:

**[docs/copilot-workspace.md](docs/copilot-workspace.md)**

Краткое содержание руководства:
- Как открыть Workspace через репозиторий или issue
- Первичная настройка сессии (спецификация, план, реализация)
- Как зафиксировать изменения через Pull Request
