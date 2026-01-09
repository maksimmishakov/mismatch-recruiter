#!/bin/bash
# НЕДЕЛЯ 1, ДЕНЬ 3: PostgreSQL и Redis конфигурация
# Запускать на DATABASE_SERVER

set -e

echo '=== НАЧАЛО УСТАНОВКИ PostgreSQL и Redis ==='

# ШАГ 1: Обновить систему
echo '[1] Обновление системы...'
sudo apt-get update
sudo apt-get upgrade -y

# ШАГ 2: Установить PostgreSQL 14
echo '[2] Установка PostgreSQL 14...'
sudo apt-get install -y postgresql postgresql-contrib postgresql-client libpq-dev

# Проверить версию
sudo -u postgres psql --version

# ШАГ 3: Конфигурация PostgreSQL
echo '[3] Конфигурация PostgreSQL...'

# Создать базу данных
sudo -u postgres psql << 'SQL'
CREATE DATABASE mismatch_production;
CREATE USER mismatch_prod WITH PASSWORD 'strong_password_here_change_it';
ALTER ROLE mismatch_prod SET client_encoding TO 'utf8';
ALTER ROLE mismatch_prod SET default_transaction_isolation TO 'read committed';
ALTER ROLE mismatch_prod SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE mismatch_production TO mismatch_prod;
\c mismatch_production
CREATE EXTENSION IF NOT EXISTS pg_trgm;
GRANT ALL PRIVILEGES ON SCHEMA public TO mismatch_prod;
SQL

echo '✅ PostgreSQL база создана'

# ШАГ 4: Тастроить PostgreSQL для Production
echo '[4] Оптимизация PostgreSQL для production...'

# Копия production config
sudo tee /etc/postgresql/14/main/postgresql.conf > /dev/null << 'POSTGRE_CONFIG'
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
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 64
hot_standby = on
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_statement = 'none'
log_min_duration_statement = 1000
shared_preload_libraries = 'pg_stat_statements'
POSTGRE_CONFIG

sudo systemctl restart postgresql

echo '✅ PostgreSQL оптимизирована'

# ШАГ 5: Установить Redis 7
echo '[5] Установка Redis 7...'
sudo apt-get install -y redis-server redis-tools

# Проверить версию
redis-cli --version

# ШАГ 6: Конфигурация Redis
echo '[6] Конфигурация Redis...'

sudo tee /etc/redis/redis.conf > /dev/null << 'REDIS_CONFIG'
port 6379
bind 0.0.0.0
protected-mode yes
daemonize yes
supervised systemd
pidfile /var/run/redis/redis-server.pid
loglevel notice
logfile /var/log/redis/redis-server.log
databases 16
requirepass redis_password_here_change_it
maxmemory 2gb
maxmemory-policy allkeys-lru
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
REDIS_CONFIG

sudo systemctl restart redis-server

echo '✅ Redis конфигурирован'

# ШАГ 7: Верификация
echo '[7] Верификация сервисов...'

# Проверить PostgreSQL
sudo systemctl status postgresql
sudo -u postgres psql -c 'SELECT version();'

# Проверить Redis
sudo systemctl status redis-server
redis-cli ping

echo ''
echo '=== КОНФИГУРАЦИЯ ЗАВЕРШЕНА ==='
echo ''
echo 'Параметры для .env.production:'
echo 'DATABASE_URL=postgresql://mismatch_prod:strong_password_here_change_it@'$HOSTNAME':5432/mismatch_production'
echo 'REDIS_URL=redis://:redis_password_here_change_it@'$HOSTNAME':6379/0'
echo ''
echo 'Добавить эти значения в .env на app серверах'
