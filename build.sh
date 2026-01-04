#!/bin/bash
set -e

echo "🚧 MisMatch Recruiter - Production Build Script"
echo "════════════════════════════════"

# Frontend Build
echo "⏳ Building Frontend..."
cd frontend
npm install --production
npm run build
echo "✅ Frontend built successfully"
cd ..

# Backend Dependencies
echo "⏳ Setting up Backend..."
pip3 install -r requirements.txt
echo "✅ Backend dependencies installed"

# Docker Build
echo "⏳ Building Docker images..."
docker-compose build
echo "✅ Docker images built successfully"

# Final Status
echo "════════════════════════════════"
echo "✨ Production build complete!"
echo "Next: docker-compose up -d"
echo "════════════════════════════════"
