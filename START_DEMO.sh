#!/bin/bash

# MisMatch Recruiter - DEMO START SCRIPT
# Всё что нужно для запуска демо

echo "================================================"
echo "MisMatch Recruiter - DEMO MODE"
echo "================================================"
echo ""
echo "📋 Текущее время: $(date)"
echo "🎯 Демо Lamoda: 8 января 2026, 13:00 MSK"
echo ""

echo "1️⃣  Очистка старых контейнеров и volumes..."
docker-compose down -v

echo ""
echo "2️⃣  Пересборка Docker образов..."
docker-compose build --no-cache

echo ""
echo "3️⃣  Запуск всех сервисов..."
docker-compose up -d

echo ""
echo "4️⃣  Ожидание 10 секунд для инициализации БД..."
sleep 10

echo ""
echo "✅ ВСЕХ ГОТОВО!"
echo ""
echo "🌐 Доступно:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:5000/api"
echo "   Database:  postgres://localhost:5432"
echo ""
echo "📝 Для тестирования API см. DEMO_TESTING_CHECKLIST.md"
echo ""
echo "==="
echo "Смотрите логи:"
echo "   docker-compose logs -f backend"
echo "   docker-compose logs -f frontend"
echo "   docker-compose logs -f db"
echo ""
