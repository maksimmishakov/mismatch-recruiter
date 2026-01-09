#!/bin/bash
# НЕДЕЛЯ 1, ДЕНЬ 5: Final Pre-Launch Checklist
# Окончательная проверка перед работы в production

set -e

echo '======================================'
echo ' PRODUCTION LAUNCH FINAL CHECKLIST'
echo '======================================'
echo ''

SUCCESS=0
FAILED=0

check_status() {
    if [ $? -eq 0 ]; then
        echo '✅' $1
        ((SUCCESS++))
    else
        echo '❌' $1
        ((FAILED++))
    fi
}

echo '[1] Проверка SSL сертификатов'
curl -s https://app.mismatch-recruiter.ru/ > /dev/null
check_status 'SSL certificate valid'

echo '[2] Проверка Nginx'
sudo nginx -t > /dev/null 2>&1
check_status 'Nginx config valid'

echo '[3] Проверка приложения'
curl -f -s https://app.mismatch-recruiter.ru/api/health > /dev/null
check_status 'Application health endpoint'

echo '[4] Проверка базы данных'
echo 'SELECT 1;' | psql "$DATABASE_URL" > /dev/null 2>&1
check_status 'Database connection'

echo '[5] Проверка Redis'
redis-cli -u "$REDIS_URL" ping > /dev/null 2>&1
check_status 'Redis connection'

echo '[6] Проверка Логов'
sudo tail -5 /var/log/nginx/mismatch-recruiter.access.log > /dev/null
check_status 'Log files accessible'

echo '[7] Проверка DNS'
nslookup app.mismatch-recruiter.ru > /dev/null 2>&1
check_status 'DNS resolution'

echo ''
echo '======================================'
echo ' SUMMARY'
echo '======================================'
echo 'Successful checks:' $SUCCESS
echo 'Failed checks:' $FAILED
echo ''

if [ $FAILED -eq 0 ]; then
    echo '✅ ALL CHECKS PASSED - READY FOR PRODUCTION'
    echo ''
    echo 'Последние шаги:'
    echo '  1. Объявить дату и время запуска: 14 января, 11:00 MSK'
    echo '  2. Отправить инвайты команде'
    echo '  3. Находиться близ нарубителя'
    echo '  4. Мониторить логи:'
    echo '     tail -f /var/log/nginx/mismatch-recruiter.error.log'
    echo '     journalctl -u mismatch-recruiter -f'
    echo '  5. Через 1 час - перевести на нормальное мониторинг'
    exit 0
else
    echo '❌ SOME CHECKS FAILED - DO NOT PROCEED'
    echo ''
    echo 'Ошибки:'
    echo '  1. Проверьте логи недавних ошибок'
    echo '  2. Принимайте срадю для исправления'
    echo '  3. При необходимости - rollback действий'
    exit 1
fi
