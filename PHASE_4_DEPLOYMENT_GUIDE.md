# Phase 4: Analytics Deployment Guide

## Deployment Checklist

### Pre-Deployment Validation
- [ ] All tests passing (analytics_service_tests.py)
- [ ] Code coverage > 90%
- [ ] Analytics service integrated in app/main.py
- [ ] Database migrations completed
- [ ] Environment variables configured
- [ ] API documentation updated

### Deployment Steps

1. **Database Preparation**
   - Verify database connectivity
   - Confirm all models loaded (Job, Candidate, MatchResult)
   - Check indices for performance

2. **Application Setup**
   - Pull latest changes from master
   - Install dependencies: `pip install -r requirements.txt`
   - Run migrations if needed

3. **Service Activation**
   - Start analytics service daemon
   - Verify cache layer operational
   - Check logging configuration

4. **API Validation**
   ```bash
   curl http://localhost:8000/api/v1/analytics/recruitment-metrics
   curl http://localhost:8000/api/v1/analytics/job-analytics
   curl http://localhost:8000/api/v1/analytics/candidate-analytics
   curl http://localhost:8000/api/v1/analytics/match-performance
   ```

5. **Monitoring Setup**
   - Configure performance metrics dashboards
   - Set up alert thresholds
   - Enable comprehensive logging

## Production Configuration

### Environment Variables
```
ANALYTICS_CACHE_TTL=3600
ANALYTICS_BATCH_SIZE=1000
ANALYTICS_EXPORT_MAX_RECORDS=50000
LOG_LEVEL=INFO
```

### Performance Tuning
- Database connection pooling: 10 connections
- Query timeout: 30 seconds
- Cache expiration: 1 hour
- Maximum concurrent requests: 100

## Rollback Procedure

1. Stop analytics service
2. Revert to previous application version
3. Clear analytics cache
4. Restart application with rollback commit

## Monitoring & Alerts

### Key Metrics to Monitor
- API response time (target: < 100ms)
- Database query latency
- Cache hit rate (target: > 80%)
- Error rate (target: < 0.1%)
- Concurrent active requests

### Alert Thresholds
- Response time > 500ms: Warning
- Response time > 1000ms: Critical
- Error rate > 1%: Critical
- Database connections > 8: Warning

## Support & Troubleshooting

### Common Issues

**Issue**: Analytics endpoints returning 500 errors
- Check database connectivity
- Verify all required models are imported
- Check error logs in /logs directory

**Issue**: Slow query performance
- Check database indices
- Review query optimization
- Increase cache TTL if applicable

**Issue**: Cache invalidation failures
- Restart cache service
- Clear cache manually if needed
- Check Redis/cache backend status
