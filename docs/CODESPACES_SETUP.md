# 👨‍💻 GitHub Codespaces Setup Guide

## ⚡ One-Click Development Environment

MisMatch Recruiter is fully configured for GitHub Codespaces - no local setup required!

### Quick Start (30 seconds)

1. **Open this repository on GitHub**
2. Click the **Code** button (green)
3. Select **Codespaces** tab
4. Click **Create codespace on main**
5. Wait 2-3 minutes for environment to initialize

**That's it!** Your full dev environment is ready:
- ✅ Python 3.12 with all dependencies
- ✅ PostgreSQL 15 database
- ✅ Redis 7 cache
- ✅ Node.js 18 (for future frontend)
- ✅ Docker & Docker Compose
- ✅ VS Code extensions (Python, GitLens, Copilot)

### What Gets Installed Automatically

The `.devcontainer/setup-dev.sh` script runs automatically and:

```bash
✅ Updates system packages
✅ Installs Python dependencies (Flask, SQLAlchemy, etc.)
✅ Installs dev tools (pytest, black, flake8)
✅ Creates PostgreSQL database
✅ Initializes Redis cache
```

## 🚀 Next Steps After Codespace Opens

### 1. Start Backend Server
```bash
source /workspace/venv/bin/activate
python app.py
```

### 2. Access the Application
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

### 3. Run Docker Stack (for Lamoda demo)
```bash
docker-compose up -d
```

This starts:
- Backend (port 5000)
- PostgreSQL (port 5432)
- Redis (port 6379)
- Prometheus (port 9090)
- Grafana (port 3001)
- PgAdmin (port 5050)

### 4. Run Tests
```bash
cd /workspace
pytest tests/ -v --cov
```

## 📄 Configuration Files

### `.devcontainer/devcontainer.json`
Defines your Codespace environment:
- Base image: Python 3.12
- Features: PostgreSQL 15, Redis 7, Node.js 18
- Port forwarding: 5000, 3000, 5432, 6379, 8080, 9090, 3001
- VS Code extensions and settings

### `.devcontainer/setup-dev.sh`
Automatic setup script that:
- Updates packages
- Creates Python virtual environment
- Installs pip dependencies
- Initializes PostgreSQL database

## 🔇 Customizing Your Environment

### Add More VS Code Extensions

Edit `.devcontainer/devcontainer.json`:
```json
"extensions": [
  "ms-python.python",
  "ms-python.vscode-pylance",
  "YOUR-EXTENSION-ID"
]
```

### Install Additional System Packages

Edit `.devcontainer/setup-dev.sh`:
```bash
apt-get install -y your-package-name
```

### Change Python Version

Edit `.devcontainer/devcontainer.json`:
```json
"image": "mcr.microsoft.com/devcontainers/python:3.11"
```

## 📚 Environment Variables

Automatically loaded from `.env` file:

```bash
FLASK_ENV=development
DATABASE_URL=postgresql://mismatch_user:password@localhost/mismatch
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=dev-secret-key
```

## ⚛️ Port Forwarding

These ports are automatically forwarded:

| Port | Service | URL |
|------|---------|-----|
| 5000 | Flask Backend | http://localhost:5000 |
| 3000 | Frontend/Grafana | http://localhost:3000 |
| 5432 | PostgreSQL | localhost:5432 |
| 6379 | Redis | localhost:6379 |
| 8080 | Reserved | http://localhost:8080 |
| 9090 | Prometheus | http://localhost:9090 |
| 3001 | Grafana | http://localhost:3001 |

## 🛠️ Troubleshooting

### Python dependencies not installed?
```bash
source /workspace/venv/bin/activate
pip install -r requirements.txt
```

### Database connection error?
```bash
psql -U mismatch_user -d mismatch -c "SELECT version();"
```

### Port already in use?
```bash
lsof -i :5000  # Check what's using port 5000
```

### Need to rebuild container?

1. Click **Codespaces** button (bottom left)
2. Select your codespace
3. Click **...** (three dots)
4. Choose **Rebuild container**

## 📄 Documentation

- [Docker Compose Setup](./DOCKER_SETUP.md)
- [Lamoda Integration Guide](./LAMODA_INTEGRATION.md)
- [API Documentation](./API.md)
- [Project Structure](./PROJECT_STRUCTURE.md)

## 🚀 Pro Tips

### Use GitHub Copilot
Codespaces comes with GitHub Copilot built-in! Just start typing and get AI suggestions.

### Terminal Shortcuts
- `Ctrl+`` - Open integrated terminal
- `Ctrl+J` - Toggle panel
- `Ctrl+K Ctrl+S` - Keyboard shortcuts

### Git Integration
All git commands work seamlessly:
```bash
git pull
git add .
git commit -m "Your message"
git push
```

### Extensions Recommendations
- **Thunder Client** - API testing
- **REST Client** - Quick API requests
- **Peacock** - Color code your workspace

## 🌟 Performance Tips

1. **Close unused tabs** - Reduces memory usage
2. **Use Stop button** - Pause codespace when not working (saves hours)
3. **Configure auto-stop** - Stops after 30 mins of inactivity (default)
4. **Monitor storage** - You get 20GB free per month

## 📄 Additional Resources

- [GitHub Codespaces Docs](https://docs.github.com/en/codespaces)
- [Dev Containers Specification](https://containers.dev/)
- [VS Code in Codespaces](https://code.visualstudio.com/docs/remote/codespaces)

---

**Status**: ✅ Production Ready for Development
**Last Updated**: 2026-01-03
**Supported**: Python 3.12, PostgreSQL 15, Redis 7
