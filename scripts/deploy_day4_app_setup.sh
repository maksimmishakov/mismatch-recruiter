#!/bin/bash
# НЕДЕЛЯ 1, ДЕНЬ 4: Application deployment
# Запускать на APP_SERVER_1 и APP_SERVER_2

set -e

echo '=== НАЧАЛО РАЗВЕРТЫВАНИЯ ПРИЛОЖЕНИЯ ==='

APP_HOME=/opt/mismatch-recruiter
APP_USER=app
APP_GROUP=app
PORT=5000

# ШАГ 1: Установить депенденции
echo '[1] Установка системных депенденций...'
sudo apt-get update
sudo apt-get install -y \
  python3-pip \
  python3-venv \
  python3-dev \
  git \
  build-essential \
  curl \
  wget \
  supervisor \
  libpq-dev

# ШАГ 2: Создать пользователя
echo '[2] Создание пользователя...'
sudo useradd -m -s /bin/bash $APP_USER || true
sudo usermod -aG sudo $APP_USER || true

# ШАГ 3: Клонировать репозиторий
echo '[3] Клонирование репозитория...'
sudo mkdir -p $APP_HOME
sudo chown -R $APP_USER:$APP_GROUP $APP_HOME

sudo -u $APP_USER git clone https://github.com/maksimmishakov/mismatch-recruiter.git $APP_HOME || true
cd $APP_HOME
sudo -u $APP_USER git pull origin main || true

# ШАГ 4: Создать Python virtual environment
echo '[4] Конфигурация Python...'
sudo -u $APP_USER python3 -m venv $APP_HOME/venv
sudo -u $APP_USER $APP_HOME/venv/bin/pip install --upgrade pip setuptools wheel
sudo -u $APP_USER $APP_HOME/venv/bin/pip install -r $APP_HOME/requirements.txt

# ШАГ 5: Настроить environment variables
echo '[5] Настройка окружающей среды...'

sudo tee $APP_HOME/.env > /dev/null << 'ENV_CONFIG'
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here-change-it
DATABASE_URL=postgresql://mismatch_prod:password@DB_SERVER_IP:5432/mismatch_production
REDIS_URL=redis://:password@CACHE_SERVER_IP:6379/0
LAMODA_CLIENT_ID=your-lamoda-client-id
LAMODA_CLIENT_SECRET=your-lamoda-client-secret
LAMODA_REDIRECT_URI=https://api.mismatch-recruiter.ru/api/lamoda/oauth/callback
LAMODA_WEBHOOK_SECRET=your-lamoda-webhook-secret
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
ENV_CONFIG

sudo chown $APP_USER:$APP_GROUP $APP_HOME/.env
sudo chmod 600 $APP_HOME/.env

echo '⚠️  Проредактируйте $APP_HOME/.env с нужными значениями'

# ШАГ 6: Создать systemd service
echo '[6] Создание systemd сервиса...'

sudo tee /etc/systemd/system/mismatch-recruiter.service > /dev/null << 'SYSTEMD_CONFIG'
[Unit]
Description=Mismatch Recruiter Application
After=network.target

[Service]
Type=simple
User=app
WorkingDirectory=/opt/mismatch-recruiter
Environment="PATH=/opt/mismatch-recruiter/venv/bin"
EnvironmentFile=/opt/mismatch-recruiter/.env
ExecStart=/opt/mismatch-recruiter/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 -t 120 app:app
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=mismatch

[Install]
WantedBy=multi-user.target
SYSTEMD_CONFIG

sudo systemctl daemon-reload
sudo systemctl enable mismatch-recruiter

# ШАГ 7: Установить Gunicorn
echo '[7] Установка Gunicorn...'
sudo -u $APP_USER $APP_HOME/venv/bin/pip install gunicorn

# ШАГ 8: Датабазные миграции
echo '[8] Применение database migrations...'
cd $APP_HOME
sudo -u $APP_USER $APP_HOME/venv/bin/flask db upgrade --production

# ШАГ 9: Запустить сервис

echo '[9] Запуск приложения...'
sudo systemctl start mismatch-recruiter

# Проверить статус
echo '[10] Проверка статуса...'
sudo systemctl status mismatch-recruiter

echo ''
echo '=== ПОМЕЩЕНИЕ ПРИЛОЖЕНИЯ ЗАВЕРШЕНО ==='
echo ''
echo 'Проверить:'
echo '  curl http://127.0.0.1:5000/api/health'
echo '  curl -I https://app.mismatch-recruiter.ru/health'
echo ''
echo 'Логи:'
echo '  sudo journalctl -u mismatch-recruiter -f'
echo '  sudo tail -f /var/log/nginx/mismatch-recruiter.access.log'
