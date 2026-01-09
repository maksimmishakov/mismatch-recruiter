#!/bin/bash
# НЕДЕЛЯ 1, ДЕНЬ 5: Load Testing
# Протестировать приложение

set -e

echo '=== НАЧАЛО LOAD TESTING ==='

# Параметры
TARGET_URL="https://app.mismatch-recruiter.ru"
CONCURRENCY=1000
DURATION=60
WARMUP=10

# ШАГ 1: Установить Apache Bench
echo '[1] Установка wrk (быстрые load tests)...'
sudo apt-get install -y curl httpie

# Установить wrk
if ! command -v wrk &> /dev/null; then
    echo '[2] Компиляция wrk...'
    sudo apt-get install -y build-essential
    git clone https://github.com/wg/wrk.git /tmp/wrk || true
    cd /tmp/wrk
    make
    sudo cp wrk /usr/local/bin/
    cd -
fi

# ШАГ 2: Health check
echo '[2] Проверка health endpoint...'
curl -f -s $TARGET_URL/health > /dev/null && echo '✅ Приложение готово' || echo '❌ Приложение не отвечает'

# ШАГ 3: Прегрев (warmup)
echo '[3] Прегрев системы '$WARMUP' секунд...'
wrk -t 4 -c 10 -d ${WARMUP}s $TARGET_URL/api/health

# ШАГ 4: Load test
echo '[4] Load testing ('$CONCURRENCY' concurrent connections, '$DURATION' seconds)...'
wrk -t 8 -c $CONCURRENCY -d ${DURATION}s $TARGET_URL/api/health > /tmp/load-test-results.txt

echo ''
echo '=== RESULTS ==='
cat /tmp/load-test-results.txt

# Сохранить результаты
echo ''
echo 'Результаты сохранены в /tmp/load-test-results.txt'

# Проверка ошибок
echo ''
echo '[5] Проверка ошибок...'
echo 'Открыть логи:'
echo '  sudo tail -100 /var/log/nginx/mismatch-recruiter.error.log'
echo '  sudo journalctl -u mismatch-recruiter | tail -100'

echo ''
echo '=== ОЧКИ ==='
echo 'Отличные результаты:'
echo '  - Error rate: 0%'
echo '  - Latency p95: < 100ms'
echo '  - Requests/sec: > 1000'
echo '  - no timeouts'
