# LAMODA Recruiter - Развертывание на Amvera
## Пошаговое руководство (12-15 января 2026)

### ФАЗА 1: ПОДГОТОВКА (12 января)

#### Шаг 1.1: Проверка всех файлов
```bash
# Должны быть все эти файлы:
ls -la requirements.txt wsgi.py .env.example docker/Dockerfile.api .amvera.yaml

# Результат: ✅ All files present
```

#### Шаг 1.2: Проверка Git
```bash
git status
# Должно быть: On branch main, nothing to commit

git log --oneline | head -3
# Должны быть latest commits
```

#### Шаг 1.3: Финальный коммит
```bash
git add .amvera.yaml .env.example
git commit -m "deploy: Add Amvera configuration files for production deployment"
git push origin main
```

---

### ФАЗА 2: НАСТРОЙКА AMVERA (14 января)

#### Шаг 2.1: Создать аккаунт Amvera
1. Перейти на https://amvera.io
2. Нажать "Sign Up" или "Зарегистрироваться"
3. Заполнить:
   - Email: your-email@lamoda.ru
   - Password: StrongPassword2026!
   - Full Name: Your Name
   - Country: Russian Federation
4. Нажать "Create Account"

#### Шаг 2.2: Подтвердить email
1. Проверить входящие письма
2. Нажать ссылку подтверждения
3. Вернуться в Amvera Dashboard

#### Шаг 2.3: Создать новый проект
1. На Dashboard: нажать "Create New Project" или "New Project"
2. Выбрать "GitHub" как источник
3. Нажать "Connect to GitHub"

---

### ФАЗА 3: ИНТЕГРАЦИЯ GITHUB (14 января)

#### Шаг 3.1: Авторизация GitHub в Amvera
1. На странице авторизации нажать "Authorize amvera-io"
2. Разрешить доступ к репозиториям
3. Дождаться перенаправления

#### Шаг 3.2: Выбрать репозиторий
1. Выбрать: mismatch-recruiter
2. Выбрать ветку: main
3. Нажать "Continue" или "Next"

#### Шаг 3.3: Конфигурация проекта
1. Project name: lamoda-recruiter
2. Description: AI-powered recruitment system for LAMODA
3. Port: 5000
4. Нажать "Continue"

---

### ФАЗА 4: ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ (14 января)

#### Шаг 4.1: Добавить переменные в Amvera
В разделе "Environment Variables" добавить:

| Ключ | Значение | Описание |
|------|----------|----------|
| FLASK_ENV | production | Production environment |
| FLASK_DEBUG | 0 | Disable debug mode |
| DATABASE_URL | sqlite:///mismatch.db | SQLite database |
| SECRET_KEY | lamoda-prod-secret-2026 | Flask secret key |
| JWT_SECRET_KEY | lamoda-jwt-secret-2026 | JWT authentication |
| CORS_ORIGINS | * | CORS origins |
| LOG_LEVEL | INFO | Logging level |

#### Шаг 4.2: Проверить переменные
1. Убедиться, что все переменные добавлены
2. Нажать "Save" или "Сохранить"
3. Перезагрузить страницу

---

### ФАЗА 5: DOCKER КОНФИГУРАЦИЯ (14 января)

#### Шаг 5.1: Проверить Docker файлы
```bash
# Dockerfile.api содержит:
FROM python:3.12-slim
WORKDIR /workspaces/mismatch-recruiter
RUN apt-get update && apt-get install -y gcc postgresql-client curl
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", wsgi:app"]
```

#### Шаг 5.2: Проверить requirements.txt
```bash
cat requirements.txt | head -10
# Должно быть:
# Flask==2.3.0
# Flask-SQLAlchemy==3.0.0
# Flask-CORS==4.0.0
# gunicorn==20.1.0
```

---

### ФАЗА 6: РАЗВЕРТЫВАНИЕ (14-15 января)

#### Шаг 6.1: Запустить развертывание
1. На странице проекта нажать "Deploy" или "Развернуть"
2. Выбрать ветку: main
3. Дождаться начала сборки

#### Шаг 6.2: Мониторить процесс
1. Смотреть логи развертывания
2. Дождаться статуса "Deployment successful" или зеленого статуса
3. Время развертывания: 5-10 минут

#### Шаг 6.3: Получить Production URL
1. Скопировать Production URL из Dashboard
2. Формат: https://mismatch-recruiter-XXXXX.amvera.io
3. Сохранить URL для демо

---

### ФАЗА 7: ПРОВЕРКА РАЗВЕРТЫВАНИЯ (15 января)

#### Шаг 7.1: Проверить здоровье API
```bash
curl https://mismatch-recruiter-XXXXX.amvera.io/api/health
# Ожидаемый результат:
# {"status": "healthy", "message": "LAMODA Recruiter API is running"}
```

#### Шаг 7.2: Проверить все endpoints
```bash
# Candidates
curl https://mismatch-recruiter-XXXXX.amvera.io/api/candidates

# Jobs
curl https://mismatch-recruiter-XXXXX.amvera.io/api/jobs

# Matches
curl https://mismatch-recruiter-XXXXX.amvera.io/api/matches
```

#### Шаг 7.3: Проверить логи
1. На Dashboard: перейти в "Logs"
2. Убедиться, что нет критических ошибок
3. Должны быть логи вроде:
   - "INFO Listening at http://0.0.0.0:5000"
   - "INFO Workers ready"

---

### ФАЗА 8: ПОДГОТОВКА ДЕМО (15 января, 6:00-9:00)

#### Шаг 8.1: Создать тестовые данные
```bash
# На Production URL создать несколько кандидатов и вакансий
curl -X POST https://mismatch-recruiter-XXXXX.amvera.io/api/candidates \
  -H 'Content-Type: application/json' \
  -d '{"first_name": "Test", "last_name": "User", "email": "test@lamoda.ru", "skills": ["Python"], "experience_years": 5}'
```

#### Шаг 8.2: Проверить тестовые данные
```bash
# Должны видеть созданные данные
curl https://mismatch-recruiter-XXXXX.amvera.io/api/candidates
```

#### Шаг 8.3: Создать DEMO_URLS.txt
```
Production URL: https://mismatch-recruiter-XXXXX.amvera.io
Health Check: https://mismatch-recruiter-XXXXX.amvera.io/api/health
Candidates: https://mismatch-recruiter-XXXXX.amvera.io/api/candidates
Jobs: https://mismatch-recruiter-XXXXX.amvera.io/api/jobs
Matches: https://mismatch-recruiter-XXXXX.amvera.io/api/matches
```

---

### ФАЗА 9: МОНИТОРИНГ PRODUCTION (15 января, 9:00-14:00)

#### Мониторить перед демо:
- ✅ CPU Usage: < 50%
- ✅ Memory Usage: < 512MB
- ✅ Response Time: < 200ms
- ✅ Uptime: 100%
- ✅ Health Check: Passing

#### Если проблемы:
1. **High CPU**: Reduce workers to 2-3
2. **High Memory**: Check for memory leaks in app.py
3. **Slow Response**: Optimize database queries
4. **Down**: Check logs and redeploy

---

### ФАЗА 10: ДЕМОНСТРАЦИЯ (15 января, 14:00)

#### 14:00-14:05: Введение (5 минут)
"Здравствуйте! Сегодня я представлю вам MisMatch - систему AI-подбора кандидатов для LAMODA. Система полностью разработана и развернута в production."

#### 14:05-14:25: Live Demo (20 минут)
1. Показать Production URL
2. Проверить здоровье API
3. Создать нового кандидата в real-time
4. Создать новую вакансию в real-time
5. Создать матч между кандидатом и вакансией
6. Показать список кандидатов с фильтрацией
7. Показать список вакансий
8. Показать матчинги и оценки

#### 14:25-14:45: Q&A (20 минут)
"Спасибо за внимание! Готов ответить на ваши вопросы."

---

### РЕЗЕРВНЫЕ ПЛАНЫ

#### Если Production Down:
1. Нажать "Redeploy" в Dashboard
2. Дождаться нового развертывания (5-10 мин)
3. Если не помогает: использовать локальный backup (localhost:5000)

#### Если забыл Production URL:
1. Перейти на https://amvera.io/dashboard
2. Выбрать проект "lamoda-recruiter"
3. Скопировать URL из раздела "Deployment"

#### Если нет интернета:
1. Использовать localhost: http://localhost:5000
2. Запустить локально: python -m flask --app app run
3. Использовать pre-recorded video

---

## КОНТРОЛЬНЫЙ СПИСОК

- [ ] Все файлы подготовлены (.env.example, .amvera.yaml, wsgi.py)
- [ ] Amvera аккаунт создан и подтвержден
- [ ] GitHub интегрирована с Amvera
- [ ] Переменные окружения установлены
- [ ] Развертывание завершено успешно
- [ ] Production URL рабочий
- [ ] All endpoints отвечают
- [ ] Тестовые данные загружены
- [ ] Demo URLs документированы
- [ ] Production мониторится
- [ ] Demo script готов
- [ ] Резервные планы готовы

---

## ФИНАЛЬНАЯ ПОДГОТОВКА (15 января, 13:00)

✅ **Система готова к демонстрации**
- Production deployment: ACTIVE
- All endpoints: RESPONDING
- Health check: PASSING  
- Response time: < 200ms
- Uptime: 100%

🚀 **READY FOR DEMO AT 14:00 MSK!**
