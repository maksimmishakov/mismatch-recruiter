# Contributing to MisMatch Recruiter

Thank you for your interest in contributing!

## Local Development Setup

1. Fork this repository and clone your fork.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
make install-dev
pip install -r requirements.txt
```

4. Copy env vars:

```bash
cp .env.example .env
# fill in at least OPENAI_API_KEY and SECRET_KEY
```

5. Run backend:

```bash
python wsgi.py
# or
make run
```

6. (Optional) Run frontend:

```bash
cd frontend
npm install
npm run dev
```

---

## Coding Guidelines

- Use Python 3.11+ and Flask as the primary web framework.
- Run `make lint` before pushing.
- Format code with black + isort (or run `make format`).

---

## Testing

All new features should come with tests when possible.

Run:

```bash
make test
make coverage
```

If coverage drops significantly, consider adding more tests.

---

## Pull Requests

- Use clear titles (e.g. `feat: add salary prediction endpoint`).
- Reference related Issues in the description.
- CI (lint + tests + Docker build) must pass before merge.

---

## Automation Playbook

See `AGENT_TASKS.md` for a detailed automation script used by AI agents (Perplexity/Comet).

When you complete tasks from AGENT_TASKS, update that file with dates and status.
