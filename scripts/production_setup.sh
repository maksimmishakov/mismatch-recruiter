#!/bin/bash
# Production Environment Setup

set -e

echo "=== Production Setup ==="

# 1. Database Optimization
echo "[1] Database Optimization..."
mysql -h $DB_HOST -u $DB_USER -p$DB_PASS $DB_NAME << SQL
ALTER TABLE users ADD INDEX idx_email (email);
ALTER TABLE jobs ADD INDEX idx_status (status);
ALTER TABLE jobs ADD INDEX idx_created_at (created_at);
ALTER TABLE applications ADD INDEX idx_job_id (job_id);
ALTER TABLE applications ADD INDEX idx_user_id (user_id);
ANALYZE TABLE users, jobs, applications, users_profiles;
SQL

# 2. Create backup directory
echo "[2] Setting up backup directory..."
mkdir -p /var/backups/database
chown backup:backup /var/backups/database
chmod 700 /var/backups/database

# 3. Configure log rotation
echo "[3] Configuring log rotation..."
cat > /etc/logrotate.d/mismatch-recruiter << 'LOGCONF'
/var/log/mismatch-recruiter/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 app app
    sharedscripts
    postrotate
        systemctl reload mismatch-recruiter > /dev/null 2>&1 || true
    endscript
}
LOGCONF

# 4. Setup monitoring directory
echo "[4] Setting up monitoring..."
mkdir -p /var/log/mismatch-recruiter
chown app:app /var/log/mismatch-recruiter
chmod 755 /var/log/mismatch-recruiter

# 5. Enable SSL
echo "[5] Setting up SSL certificates..."
if [ ! -f /etc/letsencrypt/live/app.example.com/fullchain.pem ]; then
    certbot certonly --standalone -d app.example.com
fi

# 6. Configure firewall
echo "[6] Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

echo "=== Production Setup Complete ==="
