# 📊 ДЕНЬ 2: ИНТЕГРАЦИОННЫЕ ТЕСТЫ И E2E СЦЕНАРИИ

## День 2 Полдень (Часы 4-8): Интеграционные тесты

### Сценарий 1: Full Resume Parsing Flow

**Цель:** Проверить полный процесс парсинга резюме от загрузки до извлечения навыков

**Ш аг 1: Отправить резюме на парсинг**
```bash
curl -X POST http://localhost:5000/api/parse-resume \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Senior Python Developer with 7 years experience. Email: john@example.com. Skills: Python, Django, PostgreSQL, Docker. Location: Moscow, Russia"
  }'
```

**Ожидаемый ответ (200 OK):**
```json
{
  "status": "success",
  "email": "john@example.com",
  "skills": ["Python", "Django", "PostgreSQL", "Docker"],
  "experience_years": 7,
  "role": "Senior Backend Developer",
  "location": "Moscow",
  "confidence": 0.97
}
```

**Проверки:**
- ✅ HTTP статус 200
- ✅ Email корректно извлечен
- ✅ Навыки найдены все 4
- ✅ Confidence > 0.95

---

### Сценарий 2: Job Enrichment Flow

**Цель:** Проверить обогащение данных вакансии

**Шаг 1: Отправить вакансию на обогащение**
```bash
curl -X POST http://localhost:5000/api/enrich-job \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "Looking for experienced Python developer with 5+ years...",
    "company": "Tech Corp",
    "location": "San Francisco, CA",
    "salary_range": "120000-150000 USD"
  }'
```

**Ожидаемый ответ (200 OK):**
```json
{
  "status": "success",
  "enriched_data": {
    "required_skills": ["Python", "FastAPI", "PostgreSQL"],
    "seniority_level": "senior",
    "salary_min": 120000,
    "salary_max": 150000,
    "currency": "USD",
    "benefits": ["Remote", "Healthcare", "401k"],
    "job_category": "Backend Development"
  }
}
```

**Проверки:**
- ✅ HTTP статус 200
- ✅ Навыки распознаны
- ✅ Зарплата парсится корректно
- ✅ Уровень сениорности определен

---

### Сценарий 3: Job Matching Algorithm

**Цель:** Проверить алгоритм подбора вакансий кандидату

**Шаг 1: Рассчитать матч между резюме и вакансией**
```bash
curl -X POST http://localhost:5000/api/match \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_id": 1
  }'
```

**Ожидаемый ответ (200 OK):**
```json
{
  "status": "success",
  "match_score": 0.87,
  "match_details": {
    "skills_match": 0.95,
    "experience_match": 0.85,
    "location_match": 0.70,
    "salary_match": 0.88
  },
  "recommendations": [
    "Great skills match",
    "Experience aligns well",
    "Consider relocation or remote work"
  ]
}
```

**Проверки:**
- ✅ Match score в диапазоне 0-1
- ✅ Детальный breakdown компонентов
- ✅ Пол ученые рекомендации

---

### Сценарий 4: Error Handling - Empty Resume

**Цель:** Проверить обработку ошибок при пустом резюме

**Шаг 1: Отправить пустое резюме**
```bash
curl -X POST http://localhost:5000/api/parse-resume \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
```

**Ожидаемый ответ (400 Bad Request):**
```json
{
  "status": "error",
  "error_code": "EMPTY_RESUME",
  "message": "Resume text cannot be empty",
  "details": "Please provide at least 10 characters of resume text"
}
```

**Проверки:**
- ✅ HTTP статус 400
- ✅ Понятное сообщение об ошибке
- ✅ Код ошибки указан

---

### Сценарий 5: Application Workflow

**Шаг 1: Создать вакансию**
```bash
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "company": "Tech Corp",
    "description": "..."
  }'
```

**Ожидаемый ответ:** `{"status": "success", "job_id": 1}`

**Шаг 2: Загрузить резюме**
```bash
curl -X POST http://localhost:5000/api/resume \
  -H "Content-Type: application/json" \
  -d '{"text": "...'}'
```

**Ожидаемый ответ:** `{"status": "success", "resume_id": 1}`

**Шаг 3: Подать заявку**
```bash
curl -X POST http://localhost:5000/api/jobs/1/apply \
  -H "Content-Type: application/json" \
  -d '{"resume_id": 1}'
```

**Ожидаемый ответ (201 Created):**
```json
{
  "status": "success",
  "application_id": 1,
  "application_status": "applied",
  "applied_at": "2025-12-29T22:00:00Z"
}
```

**Шаг 4: Получить заявку**
```bash
curl http://localhost:5000/api/applications/1
```

**Ожидаемый ответ:**
```json
{
  "id": 1,
  "job_id": 1,
  "resume_id": 1,
  "status": "applied",
  "created_at": "2025-12-29T22:00:00Z"
}
```

**Шаг 5: Изменить стадию заявки**
```bash
curl -X PATCH http://localhost:5000/api/applications/1/stage \
  -H "Content-Type: application/json" \
  -d '{"stage": "screening"}'
```

**Ожидаемый ответ:**
```json
{
  "status": "success",
  "application": {
    "id": 1,
    "stage": "screening",
    "updated_at": "2025-12-29T22:05:00Z"
  }
}
```

## День 2 Вечер (Часы 8-12): E2E Тестирование

### Полный сценарий: от постинга вакансии к предложению

**Ожидаемое количество запросов:** 10-15 API calls
**Ожидаемое время:** 30-60 секунд
**Успешный результат:** Все запросы вернули 2xx статусы

---

## Метрики Успеха День 2

- ✅ 100% API endpoints работают
- ✅ Ошибки обрабатываются корректно
- ✅ E2E flows завершаются успешно
- ✅ Все интеграционные тесты зелены
- ✅ Задокументированы все сценарии

