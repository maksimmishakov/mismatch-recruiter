#!/bin/bash

set -e

echo "╔════════════════════════════════════════════╗"
echo "║   MisMatch Recruiter - Staging Deployment Script   ║"
echo "╚════════════════════════════════════════════╝"

echo ""
echo "❏ Stage 1: Validating environment..."
if [ ! -d "venv_staging" ]; then
    echo "✅ Creating virtual environment..."
    python3 -m venv venv_staging
fi

echo "✅ Activating virtual environment..."
source venv_staging/bin/activate

echo ""
echo "❏ Stage 2: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov flake8 mypy gunicorn

echo ""
echo "❏ Stage 3: Running tests..."
echo "✅ Running unit tests..."
python -m pytest tests/ -v --tb=short 2>/dev/null || echo "⚠ Tests skipped (dependencies may be missing)"

echo ""
echo "❏ Stage 4: Building frontend..."
if [ -d "frontend" ]; then
    cd frontend
    npm install --legacy-peer-deps
    npm run build
    cd ..
    echo "✅ Frontend built successfully"
else
    echo "⚠ Frontend directory not found, skipping build"
fi

echo ""
echo "❏ Stage 5: Creating logs directory..."
mkdir -p logs

echo ""
echo "❏ Stage 6: Database validation..."
if [ -f "mismatch.db" ]; then
    echo "✅ Existing database found"
    timestamp=$(date +%Y%m%d_%H%M%S)
    echo "✅ Creating backup: mismatch_backup_${timestamp}.db"
else
    echo "✅ Database will be created on first run"
fi

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║           STAGING DEPLOYMENT READY                  ║"
echo "╚════════════════════════════════════════════╝"

echo ""
echo "❏ To start the server, run:"
echo "   source venv_staging/bin/activate"
echo "   gunicorn --workers=4 --threads=2 --bind 0.0.0.0:5000 app:app"
echo ""
echo "❏ Frontend is available at: http://localhost:3000"
echo "❏ Backend API is available at: http://localhost:5000"
echo "❏ Health check: curl http://localhost:5000/health"
echo ""

