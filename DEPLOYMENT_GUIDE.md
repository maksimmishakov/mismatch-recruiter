# Phase 4: Analytics System - Deployment Guide

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Redis (optional, for caching)
- pip and virtualenv

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/maksimmishakov/lamoda-ai-recruiter.git
   cd lamoda-ai-recruiter
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   python -m alembic upgrade head
   ```

6. **Run the application**
   ```bash
   python -m app.main
   # Or with uvicorn
   uvicorn app.main:app --reload
   ```

## Environment Configuration

### Required Variables
```
DATABASE_URL=postgresql://user:password@localhost/lamoda_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
DEBUG=True
LOG_LEVEL=INFO
```

### Analytics Configuration
```
ANALYTICS_ENABLED=True
REPORT_GENERATION_SCHEDULE=daily
REPORT_EXPORT_FORMAT=pdf
MAX_SNAPSHOT_RETENTION_DAYS=90
```

## Database Setup

### Schema Creation
The database schema is automatically created by running migrations:
```bash
alembic upgrade head
```

### Key Tables
- `analytics_snapshots`: Stores analytics data points
- `reports`: Stores generated reports
- `user_preferences`: Stores user dashboard settings

## API Endpoints

### Analytics Routes
- `GET /api/analytics/current` - Current analytics snapshot
- `GET /api/analytics/history` - Historical analytics data
- `GET /api/analytics/export` - Export analytics data

### Report Routes
- `GET /api/reports` - List all reports
- `POST /api/reports/generate` - Generate new report
- `GET /api/reports/{id}/download` - Download report

## Dashboard Access

The analytics dashboard is available at:
- **URL**: `http://localhost:8000/dashboard`
- **Features**: Real-time KPIs, charts, exports

## Monitoring

### Logs
Application logs are stored in `logs/` directory:
- `app.log`: General application logs
- `analytics.log`: Analytics-specific logs
- `error.log`: Error logs

### Metrics
Key metrics to monitor:
- API response times
- Database query performance
- Report generation duration
- Cache hit ratio

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check DATABASE_URL format
   - Verify PostgreSQL is running
   - Check credentials

2. **Dashboard Not Loading**
   - Clear browser cache
   - Check static files path
   - Verify Flask/FastAPI serving static files

3. **Report Generation Fails**
   - Check write permissions on export directory
   - Verify required libraries (reportlab, openpyxl)
   - Check database connectivity

## Backup & Recovery

### Database Backup
```bash
pg_dump lamoda_db > backup.sql
```

### Database Restore
```bash
psql lamoda_db < backup.sql
```

## Security Considerations

1. Always use environment variables for secrets
2. Enable HTTPS in production
3. Implement API rate limiting
4. Regular security updates
5. Restrict dashboard access with authentication

## Performance Tuning

### Database Optimization
- Add indices on frequently queried columns
- Enable query caching
- Regular VACUUM and ANALYZE

### Application Optimization
- Enable Redis caching
- Implement pagination for large datasets
- Optimize report generation queries

## Support

For issues and questions:
- Create an issue on GitHub
- Check documentation
- Review logs for errors
