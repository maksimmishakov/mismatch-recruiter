# Advanced Features Implementation Guide

## Overview
This document outlines the implementation of Phase 3, 4, and 5 features for the lamoda-ai-recruiter project, enabling comprehensive monitoring, advanced API capabilities, and database optimization.

## PHASE 3: Real-Time Monitoring & Alerting

### 3.1 Prometheus Metrics Service (✅ COMPLETED)
**File**: `services/prometheus_service.py`

Implements:
- Request count tracking by method, endpoint, status
- Request duration histograms (p50, p95, p99)
- Database query monitoring
- Cache hit/miss tracking
- Error rate monitoring
- Active connection tracking
- MetricsService class for integration

### 3.2 Grafana Integration Service
**File**: `services/grafana_service.py`

Implements:
```python
class GrafanaService:
    def create_dashboard(self, dashboard_name: str, panels: list) -> bool
    def create_alert_notification(self, name: str, alert_type: str) -> bool
    def test_datasource(self) -> bool
```

### 3.3 Monitoring Routes
**File**: `app/routes_monitoring.py`

Endpoints:
- `/metrics` - Prometheus metrics endpoint
- `/api/health/detailed` - Detailed health check with Amvera status
- `/api/monitoring/status` - Monitoring system status

### 3.4 Alert Rules Configuration
**File**: `alert_rules.yml`

Alerts:
- HighErrorRate: error rate > 5% (5min)
- HighResponseTime: p95 response > 1s (5min)
- LowCacheHitRatio: cache hits < 70% (10min)
- DatabaseConnectionPoolExhausted: active connections > 18
- HighMemoryUsage: memory > 500MB (5min)

### 3.5 Prometheus Configuration
**File**: `prometheus.yml`

Configuration:
- Global scrape interval: 15 seconds
- Evaluation interval: 15 seconds
- Alertmanager integration
- Rule file loading

### 3.6 Grafana Dashboard
**File**: `grafana-dashboard.json`

Panels:
- Request Rate (requests/sec)
- Error Rate (errors/sec)
- API Response Time (p95 latency)
- Database Query Count
- Cache Hit Ratio
- Active Connections

## PHASE 4: Advanced API Enhancements

### 4.1 GraphQL Layer
**File**: `services/graphql_service.py`

GraphQL Types:
- UserType
- ResumeType
- JobType
- MatchType
- PredictionType
- SubscriptionType

Query Resolvers:
- user(id) -> UserType
- users() -> List[UserType]
- resume(id) -> ResumeType
- resumes() -> List[ResumeType]
- job(id) -> JobType
- jobs() -> List[JobType]
- matches(resume_id) -> List[MatchType]
- predictions(resume_id) -> List[PredictionType]

### 4.2 GraphQL Routes
**File**: `app/graphql_routes.py`

Endpoints:
- `POST /graphql` - GraphQL query endpoint
- `GET /graphql` - GraphQL playground UI

### 4.3 Webhook System
**File**: `services/webhook_service.py`

Implements:
```python
class WebhookService:
    @staticmethod
    def register_webhook(url: str, events: List[str], secret: str) -> bool
    @staticmethod
    def trigger_webhook(event_type: str, payload: Dict) -> bool
    @staticmethod
    def get_event_history(event_type: Optional[str] = None, limit: int = 100) -> List
```

Database Models:
- WebhookEvent: stores event history
- WebhookEndpoint: stores webhook registrations

### 4.4 Webhook Routes
**File**: `app/webhook_routes.py`

Endpoints:
- `POST /api/webhooks/register` - Register webhook
- `GET /api/webhooks/events` - Get event history

## PHASE 5: Database Optimization

### 5.1 Database Optimization Service
**File**: `services/db_optimization_service.py`

Optimizations:
- Connection pooling (20 pool, 40 overflow)
- Query performance logging
- Database indices creation
- Materialized views
- Query result caching
- Slow query detection (> 500ms)

### 5.2 Query Optimization Decorators
**File**: `services/query_optimization_decorator.py`

Decorators:
- `@eager_load_relationships(*relationships)` - Prevent N+1 queries
- `@cache_query_result(ttl=3600)` - Cache query results

### 5.3 Database Indices

Created indices:
```sql
-- User indices
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_user_created ON users(created_at DESC);

-- Resume indices
CREATE INDEX idx_resume_user_id ON resumes(user_id);
CREATE INDEX idx_resume_skills ON resumes USING GIN(skills);
CREATE INDEX idx_resume_created ON resumes(created_at DESC);

-- Job indices
CREATE INDEX idx_job_company ON jobs(company_id);
CREATE INDEX idx_job_created ON jobs(created_at DESC);

-- Match indices
CREATE INDEX idx_match_resume_job ON matches(resume_id, job_id);
CREATE INDEX idx_match_score ON matches(match_score DESC);
```

### 5.4 Materialized Views

Views created:
- `resume_job_matches` - Pre-computed high-quality matches (score > 0.7)
- `user_statistics` - User aggregation statistics

### 5.5 Database Migrations
**File**: `migrations/001_add_database_optimizations.py`

Migration system:
- Up/down functions for schema changes
- Version tracking
- Rollback capability

### 5.6 Migration Runner
**File**: `scripts/run_migrations.py`

Usage:
```bash
python scripts/run_migrations.py
```

## Integration Points

### Monitoring Integration
```python
from services.prometheus_service import MetricsService, get_metrics

# In Flask app initialization
@app.route('/metrics')
def metrics():
    return get_metrics(), 200, {'Content-Type': 'text/plain; charset=utf-8'}
```

### GraphQL Integration
```python
from services.graphql_service import schema
from app.graphql_routes import add_graphql_routes

app = add_graphql_routes(app)
```

### Webhook Integration
```python
from services.webhook_service import WebhookService

# Trigger webhook on event
WebhookService.trigger_webhook('user_signup', {
    'user_id': 123,
    'email': 'user@example.com'
})
```

### Database Optimization
```python
from services.db_optimization_service import DatabaseOptimizationService
from app import db, create_app

app = create_app()
with app.app_context():
    DatabaseOptimizationService.configure_connection_pooling(db)
    DatabaseOptimizationService.setup_query_logging(db)
    DatabaseOptimizationService.add_indices(db)
```

## Performance Metrics

### Expected Improvements
- Request latency: -30% (with caching)
- Database query time: -40% (with indices)
- Cache hit ratio: 70%+ (with optimization)
- Error rate: < 0.5%
- Active connections: < 20

### Monitoring Targets
- CPU usage: < 70%
- Memory usage: < 500MB
- Response time p95: < 1 second
- Error rate: < 1%
- Cache hit ratio: > 70%

## Deployment Checklist

- [ ] Create Prometheus configuration
- [ ] Deploy Grafana dashboards
- [ ] Configure alert rules
- [ ] Create GraphQL endpoints
- [ ] Register webhook system
- [ ] Run database migrations
- [ ] Create database indices
- [ ] Test monitoring endpoints
- [ ] Verify GraphQL playground
- [ ] Load test application

## Next Steps

1. **Monitoring**: Deploy Prometheus + Grafana stack
2. **APIs**: Enable GraphQL queries and webhook subscriptions
3. **Database**: Run migrations and create indices
4. **Testing**: Load test to verify improvements
5. **Alerting**: Configure PagerDuty/Slack integration
