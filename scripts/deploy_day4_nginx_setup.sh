#!/bin/bash
# НЕДЕЛЯ 1, ДЕНЬ 4: Nginx конфигурация
# Запускать на APP_SERVER_1 и APP_SERVER_2

set -e

echo '=== НАЧАЛО КОНФИГУРАЦИИ Nginx ==='

# ШАГ 1: Установить Nginx
echo '[1] Установка Nginx...'
sudo apt-get update
sudo apt-get install -y nginx

# Проверить версию
nginx -v

# ШАГ 2: Создать конфигурацию
echo '[2] Настройка Nginx для production...'

sudo tee /etc/nginx/sites-available/mismatch-recruiter > /dev/null << 'NGINX_CONFIG'
upstream mismatch_app {
    server 127.0.0.1:5000 max_fails=3 fail_timeout=30s;
    keepalive 32;
}

# HTTP редирект на HTTPS
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    
    return 301 https://$host$request_uri;
}

# HTTPS server block
server {
    listen 443 ssl http2 default_server;
    listen [::]:443 ssl http2 default_server;
    
    server_name mismatch-recruiter.ru app.mismatch-recruiter.ru api.mismatch-recruiter.ru;
    
    # SSL сертификаты
    ssl_certificate /etc/letsencrypt/live/mismatch-recruiter.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mismatch-recruiter.ru/privkey.pem;
    
    # SSL оптимизация
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;
    
    # HSTS заголовки
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Security заголовки
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
    
    # Gzip компрессия
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss;
    gzip_disable "msie6";
    
    # Логи
    access_log /var/log/nginx/mismatch-recruiter.access.log;
    error_log /var/log/nginx/mismatch-recruiter.error.log warn;
    
    # Health check endpoint
    location /health {
        proxy_pass http://mismatch_app/api/health;
        access_log off;
    }
    
    # API proxy
    location /api/ {
        proxy_pass http://mismatch_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection "";
        proxy_http_version 1.1;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Все другие реквесты на приложение
    location / {
        proxy_pass http://mismatch_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection "";
        proxy_http_version 1.1;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;
    
    location /api/ {
        limit_req zone=api burst=200 nodelay;
    }
    
    location / {
        limit_req zone=general burst=50 nodelay;
    }
}
NGINX_CONFIG

echo '✅ Nginx конфиг сохранен'

# ШАГ 3: Активировать сайт
echo '[3] Активирование сайта...'
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/mismatch-recruiter /etc/nginx/sites-enabled/

# Проверить конфигурацию
echo '[4] Проверка конфигурации...'
sudo nginx -t

if [ $? -eq 0 ]; then
    echo '✅ Конфигурация валидна'
else
    echo '❌ Ошибка в конфигурации!'
    exit 1
fi

# ШАГ 5: Перезагружать Nginx
echo '[5] Перезагружка Nginx...'
sudo systemctl enable nginx
sudo systemctl restart nginx

# Проверить статус
sudo systemctl status nginx

echo ''
echo '=== КОНФИГУРАЦИЯ Nginx ГОТОВА ==='
echo ''
echo 'Проверить:'
echo '  curl -I https://app.mismatch-recruiter.ru/health'
echo ''
echo 'Посмотреть логи:'
echo '  sudo tail -f /var/log/nginx/mismatch-recruiter.access.log'
echo '  sudo tail -f /var/log/nginx/mismatch-recruiter.error.log'
