# ⚡ MisMatch - QUICK START GUIDE

## 🎯 Для РАЗРАБОТЧИКОВ (30 сек)

### Option 1: GitHub Codespaces (Рекомендуется)
```bash
1. Code → Codespaces → Create codespace on main
2. Ждите 2-3 минуты (автоматический setup)
3. source /workspace/venv/bin/activate
4. python app.py
5. http://localhost:5000 ✅
```

### Option 2: Локально (Docker)
```bash
docker-compose up -d
# Все 6 сервисов запустятся
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
# Grafana: http://localhost:3001
```

---

## 🎯 Для LAMODA (Demo)

### Быстрый Demo (5 минут)

#### Шаг 1: Запустить стек
```bash
docker-compose up -d
```

#### Шаг 2: Проверить здоровье
```bash
curl http://localhost:5000/health
# Response: {"status": "ok", ...}
```

#### Шаг 3: Попробовать API
```bash
# GET candidates
curl http://localhost:5000/api/v1/candidates

# GET jobs
curl http://localhost:5000/api/v1/jobs

# GET matches
curl http://localhost:5000/api/v1/matches?job_id=1
```

#### Шаг 4: Открыть Dashboard
- **Backend API**: http://localhost:5000
- **Grafana Metrics**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Database**: http://localhost:5050 (admin@example.com/admin)

---

## 📚 ДОКУМЕНТАЦИЯ

### Для интеграции с Lamoda
📖 **[LAMODA_INTEGRATION.md](./LAMODA_INTEGRATION.md)**
- API endpoints
- Python примеры кода
- 4-шаговая интеграция
- Testing procedures

### Для разработки в Codespaces
👨‍💻 **[CODESPACES_SETUP.md](./docs/CODESPACES_SETUP.md)**
- One-click setup
- Configuration
- Pro tips
- Troubleshooting

### Полный отчет о завершении
✅ **[COMPLETION_SUMMARY.md](./COMPLETION_SUMMARY.md)**
- Статус всех сервисов
- Выполненные задачи
- Next steps
- Docker commands

---

## 🚀 PRODUCTION DEPLOYMENT

### На Amvera (уже настроено)
```bash
# Просто push в main
git push origin main
# Автоматический CI/CD → Deploy
```

**Live URL**: https://mismatch-recruiter-maksimisakov.amvera.io

---

## 🔧 ТЕХНИЧЕСКИЙ СТЕК

```
┌─────────────────────────────────────┐
│         Frontend (React)            │
│      Port 3000 (optional)           │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│    Backend API (Flask)              │
│    Port 5000 ✅ (ACTIVE)            │
└──────────────┬──────────────────────┘
               │
      ┌────────┼────────┐
      │        │        │
  ┌───▼──┐ ┌──▼───┐ ┌──▼─────┐
  │  DB  │ │Cache │ │Metrics │
  │PG 15 │ │Redis7│ │Prom/GF │
  └──────┘ └──────┘ └────────┘
```

---

## 🎓 ПРИМЕРЫ API ЗАПРОСОВ

### 1. Health Check
```bash
GET http://localhost:5000/health

Response:
{
  "status": "ok",
  "service": "mismatch-recruiter",
  "timestamp": "2026-01-03T15:00:00"
}
```

### 2. Get Candidates
```bash
GET http://localhost:5000/api/v1/candidates

Response:
{
  "success": true,
  "data": [],
  "message": "No candidates yet"
}
```

### 3. Get Jobs
```bash
GET http://localhost:5000/api/v1/jobs

Response:
{
  "success": true,
  "data": [],
  "message": "No jobs yet"
}
```

### 4. Get Metrics
```bash
GET http://localhost:5000/metrics

Response: (Prometheus format)
mismatch_requests_total 0
```

---

## 🔐 CREDENTIALS (Development Only)

```
📊 Grafana
URL: http://localhost:3001
User: admin
Pass: admin

🛠️ PgAdmin
URL: http://localhost:5050
Email: admin@example.com
Pass: admin

🗄️ PostgreSQL
Host: localhost:5432
User: mismatch_user
Pass: mismatch_password
DB: mismatch

🔴 Redis
Host: localhost:6379
No auth needed
```

---

## ❌ TROUBLESHOOTING

### Port already in use?
```bash
lsof -i :5000
kill -9 <PID>
```

### Docker container won't start?
```bash
docker-compose down -v
docker-compose up -d
```

### Database connection error?
```bash
docker-compose logs mismatch-db
```

### Need fresh start?
```bash
# Full reset
docker-compose down -v
rm -rf instance/
git clean -fd
docker-compose up -d
```

---

## 📞 SUPPORT

- 📖 Full Documentation: Check `/docs` folder
- 🐛 Issues: GitHub Issues
- �� Questions: Read the docs first!
- 🎯 Lamoda Integration: See LAMODA_INTEGRATION.md

---

**Last Updated**: 2026-01-03 15:00 MSK
**Status**: ✅ Production Ready
**Next**: Get Lamoda API key and integrate!
