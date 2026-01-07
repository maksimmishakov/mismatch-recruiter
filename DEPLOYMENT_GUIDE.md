# MisMatch Recruiter - Deployment Guide

## Pre-Deployment Checklist

### Infrastructure Requirements
- [ ] Server with Docker and Docker Compose installed
- [ ] PostgreSQL 15+ (or use Docker image)
- [ ] Node.js 18+ for frontend builds
- [ ] Python 3.11+ for backend development
- [ ] SSL/TLS certificates for HTTPS
- [ ] Domain name configured
- [ ] DNS records pointing to server

### Security Requirements
- [ ] Generate secure JWT_SECRET_KEY
- [ ] Set secure database password
- [ ] Configure firewall rules
- [ ] Enable CORS for frontend domain only
- [ ] Set secure cookie flags
- [ ] Enable HTTPS
- [ ] Configure security headers

## Deployment Steps

### 1. Prepare Server

```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### 2. Clone Repository

```bash
cd /opt
sudo git clone https://github.com/your-username/mismatch-recruiter.git
cd mismatch-recruiter
```

### 3. Configure Environment

```bash
# Create production environment file
sudo cp .env.example .env

# Edit with secure values
sudo nano .env
```

Required environment variables:
```bash
DATABASE_URL=postgresql://user:password@db:5432/mismatch_recruiter
FLASK_ENV=production
FLASK_DEBUG=False
JWT_SECRET_KEY=<generate-secure-key>
REACT_APP_API_URL=https://api.yourdomain.com
```

### 4. Build Docker Images

```bash
# Build images
docker-compose build

# Or pull pre-built images if available
docker pull mismatch-recruiter-backend:latest
docker pull mismatch-recruiter-frontend:latest
```

### 5. Start Services

```bash
# Start all services in background
docker-compose up -d

# Verify services are running
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 6. Initialize Database

```bash
# Run database migrations
docker-compose exec backend python -m flask db upgrade

# Or create tables directly
docker-compose exec backend python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### 7. Configure Nginx (Reverse Proxy)

Create `/etc/nginx/sites-available/mismatch-recruiter`:

```nginx
upstream backend {
    server backend:5000;
}

upstream frontend {
    server frontend:3000;
}

server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 8. Enable SSL/TLS with Let's Encrypt

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Generate certificates
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com

# Update Nginx configuration with SSL
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com
```

### 9. Configure Monitoring

```bash
# Install and start Prometheus
docker run -d --name prometheus prom/prometheus:latest

# Install and start Grafana
docker run -d --name grafana -p 3001:3000 grafana/grafana:latest
```

### 10. Setup Logging

```bash
# Install ELK Stack (optional)
docker-compose -f docker-compose.elk.yml up -d
```

## Backup and Recovery

### Database Backup

```bash
# Backup PostgreSQL database
docker-compose exec db pg_dump -U recruiter_user mismatch_recruiter > backup.sql

# Restore from backup
cat backup.sql | docker-compose exec -T db psql -U recruiter_user mismatch_recruiter
```

### Volume Backup

```bash
# Backup persistent volumes
docker run --rm -v mismatch-recruiter_postgres_data:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/postgres_backup.tar.gz -C /data .
```

## Monitoring and Maintenance

### Health Checks

```bash
# Check backend health
curl http://localhost:5000/api/health

# Check frontend
curl http://localhost:3000

# View container logs
docker-compose logs --tail=100 backend
```

### Performance Optimization

1. **Database Optimization**
   - Create indexes on frequently queried columns
   - Use connection pooling
   - Regular VACUUM and ANALYZE

2. **Application Optimization**
   - Enable caching (Redis)
   - Compress API responses
   - Implement pagination
   - Use CDN for static assets

3. **Infrastructure Optimization**
   - Horizontal scaling with load balancing
   - Auto-scaling based on metrics
   - Resource limits in Docker

### Log Management

```bash
# View logs
docker-compose logs --tail=100 -f backend

# Export logs
docker-compose logs backend > backend.log

# Setup log rotation
sudo nano /etc/logrotate.d/mismatch-recruiter
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend service to 3 instances
docker-compose up -d --scale backend=3

# Use load balancer to distribute traffic
# (Requires Nginx or HAProxy configuration)
```

### Database Replication

1. Setup PostgreSQL streaming replication
2. Configure hot standby
3. Setup automated failover

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   sudo lsof -i :5000
   sudo kill -9 <PID>
   ```

2. **Database Connection Issues**
   ```bash
   docker-compose exec db psql -U recruiter_user -c "SELECT version();"
   ```

3. **Out of Disk Space**
   ```bash
   docker system prune -a  # Remove unused images
   docker volume prune     # Remove unused volumes
   ```

4. **Memory Issues**
   ```bash
   docker stats  # Monitor memory usage
   ```

## Maintenance Schedule

- **Daily**: Monitor logs and metrics
- **Weekly**: Database optimization (VACUUM, ANALYZE)
- **Monthly**: Security updates and patches
- **Quarterly**: Full system backup and recovery test
- **Annually**: Capacity planning and infrastructure review

## Contact & Support

For deployment issues, contact: ops@mismatchrecruiter.com
