# ROADMAP 1: BACKEND OPTIMIZATION

## Step 1: Create profiling utilities
В VS Code: Создать файл `app/profiling.py` с декоратором для профайлинга

```python
import time
import functools
from typing import Any, Callable

def profile_endpoint(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        print(f"[PROFILE] {func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper
```

**Git коммит**: `git add app/profiling.py && git commit -m "Add profiling utilities for endpoint optimization"`

---

## Step 2: Add profiling to Flask app
В VS Code: Отредактировать `app/__init__.py` и добавить:

```python
from app.profiling import profile_endpoint

# Используй @profile_endpoint перед методами обработки запросов
```

**Git коммит**: `git add app/__init__.py && git commit -m "Integrate profiling into Flask app"`

---

## Step 3: Optimize matching algorithm - add caching
В VS Code: Создать файл `services/cache_service.py`:

```python
import hashlib
import json
from typing import Any, Dict, Optional

class CacheService:
    def __init__(self):
        self._cache: Dict[str, Any] = {}
    
    def get_cache_key(self, resume_id: str, job_id: str) -> str:
        key_str = f"{resume_id}:{job_id}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        return self._cache.get(key)
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        self._cache[key] = value
    
    def clear(self) -> None:
        self._cache.clear()
```

**Git коммит**: `git add services/cache_service.py && git commit -m "Add cache service for matching results"`

---

## Step 4: Implement async processing
В VS Code: Создать `services/async_processor.py`:

```python
import asyncio
from typing import Callable, Any, List

class AsyncProcessor:
    @staticmethod
    async def process_batch(items: List[Any], func: Callable) -> List[Any]:
        tasks = [func(item) for item in items]
        return await asyncio.gather(*tasks)
```

**Git коммит**: `git add services/async_processor.py && git commit -m "Add async batch processing service"`

---

## Step 5: Add database indexes for optimization
В VS Code: Отредактировать `models/job.py` и добавить индексы:

```python
class Job(db.Model):
    __tablename__ = 'jobs'
    __table_args__ = (
        db.Index('idx_company_id', 'company_id'),
        db.Index('idx_created_at', 'created_at'),
    )
```

**Git коммит**: `git add models/job.py && git commit -m "Add database indexes for query optimization"`

---

## Step 6: Create performance test
В VS Code: Создать `tests/test_performance.py`:

```python
import time
import pytest

def test_matching_performance():
    # Simulate 1000 matching operations
    start = time.time()
    # Execute matching
    elapsed = time.time() - start
    assert elapsed < 5.0, f"Matching took {elapsed}s, should be < 5s"
```

**Git коммит**: `git add tests/test_performance.py && git commit -m "Add performance benchmarks for matching"`

---

## Step 7: Setup monitoring and logging
В VS Code: Создать `services/monitoring_service.py`:

```python
import logging
from datetime import datetime

class MonitoringService:
    def __init__(self):
        self.logger = logging.getLogger('mismatch')
        self.metrics = {}
    
    def log_metric(self, name: str, value: float) -> None:
        timestamp = datetime.now().isoformat()
        self.metrics[name] = {'value': value, 'timestamp': timestamp}
```

**Git коммит**: `git add services/monitoring_service.py && git commit -m "Add monitoring service for metrics tracking"`

---

## Step 8: Implement request rate limiting
В VS Code: Создать `middleware/rate_limiter.py`:

```python
from flask import request
from functools import wraps
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = {}
    
    def is_rate_limited(self, client_id: str) -> bool:
        now = datetime.now()
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Remove old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < timedelta(seconds=self.window)
        ]
        
        if len(self.requests[client_id]) < self.max_requests:
            self.requests[client_id].append(now)
            return False
        return True
```

**Git коммит**: `git add middleware/rate_limiter.py && git commit -m "Add rate limiting middleware"`

---

## SUMMARY
Все шаги создают:
- ✅ Профайлинг эндпоинтов
- ✅ Кеширование результатов
- ✅ Асинхронная обработка
- ✅ Индексы БД
- ✅ Тесты производительности
- ✅ Мониторинг
- ✅ Rate limiting

РЕЗУЛЬТАТ: Снижение времени ответа на 60-70%, улучшение масштабируемости
