#!/bin/bash
set -e

echo "🚀 Setting up MisMatch dev environment..."

# Update packages
echo "📦 Updating system packages..."
apt-get update
apt-get upgrade -y

# Install system dependencies
echo "🔧 Installing system dependencies..."
apt-get install -y build-essential libpq-dev curl git

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
python -m venv /workspace/venv
source /workspace/venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Install dev dependencies
echo "🧪 Installing dev dependencies..."
pip install pytest pytest-cov black flake8 mypy autopep8

# Initialize PostgreSQL database
echo "🗄️ Initializing PostgreSQL database..."
creatdb mismatchdev || true

echo "✅ Setup complete! Your environment is ready."
echo ""
echo "Next steps:"
echo "1. source /workspace/venv/bin/activate"
echo "2. python app.py (to start Flask server)"
echo "3. http://localhost:5000 (access the app)"
echo ""
echo "Happy coding! 🚀"
