# 🚀 ПЛАН ДЕЙСТВИЙ - ФАЗА 2 (TEST INFRASTRUCTURE RECOVERY)

**Дата:** 10 января 2026, 14:35 MSK  
**Текущее состояние:** Тесты: 6 passed, 15 failed, 7 warnings, 4 errors  
**Deadline для Demo:** 14 января, 14:00 MSK  
**Времени осталось:** ~72 часа  

---

## 📊 АНАЛИЗ ТЕКУЩЕГО СОСТОЯНИЯ

### ✅ ЧТО ТЫ УЖЕ СДЕЛАЛ

**6 КРИТИЧЕСКИХ ИСПРАВЛЕНИЙ:**
1. ✅ Fixed SQLAlchemy imports в conftest.py (2 места)
2. ✅ Fixed test_models.py imports (from app → from app.database)
3. ✅ Added explicit model imports в app/__init__.py перед db.create_all()
4. ✅ Fixed fixture scope от session → function (CRITICAL)
5. ✅ Improved db_session cleanup и indentation
6. ✅ Удален db.session.close() который вызывал ошибки

**7 НОВЫХ КОММИТОВ:**
- e5e0a66: docs: comprehensive test infrastructure fixes summary
- 30c0c09: fix: remove db.session.close() from db_session
- e8ab246: fix: correct indentation in db_session fixture
- eca6211: CRITICAL FIX - change app fixture scope to function ⭐
- 422b2aa: fix: import models before db.create_all()
- 47ea33f: fix: update test_models candidate name field
- c9f9841: fix: SQLAlchemy import in test_models.py
- b21b0cb: fix: SQLAlchemy import in conftest.py

### ⚠️ ЧТО ОСТАЁТСЯ ПРОБЛЕМНЫМ

```
❌ 15 FAILED tests (root cause: architectural issues beyond simple fixes)
❌ 7 WARNINGS (deprecation warnings, fixture issues)
❌ 4 ERRORS (likely app context issues)

Проблемы:
1. Flask app context не управляется правильно в тестах
2. Fixture design смешивает db sessions и HTTP client
3. Test isolation слабая - data bleeding между тестами
4. Model registration timing issues
5. Password validation failures (bcrypt < 72 bytes)
```

---

## 🎯 СТРАТЕГИЯ СЛЕДУЮЩЕЙ ФАЗЫ

### ФАЗА 2A: ОТЛАДКА ТЕКУЩИХ ОШИБОК (3-4 часа)

#### Шаг 1: Запустить тесты с детальной отладкой

```bash
cd ~/mismatch-recruiter/backend

# Запустить тесты с максимальной verbosity
python -m pytest tests/ -vvv --tb=long --capture=no

# Сохранить вывод для анализа
python -m pytest tests/ -vvv --tb=long 2>&1 | tee test_output.log

# Запустить конкретный упавший тест для отладки
python -m pytest tests/test_api.py::test_register -vvv --tb=long --capture=no
```

#### Шаг 2: Проанализировать ошибки

**Типичные причины ошибок:**

```
ERROR 1: "Flask app not registered with SQLAlchemy"
→ app context не активен во время test_user fixture
→ Решение: Wrap fixtures with app.app_context()

ERROR 2: "no such table: user"
→ Таблицы не созданы перед тестом
→ Решение: Убедиться db.create_all() вызывается в right scope

ERROR 3: "Invalid value for password - too long"
→ bcrypt в passlib имеет лимит 72 байта
→ Решение: Использовать более короткие пароли в тестах

FAILED: test_register
→ Возможно: неверная структура payload, неправильный HTTP response
→ Решение: Проверить JSON structure и endpoint implementation
```

#### Шаг 3: Создать исправления для каждого класса ошибок

**Исправление A: Flask App Context**

```python
# В conftest.py - обновить fixtures чтобы использовать app_context

@pytest.fixture
def test_user(app):
    """Create test user with proper app context."""
    with app.app_context():  # ← ВАЖНО!
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash='short',  # ← Короче 72 символов
            role=UserRole.RECRUITER,
        )
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def test_candidate(app, test_user):
    """Create test candidate with proper app context."""
    with app.app_context():  # ← ВАЖНО!
        candidate = Candidate(
            name='John Doe',
            email='john@example.com',
            skills=['Python'],  # ← Упрощено
            experience_years=3,
            recruiter_id=test_user.id,
        )
        db.session.add(candidate)
        db.session.commit()
        return candidate
```

**Исправление B: Отделить Unit Tests от Integration Tests**

```python
# tests/unit/test_models.py - ТОЛЬКО model tests, БЕЗ HTTP
# tests/integration/test_api.py - ТОЛЬКО API tests with client

# Такая организация помогает понять где реальная проблема
```

---

### ФАЗА 2B: АРХИТЕКТУРНЫЕ УЛУЧШЕНИЯ (4-5 часов)

#### Шаг 4: Реструктурировать Test Fixtures

**Текущая проблема:**
```python
# ❌ ПЛОХО - смешивает concerns
@pytest.fixture
def app():
    app = Flask(__name__)
    db.init_app(app)
    app.register_blueprint(api_bp)
    with app.app_context():
        db.create_all()
    # ... но потом в тестах не гарантировано что context активен
    return app
```

**Правильная архитектура:**
```python
# ✅ ХОРОШО - разделяет concerns

@pytest.fixture(scope='function')
def app():
    """Fresh app for each test."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def db_session(app):
    """Database session fixture."""
    with app.app_context():
        yield db.session
        db.session.rollback()

@pytest.fixture
def client(app):
    """Test client - for integration tests only."""
    return app.test_client()

@pytest.fixture
def user_factory(db_session):
    """Factory for creating test users."""
    def _create_user(username='testuser', email='test@example.com', **kwargs):
        user = User(
            username=username,
            email=email,
            password_hash='short_pw',  # < 72 bytes
            role=UserRole.RECRUITER,
            **kwargs
        )
        db_session.add(user)
        db_session.commit()
        return user
    return _create_user
```

#### Шаг 5: Переорганизовать тесты

```
tests/
├── __init__.py
├── conftest.py (главные fixtures)
├── unit/
│   ├── __init__.py
│   └── test_models.py (ТОЛЬКО model tests)
├── integration/
│   ├── __init__.py
│   ├── test_api.py (API endpoints)
│   ├── test_auth.py (authentication)
│   └── test_crud.py (candidates/jobs)
└── fixtures/
    ├── __init__.py
    └── factories.py (test data factories)
```

#### Шаг 6: Добавить транзакционную изоляцию

```python
# В conftest.py - использовать nested transactions

@pytest.fixture(scope='function')
def db_transaction(app):
    """Transaction-based isolation for tests."""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        session = db.Session(bind=connection)
        
        yield session
        
        session.close()
        transaction.rollback()
        connection.close()
```

---

### ФАЗА 2C: ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ (2-3 часа)

#### Шаг 7: Запустить полный тест-цикл

```bash
# 1. Запустить все тесты
python -m pytest tests/ -v

# 2. Проверить coverage
python -m pytest tests/ --cov=app --cov-report=html

# 3. Запустить отдельно unit и integration
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v

# 4. Целевой результат: ≥ 70% passed tests
```

#### Шаг 8: Создать документацию

```markdown
# PHASE_2_TEST_RECOVERY_COMPLETE.md
- Описать все 6 исправлений в деталях
- Показать до/после для каждого
- Объяснить root causes
- Дать recommendations для других проектов
```

#### Шаг 9: Git Commits

```bash
git add tests/ backend/conftest.py backend/app/__init__.py

git commit -m "refactor: restructure test fixtures and architecture

- Separate unit tests from integration tests
- Add proper Flask app context management
- Implement transaction-based test isolation
- Add test data factories
- Improve test organization

This fixes remaining 15 failed tests by addressing
architectural issues in the test fixture design."

git push origin main
```

---

## 📋 ДЕТАЛЬНЫЙ ПЛАН ДО DEADLINE

### ДЕНЬ 10 января (СЕЙЧАС)
**14:35 - 18:00 MSK (3.5 часа)**

- [ ] 14:35-15:35: Шаг 1-2 (Запустить тесты, анализ ошибок)
- [ ] 15:35-16:35: Шаг 3 (Создать исправления для каждого типа ошибок)
- [ ] 16:35-17:00: Шаг 4 (Реструктурировать fixtures)
- [ ] 17:00-17:30: Начать Шаг 5 (переорганизовать тесты)
- [ ] 17:30-18:00: Git commits, push

**Целевой результат:** 70%+ тесты зелёные, архитектура исправлена

---

### ДЕНЬ 11 января
**10:00 - 18:00 MSK (8 часов)**

- [ ] 10:00-11:00: Завершить Шаг 5-6 (организация, транзакции)
- [ ] 11:00-12:00: Шаг 7 (полный test-цикл)
- [ ] 12:00-13:00: Шаг 8 (документация)
- [ ] 13:00-14:00: Finalize Шаг 9 (commits)
- [ ] 14:00+: **BACKEND ТЕСТЫ 100% ГОТОВЫ** ✅

**Параллельно:**
- Alembic migrations setup
- Staging deployment preparation

---

### ДЕНЬ 12-13 января
**Demo data, integration testing, frontend integration**

---

### ДЕНЬ 14 января, 14:00 MSK
**🎉 DEMO FOR LAMODA**

---

## 🚨 КРИТИЧНЫЕ POINTS

### ⚠️ Password Validation Issue

**Проблема:** bcrypt в passlib имеет максимум 72 байта для пароля

```python
# ❌ НЕПРАВИЛЬНО
password = 'this_is_a_very_long_password_that_exceeds_72_bytes_and_will_fail_with_invalid_password_error_in_bcrypt'

# ✅ ПРАВИЛЬНО
password = 'short_pwd'  # или 'test123'

# Во ВСЕХ тестах используй короткие пароли!
```

### ⚠️ App Context Management

**Проблема:** Тесты могут работать локально но падать в CI/CD

```python
# ❌ НЕПРАВИЛЬНО
def test_something(app):
    user = User(...)  # app context не активен!
    db.session.add(user)

# ✅ ПРАВИЛЬНО
def test_something(app):
    with app.app_context():
        user = User(...)
        db.session.add(user)
        db.session.commit()
```

### ⚠️ Test Data Isolation

**Проблема:** Если один тест создаёт данные, они могут быть видны другому тесту

```python
# Решение: Используй fixture scope='function' для app
# Это гарантирует свежую БД для каждого теста
```

---

## 📈 EXPECTED OUTCOMES

### By End of Day 10
- ✅ 70%+ тесты passing
- ✅ Архитектура исправлена
- ✅ Documentation создана

### By End of Day 11
- ✅ 90%+ тесты passing
- ✅ Backend полностью готов
- ✅ Готово к staging deployment

### By Day 14, 14:00
- ✅ 100% тесты passing (или acceptable failures)
- ✅ Backend работает в production
- ✅ Demo успешен для Lamoda

---

## 💡 KEY PRINCIPLES

1. **Test First, Fix Second** - Запусти тесты, поймись что падает, потом фиксь
2. **Small Commits** - Каждое исправление = один commit
3. **Document Everything** - Для будущих разработчиков (и для себя)
4. **Isolate Problems** - Unit tests отдельно от integration tests
5. **Verify Locally** - Перед push на GitHub запусти тесты локально

---

## 📌 SUMMARY

**Ты на 60% пути к 100% working backend!**

**Твои 6 исправлений решили критические проблемы импортов и fixture scopes.**

**Теперь нужно решить оставшиеся 15 failed tests через:**
- Flask app context management
- Test fixture restructuring
- Transaction-based isolation
- Test data factories
- Better test organization

**Это стандартные архитектурные улучшения которые требуют ~8-10 часов работы.**

**У тебя есть 72 часа до deadline - более чем достаточно!** 💪

---

**ГОТОВ? НАЧИНАЙ С ЭТАПА 1 - ЗАПУСТИ ТЕСТЫ И ПОСМОТРИ ЧТО ПАДАЕТ!**
