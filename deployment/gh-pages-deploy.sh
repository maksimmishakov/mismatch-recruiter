#!/bin/bash

# MisMatch GitHub Pages Deployment Script
# Deploys landing page to gh-pages branch
# Days 22-28: Optimization and Deployment Phase

set -e

echo "🚀 Starting GitHub Pages deployment..."

# Configuration
REPO_NAME="mismatch-recruiter"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
COMMIT="$(git rev-parse --short HEAD)"

echo "📋 Repository: $REPO_NAME"
echo "📋 Branch: $BRANCH"
echo "📋 Commit: $COMMIT"

# Install dependencies
echo "📦 Installing dependencies..."
if [ -d "frontend" ]; then
  cd frontend
  npm install || npm ci
  cd ..
fi

# Build frontend
echo "🔨 Building landing page..."
if [ -f "frontend/package.json" ]; then
  cd frontend
  npm run build
  cd ..
  echo "✅ Build successful"
fi

# Prepare gh-pages
echo "📂 Preparing deployment directory..."
mkdir -p .gh-pages-temp

# Copy build artifacts
echo "📋 Copying artifacts..."
if [ -d "frontend/dist" ]; then
  rm -rf .gh-pages-temp/*
  cp -r frontend/dist/* .gh-pages-temp/
  touch .gh-pages-temp/.nojekyll
  echo "✅ Artifacts copied"
fi

# Commit and push
echo "📤 Pushing to gh-pages..."
cd .gh-pages-temp
git config user.email "ci@mismatch.io"
git config user.name "MisMatch CI"

if ! git diff --quiet; then
  git add .
  git commit -m "deploy: Landing page update ($COMMIT)"
  git push origin gh-pages
  echo "✅ Pushed to gh-pages"
fi

cd ..

# Cleanup
echo "🧹 Cleaning up..."
rm -rf .gh-pages-temp

echo "🎉 GitHub Pages deployment completed successfully!"
echo "Visit: https://maksimmishakov.github.io/$REPO_NAME"
exit 0
