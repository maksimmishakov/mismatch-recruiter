# Production Deployment Guide

## Overview
This guide provides comprehensive instructions for deploying the MisMatch Recruiter application to production environments.

## Prerequisites
- Docker and Docker Compose installed
- PostgreSQL 12+ or database service
- Python 3.8+
- Redis instance for caching
- Domain name and SSL certificate

## Environment Configuration

### 1. Prepare Environment Variables
```bash
cp .env.example .env
```

Edit `.env` with production values:
```
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=<generate-secure-key>
DATABASE_URL=postgresql://user:password@db-host:5432/db_name
REDIS_URL=redis://redis-host:6379/0
```

### 2. Generate Secret Key
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Docker Deployment

### Build Images
```bash
docker-compose build
```

### Run Services
```bash
docker-compose up -d
```

### Database Migrations
```bash
docker-compose exec backend flask db upgrade
```

### Health Check
```bash
curl http://localhost:5000/api/health
```

## Direct Server Deployment

### 1. System Setup
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-pip postgresql postgresql-contrib redis-server nginx

# Create application user
sudo useradd -m -s /bin/bash recruiter
```

### 2. Application Setup
```bash
# Clone repository
cd /opt
sudo git clone https://github.com/maksimmishakov/mismatch-recruiter.git
sudo chown -R recruiter:recruiter mismatch-recruiter
```

### 3. Python Environment
```bash
cd /opt/mismatch-recruiter
sudo -u recruiter python3 -m venv venv
sudo -u recruiter venv/bin/pip install -r backend/requirements.txt
```

### 4. Database Setup
```bash
# Create database
sudo -u postgres createdb mismatch_db
sudo -u postgres createuser recruiter -P
sudo -u postgres psql mismatch_db -c "GRANT ALL PRIVILEGES ON DATABASE mismatch_db TO recruiter;"

# Run migrations
sudo -u recruiter venv/bin/python backend/wsgi.py db upgrade
```

### 5. Gunicorn Setup
```bash
# Create systemd service
sudo tee /etc/systemd/system/mismatch-recruiter.service << EOF
[Unit]
Description=MisMatch Recruiter Application
After=network.target

[Service]
Type=notify
User=recruiter
WorkingDirectory=/opt/mismatch-recruiter
ExecStart=/opt/mismatch-recruiter/venv/bin/gunicorn \\
    --workers 4 \\
    --worker-class sync \\
    --bind 127.0.0.1:5000 \\
    --timeout 30 \\
    backend.wsgi:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable mismatch-recruiter
sudo systemctl start mismatch-recruiter
```

### 6. Nginx Configuration
```bash
sudo tee /etc/nginx/sites-available/mismatch-recruiter << 'EOF'
upstream mismatch_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    client_max_body_size 16M;
    
    location / {
        proxy_pass http://mismatch_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /opt/mismatch-recruiter/frontend/build/static/;
        expires 1y;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/mismatch-recruiter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Monitoring

### Application Logs
```bash
# Docker
docker-compose logs -f backend

# Systemd
sudo journalctl -u mismatch-recruiter -f
```

### Health Checks
```bash
curl https://your-domain.com/api/health
```

## Security Checklist

- [ ] SECRET_KEY changed from default
- [ ] DATABASE_URL uses secure connection
- [ ] SSL certificate installed
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] CSRF protection enabled
- [ ] Security headers configured
- [ ] Database backups configured
- [ ] Log rotation configured
- [ ] Firewall rules updated

## Backup Strategy

### Database Backup
```bash
postgresql_backup.sh --db mismatch_db --user recruiter
```

### Regular Backups
Configure daily backups with:
```bash
0 2 * * * /opt/mismatch-recruiter/scripts/backup.sh
```

## Rollback Procedure

1. Identify previous working version
2. Checkout previous commit
3. Run database migrations (if needed)
4. Restart application
5. Verify health checks pass

## Support

For issues or questions, contact the development team.
