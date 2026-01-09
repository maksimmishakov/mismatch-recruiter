# Phase 8: Advanced Features - Implementation Guide

## Overview
Phase 8 introduces advanced features including:
- Real-time notifications system
- ML-based matching algorithm
- Analytics dashboards
- WebSocket support
- Performance optimizations

## Components Implemented

### 1. Notification Service
**File**: `backend/app/services/notification_service.py`

- NotificationType enum (9 types)
- NotificationPriority enum (4 levels)
- NotificationService class with methods:
  - create_match_notification()
  - create_application_notification()
  - create_job_alert_notification()
  - create_system_notification()

### 2. Advanced Matching Algorithm  
**File**: `backend/app/services/advanced_matching.py`

- AdvancedMatcher class using TF-IDF
- Weight distribution:
  - Skills: 35%
  - Experience: 25%
  - Education: 20%
  - Location: 10%
  - Salary: 10%
- Methods:
  - calculate_match_score()
  - _calculate_text_similarity()
  - _match_experience()
  - _match_education()
  - _match_salary()
  - get_match_level()

### 3. Analytics Dashboard
**File**: `backend/monitoring/grafana/dashboards/main-dashboard.json`

Dashboard panels:
1. Request Rate (req/s)
2. Error Rate (%)
3. Response Time p95 (ms)
4. Active Connections
5. Cache Hit Rate (%)
6. Match Success Rate (%)

## API Endpoints (Phase 8)

### Notifications
- `GET /api/notifications` - List user notifications
- `POST /api/notifications/{id}/read` - Mark as read
- `DELETE /api/notifications/{id}` - Delete notification
- `WebSocket /api/notifications/stream` - Real-time updates

### Analytics
- `GET /api/analytics/dashboard` - Dashboard metrics
- `GET /api/analytics/matches` - Match statistics
- `GET /api/analytics/applications` - Application metrics
- `GET /api/analytics/funnel` - User funnel analysis

### Matching
- `POST /api/matching/calculate` - Calculate match score
- `GET /api/matching/candidates-to-vacancy/{vacancy_id}` - Find candidates
- `GET /api/matching/vacancies-to-candidate/{candidate_id}` - Find jobs

## Database Models (New)

### Notification Model
```python
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(50))
    title = db.Column(db.String(255))
    message = db.Column(db.Text)
    data = db.Column(db.JSON)
    priority = db.Column(db.Integer)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
```

## WebSocket Integration

### Real-time Notifications
```javascript
// Frontend
const socket = new WebSocket('wss://api.mismatch-recruiter.ru/api/notifications/stream?token=XXX');

socket.onmessage = (event) => {
    const notification = JSON.parse(event.data);
    showNotification(notification);
};
```

### Backend Handler
```python
@socketio.on('connect')
def handle_connect():
    emit('response', {'data': 'Connected'})

@socketio.on_error_default
def default_error_handler(e):
    logger.error(f'WebSocket error: {e}')
```

## Performance Optimizations

### Caching Strategy
- Match scores cached for 24 hours
- Analytics data cached for 1 hour
- User preferences cached for 12 hours
- Notification counts cached for 5 minutes

### Database Indexing
```sql
CREATE INDEX idx_notifications_user_read ON notification(user_id, read);
CREATE INDEX idx_matches_score ON match(score DESC);
CREATE INDEX idx_applications_status ON application(status);
```

## Testing Strategy

### Unit Tests
- Test notification creation
- Test matching algorithm
- Test analytics calculations
- Test WebSocket handlers

### Integration Tests
- Test notification delivery
- Test real-time updates
- Test analytics aggregation
- Test matching with real data

### Load Tests
- Simulate 1000 concurrent users
- Test WebSocket scalability
- Test notification throughput
- Monitor response times

## Configuration

### Environment Variables
```bash
# Notifications
NOTIFICATION_QUEUE_SIZE=1000
NOTIFICATION_RETENTION_DAYS=30

# Analytics
ANALYTICS_SAMPLE_RATE=0.1
ANALYTICS_RETENTION_DAYS=90

# WebSocket
WEBSOCKET_PING_INTERVAL=30
WEBSOCKET_MAX_MESSAGE_SIZE=1048576
```

## Metrics to Monitor

### Notification System
- Notifications created per day
- Notification delivery latency (target: <100ms)
- WebSocket connection count
- Notification processing time

### Matching Algorithm
- Average match score
- Calculation time (target: <50ms)
- Cache hit rate (target: >80%)
- TF-IDF vectorization time

### Analytics
- Dashboard load time (target: <500ms)
- Query execution time
- Data freshness
- Storage usage

## Troubleshooting

### High Notification Latency
1. Check Redis connection pool
2. Monitor queue size
3. Check database performance
4. Review WebSocket handlers

### Matching Score Inconsistencies
1. Verify TF-IDF weights
2. Check input data format
3. Review cache invalidation
4. Compare with test data

### Dashboard Performance
1. Check Prometheus scrape interval
2. Review query complexity
3. Optimize Grafana rendering
4. Monitor database queries

## Deployment Checklist

- [ ] Notification service configured
- [ ] Advanced matching algorithm deployed
- [ ] Analytics queries optimized
- [ ] WebSocket handler configured
- [ ] Database models migrated
- [ ] Grafana dashboards imported
- [ ] Redis caching configured
- [ ] Monitoring and alerts set up
- [ ] Performance tests passed
- [ ] Documentation updated

## Timeline
**Duration**: 3-4 days
**Status**: IN PROGRESS

## Next Steps
- Phase 9: Lamoda Integration
- Phase 10: Production Launch
