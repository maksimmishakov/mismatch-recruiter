# PRODUCTION DEPLOYMENT PLAN

**Project**: Mismatch Recruiter
**Target Domain**: app.mismatch-recruiter.ru
**Launch Date**: January 2026
**Status**: ACTIVE DEPLOYMENT PHASE

---

## PRIORITY 1: DOMAIN & SSL SETUP (Next 24 hours)

### Objectives

1. ✅ Configure custom domain `app.mismatch-recruiter.ru`
2. ✅ Set up SSL certificate for production domain  
3. ✅ Configure DNS records (A record, CNAME)
4. ✅ Test HTTPS connectivity

### Domain Setup

#### Step 1: Register Domain

**Domain Name**: mismatch-recruiter.ru
**DNS Provider**: Cloudflare (recommended for DDoS protection)
**Configuration**:

```
A Record:        mismatch-recruiter.ru        -> [Production IP]
CNAME:           www                          -> mismatch-recruiter.ru
CNAME:           app                          -> mismatch-recruiter.ru
CNAME:           api                          -> mismatch-recruiter.ru
CNAME:           cdn                          -> mismatch-recruiter.ru
MX Record:       mail                         -> [Mail Server]
TXT Record:      SPF                          -> "v=spf1 include:cloudflare.net ~all"
```

#### Step 2: SSL Certificate Setup

**Method**: Let's Encrypt (free, automated)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-dns-cloudflare

# Create Cloudflare API token
# Store in ~/.cloudflare.ini

# Request SSL certificate
certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials ~/.cloudflare.ini \
  -d mismatch-recruiter.ru \
  -d app.mismatch-recruiter.ru \
  -d api.mismatch-recruiter.ru \
  -d cdn.mismatch-recruiter.ru

# Certificates will be in:
# /etc/letsencrypt/live/mismatch-recruiter.ru/
```

#### Step 3: Configure Auto-Renewal

```bash
# Create renewal script
cat > /etc/cron.d/certbot-renewal << 'CRON'
0 3 * * * certbot renew --quiet --post-hook "systemctl reload nginx"
CRON

# Test renewal
certbot renew --dry-run
```

### SSL Configuration in Nginx

```nginx
# /etc/nginx/sites-available/mismatch-recruiter

server {
    listen 80;
    listen [::]:80;
    server_name mismatch-recruiter.ru app.mismatch-recruiter.ru api.mismatch-recruiter.ru;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name mismatch-recruiter.ru app.mismatch-recruiter.ru api.mismatch-recruiter.ru;
    
    # SSL Certificates
    ssl_certificate /etc/letsencrypt/live/mismatch-recruiter.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mismatch-recruiter.ru/privkey.pem;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Proxy settings
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:5000/api/health;
        access_log off;
    }
}
```

### Testing

```bash
# Test HTTPS connectivity
curl -I https://app.mismatch-recruiter.ru/health

# Expected response:
# HTTP/2 200
# Content-Type: application/json
# Strict-Transport-Security: max-age=31536000; includeSubDomains

# Test SSL certificate
openssl s_client -connect app.mismatch-recruiter.ru:443 -servername app.mismatch-recruiter.ru

# Test DNS propagation
nslookup app.mismatch-recruiter.ru
dig app.mismatch-recruiter.ru

# Check SSL grade
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=app.mismatch-recruiter.ru
```

**Expected Duration**: 2-4 hours
**Owner**: DevOps Lead
**Status**: ⏳ IN PROGRESS

---

## PRIORITY 2: PRODUCTION ENVIRONMENT SETUP (Day 1-2)

### Objectives

1. Provision production servers (Amvera Cloud or AWS)
2. Set up production database (PostgreSQL)
3. Configure production Redis instance
4. Set up log aggregation (ELK/CloudWatch)
5. Configure monitoring (Prometheus/Grafana)

### Infrastructure Architecture

```
Internet
   |
   v
Cloudflare CDN (DDoS Protection)
   |
   v
Load Balancer (HAProxy/Nginx)
   |
   +--------+--------+
   |        |        |
   v        v        v
  App1     App2     App3  (3x Replicas)
   |        |        |
   +--------+--------+
        |
        v
  Redis Cache Cluster
        |
   +----+----+
   |    |    |
   v    v    v
 PostgreSQL Primary -> Standby 1 -> Standby 2
        |
        v
  Automated Backups (S3)
```

### Infrastructure Provisioning

#### Option A: Amvera Cloud (Russian-based)

```bash
# 1. Create account on amvera.ru
# 2. Provision instances:

Production Servers:
├─ 2x App Servers (4 CPU, 8GB RAM each) - Ubuntu 22.04 LTS
├─ 1x Database Server (8 CPU, 16GB RAM) - PostgreSQL
└─ 1x Cache Server (2 CPU, 4GB RAM) - Redis

# 3. Configure VPC and security groups
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 5432/tcp    # PostgreSQL (internal only)
sudo ufw allow 6379/tcp    # Redis (internal only)
sudo ufw enable
```

#### Option B: AWS EC2

```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Create subnets
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
aws ec2 create-subnet --vpc-id vpc-xxx --cidr-block 10.0.2.0/24 --availability-zone us-east-1b

# Create security groups
aws ec2 create-security-group --group-name mismatch-sg --description "Mismatch Recruiter" --vpc-id vpc-xxx

# Launch EC2 instances
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.large \
  --key-name mismatch-key \
  --security-group-ids sg-xxx \
  --subnet-id subnet-xxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=mismatch-app-1}]'
```

### Database Setup

```bash
# 1. Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib postgresql-client

# 2. Configure PostgreSQL
sudo -u postgres psql

CREATE DATABASE mismatch_production;
CREATE USER mismatch_prod WITH PASSWORD 'secure_password_here';
ALTER ROLE mismatch_prod SET client_encoding TO 'utf8';
ALTER ROLE mismatch_prod SET default_transaction_isolation TO 'read committed';
ALTER ROLE mismatch_prod SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE mismatch_production TO mismatch_prod;
\q

# 3. Configure PostgreSQL for production
sudo nano /etc/postgresql/14/main/postgresql.conf

# Settings:
max_connections = 200
shared_buffers = 4GB
effective_cache_size = 12GB
maintenance_work_mem = 1GB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 10MB

# 4. Enable backup and replication
sudo nano /etc/postgresql/14/main/pg_hba.conf

# Add replication users
local   replication     replication_user                     md5
host    replication     replication_user     127.0.0.1/32    md5
host    replication     replication_user     10.0.2.0/24     md5

# 5. Run initial migration
cd /app
flask db upgrade --production
```

### Redis Setup

```bash
# 1. Install Redis
sudo apt-get install redis-server

# 2. Configure Redis
sudo nano /etc/redis/redis.conf

# Settings:
bind 0.0.0.0                      # Allow remote connections
protected-mode yes
port 6379
daemonize yes
supervised systemd
pidfile /var/run/redis/redis-server.pid
loglevel notice
logfile /var/log/redis/redis-server.log
databasesEOF
# Continuation of Production Setup
# Let me save this and create next steps document
echo 'PRODUCTION_DEPLOYMENT_PLAN.md created successfully' && wc -l PRODUCTION_DEPLOYMENT_PLAN.md
cat > NEXT_STEPS_PRODUCTION_DEPLOYMENT.md << 'EOF'
# NEXT STEPS: PRODUCTION DEPLOYMENT

**Date**: January 9, 2026, 5:00 PM MSK
**Status**: Ready for immediate execution
**Timeline**: Deploy within 7 days

---

## IMMEDIATE ACTIONS (Next 24 hours)

### 1. Domain Registration & DNS Setup

**Action Items:**
```bash
# Step 1: Register domain on Cloudflare
Domain: mismatch-recruiter.ru
Provider: Cloudflare (cloudflare.com)
Cost: ~$0.88/year (cheap top-level domain)

# Step 2: Configure DNS records
A Record: mismatch-recruiter.ru -> [Production Server IP]
CNAME: app -> mismatch-recruiter.ru
CNAME: api -> mismatch-recruiter.ru
CNAME: www -> mismatch-recruiter.ru

# Step 3: Update Cloudflare security
- Enable DDoS protection
- Enable WAF (Web Application Firewall)
- Set SSL/TLS to "Full (strict)"
- Enable HSTS
```

**Responsible**: DevOps Lead
**Deadline**: January 10, 2026 (24 hours)
**Status**: ⏳ PENDING

---

### 2. Production Server Provisioning

**Infrastructure Requirements:**
```
Production Servers:
├─ 2x Application Servers
│  ├─ CPU: 4 cores
│  ├─ RAM: 8GB
│  ├─ Storage: 100GB SSD
│  └─ OS: Ubuntu 22.04 LTS
│
├─ 1x Database Server
│  ├─ CPU: 8 cores
│  ├─ RAM: 16GB  
│  ├─ Storage: 500GB SSD
│  └─ DB: PostgreSQL 14
│
└─ 1x Cache Server
   ├─ CPU: 2 cores
   ├─ RAM: 4GB
   ├─ Storage: 50GB SSD
   └─ Cache: Redis 7.0
```

**Provider Options:**
- Amvera Cloud (amvera.ru) - Russian-based, ~$50/month
- AWS EC2 - Global, ~$60/month
- DigitalOcean - Simple setup, ~$40/month

**Setup Script:**
```bash
#!/bin/bash
set -e

echo "[1] Installing system packages..."
sudo apt-get update
sudo apt-get install -y \
  curl \
  wget \
  git \
  nginx \
  python3-pip \
  postgresql-client \
  redis-tools \
  htop \
  iotop

echo "[2] Cloning application repository..."
cd /opt
sudo git clone https://github.com/maksimmishakov/mismatch-recruiter.git
cd mismatch-recruiter

echo "[3] Setting up Python environment..."
sudo python3 -m pip install virtualenv
sudo python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

echo "[4] Configuring environment variables..."
sudo cp .env.production.template .env.production
sudo nano .env.production  # Edit with actual values

echo "[5] Running database migrations..."
flask db upgrade --production

echo "[6] Setting up systemd service..."
sudo cp deployment/mismatch.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mismatch
sudo systemctl start mismatch

echo "[7] Configuring Nginx..."
sudo cp deployment/nginx.conf /etc/nginx/sites-available/mismatch
sudo ln -s /etc/nginx/sites-available/mismatch /etc/nginx/sites-enabled/mismatch
sudo nginx -t
sudo systemctl reload nginx

echo "✅ Production setup complete!"
```

**Responsible**: Infrastructure Team
**Deadline**: January 11, 2026 (48 hours)
**Status**: ⏳ PENDING

---

### 3. SSL Certificate Setup

**Steps:**
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Request certificate
sudo certbot certonly \
  --nginx \
  -d mismatch-recruiter.ru \
  -d app.mismatch-recruiter.ru \
  -d api.mismatch-recruiter.ru

# Auto-renewal
sudo certbot renew --dry-run
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Verify
ls -la /etc/letsencrypt/live/mismatch-recruiter.ru/
```

**Responsible**: DevOps Lead
**Deadline**: January 11, 2026
**Status**: ⏳ PENDING

---

## WEEK 1 DEPLOYMENT SCHEDULE

### Monday, January 13
```
09:00 - Team standup
09:30 - Final security audit
10:00 - Database migration dry-run
11:00 - Monitoring system verification
12:00 - Load test (1000 concurrent users)
13:00 - Lunch break
14:00 - Go-live checklist review
15:00 - Team readiness confirmation
16:00 - On-call rotation briefing
17:00 - Final preparations
```

### Tuesday, January 14
```
09:00 - Production deployment window opens
09:00 - Deploy to green environment
09:15 - Run smoke tests
09:30 - Database verification
09:45 - Health check verification
10:00 - Switch traffic (blue -> green)
10:15 - Intensive monitoring (30 min)
10:45 - Gradual traffic increase
11:00 - Team notification
12:00 - First user acceptance tests
13:00 - Lunch
14:00 - Lamoda integration testing
15:00 - First matches verification
16:00 - Customer communication
17:00 - End of day summary
18:00 - Night shift begins
```

---

## PHASE 11: FEATURE EXPANSION (Months 2-3)

### Planned Features

```
1. Advanced Matching Algorithms
   ├─ Machine Learning integration (TensorFlow)
   ├─ Candidate scoring refinement
   ├─ Job recommendation engine
   └─ Predictive analytics

2. Enhanced Notifications
   ├─ Push notifications (Firebase)
   ├─ In-app messaging
   ├─ Email templates customization
   └─ SMS notifications (Twilio)

3. Reporting & Analytics
   ├─ Custom dashboards
   ├─ Export to PDF/Excel
   ├─ Email reports scheduling
   └─ Data visualization (Chart.js)

4. Mobile App
   ├─ iOS app (React Native)
   ├─ Android app (React Native)
   ├─ Push notifications
   └─ Offline mode

5. API Marketplace
   ├─ Open API documentation (Swagger)
   ├─ API keys & rate limiting
   ├─ Third-party integrations
   └─ Developer portal
```

**Timeline**: February - March 2026
**Resources**: +2 engineers
**Budget**: $15,000

---

## PHASE 12: SCALE & ENTERPRISE (Months 4-6)

### Infrastructure Scaling

```
1. High Availability
   ├─ Multi-region deployment (Russia + EU)
   ├─ Database replication
   ├─ Load balancing (Kubernetes)
   └─ Disaster recovery (99.99% uptime target)

2. Performance
   ├─ Database optimization
   ├─ CDN integration (Cloudflare)
   ├─ Query caching (Redis)
   └─ Connection pooling

3. Security
   ├─ Penetration testing
   ├─ GDPR compliance
   ├─ Data encryption (end-to-end)
   └─ Audit logging

4. Compliance
   ├─ SOC 2 certification
   ├─ ISO 27001 certification
   ├─ GDPR compliance documentation
   └─ Data residency options (Russia)
```

**Timeline**: April - June 2026
**Resources**: +3 engineers
**Budget**: $40,000

---

## PHASE 13: MARKET EXPANSION (Months 7-12)

### Growth Strategy

```
1. Customer Acquisition
   ├─ Sales team expansion (5 -> 20 people)
   ├─ Marketing campaign launch
   ├─ Conference presence
   └─ Partnership development

2. Competitive Positioning
   ├─ Feature parity with competitors
   ├─ Superior matching accuracy (target: 95%)
   ├─ Better customer support (24/7)
   └─ Competitive pricing strategy

3. Partnerships
   ├─ Lamoda (primary partner - launched)
   ├─ Yandex Market
   ├─ Avito
   ├─ Other major e-commerce platforms
   └─ HR software integrations

4. Geographic Expansion
   ├─ Russia (primary market)
   ├─ Ukraine (Q3 2026)
   ├─ Belarus (Q4 2026)
   └─ Kazakhstan (Q4 2026)
```

**Timeline**: July - December 2026
**Resources**: +10 people (sales, marketing, support)
**Budget**: $200,000

---

## PRE-LAUNCH CHECKLIST

### Code & Infrastructure

- [ ] All unit tests passing (pytest, jest)
- [ ] Integration tests passing (100% coverage)
- [ ] Code review completed (2+ reviewers)
- [ ] Linting rules passing (pylint, eslint)
- [ ] Security audit completed (OWASP top 10)
- [ ] Docker image built and tested
- [ ] Kubernetes manifests prepared
- [ ] Database migrations tested on backup

### Configuration

- [ ] SSL certificates valid and installed
- [ ] DNS records propagated
- [ ] CDN configured and tested
- [ ] Load balancer operational
- [ ] Database backups configured
- [ ] Log aggregation operational
- [ ] Monitoring alerts active
- [ ] Health check endpoints verified

### Monitoring & Alerting

- [ ] Grafana dashboards created (6+ dashboards)
- [ ] Prometheus targets configured
- [ ] Alert rules defined (10+ rules)
- [ ] Sentry error tracking active
- [ ] Uptime monitoring active
- [ ] Synthetic tests configured
- [ ] PagerDuty integration active
- [ ] Slack alerts configured

### Documentation & Training

- [ ] Deployment guide written
- [ ] Rollback procedure documented
- [ ] Runbooks created (5+ runbooks)
- [ ] API documentation updated
- [ ] Architecture diagram created
- [ ] Team training completed
- [ ] On-call procedures established
- [ ] Post-mortem template prepared

### Business & Legal

- [ ] Go-live announcement prepared
- [ ] Customer communication planned
- [ ] Support team trained (Level 1 & 2)
- [ ] Pricing finalized
- [ ] Terms of service updated
- [ ] Privacy policy updated
- [ ] Legal review completed
- [ ] Insurance updated

---

## SUCCESS METRICS (First Month)

### Technical Metrics

```
Uptime:       99.9%
Latency P95:  < 100ms
Error Rate:   < 0.1%
Cache Hit:    > 80%
DB Response:  < 50ms
```

### Business Metrics

```
Registered Users:      100+
Active Users:          50+
Matches Created:       500+
Customer Satisfaction: > 4.5/5
NPS Score:            > 50
```

### Integration Metrics

```
Lamoda Test Users:     20+
Job Postings Synced:   500+
Sync Success Rate:     99%+
Webhook Processing:    100%
Error Rate:            < 0.5%
```

---

## CONTINGENCY PLANS

### If Database Migration Fails

```
1. Immediately rollback to backup
2. Investigate root cause
3. Fix issue in staging
4. Test thoroughly
5. Retry migration
6. If still failing: manual data entry + sync
```

### If Performance Degrades

```
1. Check database slow query log
2. Analyze Grafana metrics
3. Review error logs (Sentry)
4. Options:
   a. Increase cache TTL
   b. Add database indexes
   c. Scale up resources
   d. Reduce feature set
```

### If Lamoda Integration Breaks

```
1. Disable webhook processing
2. Fallback to manual job entry
3. Investigate API changes
4. Update integration code
5. Re-enable webhooks
6. Verify sync
```

---

## ROLLBACK PROCEDURE

```
If critical issue detected (P1):

0 minutes:   Alert sent
5 minutes:   Team gathered
10 minutes:  Root cause identified
15 minutes:  Rollback decision made
20 minutes:  Previous version deployed
25 minutes:  Health checks verified
30 minutes:  Rollback complete
```

