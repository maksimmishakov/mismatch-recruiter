# MisMatch Recruiter - КРИТИЧЕСКИЕ ПРОБЛЕМЫ И ПЛАН ДЕЙСТВИЙ

**Дата:** 7 января 2026
**Время:** 23:50 MSK
**Статус:** 🔴 КРИТИЧЕСКОЕ - 25% функциональности
**Демо Lamoda:** 8 января 13:00 MSK (осталось ~13 часов)

---

## 🚨 КРИТИЧЕСКИЕ БЛОКИРУЮЩИЕ ПРОБЛЕМЫ (3 ШАГА ДО ЗАПУСКА)

### ПРОБЛЕМА 1: Docker-Compose конфликтует с Dockerfile

**Файл:** `docker-compose.yml`, строка 34
**Серьёзность:** 🔴 КРИТИЧЕСКАЯ - Контейнер не запустится
**Время исправления:** 1 минута

#### Текущая проблема:
```yaml
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  container_name: mismatch_backend
  environment:
    DATABASE_URL: postgresql://recruiter_user:secure_password@db:5432/mismatch_recruiter
    FLASK_ENV: development
    JWT_SECRET_KEY: dev-secret-key-change-in-production
  ports:
    - "5000:5000"
  depends_on:
    db:
      condition: service_healthy
  volumes:
    - ./backend:/app
  command: python main.py  # ❌ КОНФЛИКТ С DOCKERFILE CMD
```

#### Почему это проблема:
- `Dockerfile` (строка 10) имеет: `CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "main:app"]`
- `docker-compose.yml` переопределяет это на: `command: python main.py`
- Результат: Flask запускается напрямую без Gunicorn в production-подобной среде
- Для development нужен development сервер, но он неправильный

#### Решение:
**УДАЛИТЬ строку 34** (command: python main.py)

```yaml
# ✅ ПРАВИЛЬНОЕ
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  container_name: mismatch_backend
  environment:
    DATABASE_URL: postgresql://recruiter_user:secure_password@db:5432/mismatch_recruiter
    FLASK_ENV: development
    JWT_SECRET_KEY: dev-secret-key-change-in-production
  ports:
    - "5000:5000"
  depends_on:
    db:
      condition: service_healthy
  volumes:
    - ./backend:/app
  # command: УДАЛЕНО - использовать CMD из Dockerfile
```

---

### ПРОБЛЕМА 2: API Routes НЕ ПОДКЛЮЧЕНЫ

**Файл:** `backend/app/api/routes.py`
**Серьёзность:** 🔴 КРИТИЧЕСКАЯ - 75% функциональности отсутствует
**Время исправления:** 15-20 минут

#### Текущий статус endpoints:

| Endpoint | Статус | Примечание |
|----------|--------|------------|
| POST /api/auth/register | ✅ Есть | Полностью реализован |
| POST /api/auth/login | ✅ Есть | Полностью реализован |
| GET /api/health | ✅ Есть | Работает |
| GET/POST /api/candidates | ❌ ОТСУТСТВУЕТ | КРИТИЧНО |
| GET /api/candidates/<id> | ❌ ОТСУТСТВУЕТ | КРИТИЧНО |
| PUT /api/candidates/<id> | ❌ ОТСУТСТВУЕТ | КРИТИЧНО |
| DELETE /api/candidates/<id> | ❌ ОТСУТСТВУЕТ | КРИТИЧНО |
| GET/POST /api/jobs | ❌ ОТСУТСТВУЕТ | КРИТИЧНО |
| GET /api/jobs/<id> | ❌ ОТСУТСТВУЕТ | КРИТИЧНО |
| GET/POST /api/matches | ❌ ОТСУТСТВУЕТ | КРИТИЧНО |
| GET /api/auth/me | ❌ ОТСУТСТВУЕТ | ВАЖНО |
| POST /api/auth/refresh | ❌ ОТСУТСТВУЕТ | ВАЖНО |

#### Почему это произошло:
```
Оригинальная структура (план):  backend/app/routes/ (каждый endpoint в отдельном файле)
Текущая реализация:              backend/app/api/routes.py (только auth endpoints)
```

#### Решение: Полностью переписать `backend/app/api/routes.py`

**Новый файл:** `backend/app/api/routes.py` (200+ строк)
