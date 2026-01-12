# LAMODA Recruiter - Полный план деплоймента в Production
## Пошаговое руководство для January 14-15, 2026

---

## ЭТАП 1: ПОВТОРНАЯ ПРОВЕРКА ПОдготовки (13 января, 09:00-10:00)

### ШАГ 1.1: Открыть терминал и проверить git status
```bash
git status
# Ожидаемый результат:
# On branch main
# Your branch is up to date with 'origin/main'
# nothing to commit, working tree clean
```

### ШАГ 1.2: Проверить все обязательные файлы
```bash
ls -1 | grep -E '^(requirements|wsgi|.env.example|.amvera.yaml|docker-compose)'
# Ожидаемые файлы:
# .env.example
# .amvera.yaml
# requirements.txt
# wsgi.py
```

### ШАГ 1.3: Проверить requirements.txt
```bash
cat requirements.txt | head -15
# Навверяются вот депенденси:
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
Flask-CORS==4.0.0
Flask-JWT-Extended==4.4.0
gunicorn==20.1.0
psycopg2-binary==2.9.0
python-dotenv==1.0.0
Werkzeug==2.3.0
jinja2==3.1.2
```

### ШАГ 1.4: Проверить wsgi.py
```bash
cat wsgi.py
# Должно содержать:
from app import create_app
app = create_app()
if __name__ == "__main__":
    app.run()
```

### ШАГ 1.5: Проверить .amvera.yaml
```bash
cat .amvera.yaml | head -20
# должно содержать enviroment: production
```

### ОПРЕДЕЛЕННО ПРОВЕРОКи: ✅
