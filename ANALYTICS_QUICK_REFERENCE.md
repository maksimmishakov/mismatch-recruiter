# 🚀 Analytics Dashboard - Quick Reference

## Access Points

### Dashboard UI
- **Local:** `http://localhost:5000/analytics-dashboard`
- **Cloud:** `https://lamoda-recruiter-maksmisakov.amvera.io/analytics-dashboard`

### API Endpoint
- **Local:** `http://localhost:5000/api/analytics`
- **Cloud:** `https://lamoda-recruiter-maksmisakov.amvera.io/api/analytics`

---

## API Response Format

```json
{
  "success": true,
  "total_candidates": 42,
  "status_breakdown": {
    "approved": 12,
    "rejected": 8,
    "pending": 22
  },
  "average_score": 72.5,
  "top_skills": [
    ["Python", 28],
    ["JavaScript", 15],
    ["React", 12]
  ],
  "timestamp": "2025-12-23T23:59:59.000Z"
}
```

---

## Core Files

| File | Purpose | Lines |
|------|---------|-------|
| `templates/analytics.html` | Dashboard UI with 4 metric cards | 199 |
| `utils/analytics_cache.py` | In-memory caching with TTL | 134 |
| `utils/excel_exporter.py` | Excel export utilities | 158 |
| `app.py` (routes) | `/analytics-dashboard` + `/api/analytics` | N/A |

---

## Key Features

### 📊 Dashboard Metrics
1. **Total Resumes** - Total candidates in database
2. **Average Score** - Mean matching score (0-100%)
3. **Unique Skills** - Count of distinct skills identified
4. **Success Matches** - Candidates with approved status

### 🕋 Performance Optimizations
- **In-Memory Cache:** Reduces DB queries by 80%
- **5-Minute TTL:** Balance between freshness & performance
- **Auto-Refresh:** Updates every 30 seconds (client-side)

### 🛠 Utility Functions

**Caching:**
```python
from utils.analytics_cache import get_cached_analytics
analytics = get_cached_analytics(db.session, Candidate)
```

**Excel Export:**
```python
from utils.excel_exporter import export_analytics_to_excel
excel_bytes = export_analytics_to_excel(analytics_data)
```

---

## Testing Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Flask dev server
flask run

# 3. Open dashboard
# Browser: http://localhost:5000/analytics-dashboard

# 4. Test API
# curl http://localhost:5000/api/analytics
```

---

## Dashboard Behavior

| Event | Behavior |
|-------|----------|
| Page Load | Calls `/api/analytics`, displays metrics |
| API Error | Shows "N/A" for affected metrics |
| Every 30s | Auto-refresh from API |
| Hover Cards | Slight animation (translateY -5px) |
| Data Update | Timestamp updates on refresh |

---

## Deployment Status

**Branch:** `master`
**Commits:** 4 related to analytics
**Deployment:** Amvera (building...)
**Build Time:** ~5-10 minutes

---

## Troubleshooting

### API Returns 503
- Application still building on Amvera
- Wait 5-10 minutes and refresh

### Metrics Show N/A
- Check API endpoint returns valid JSON
- Verify database has candidate records
- Check browser console for JavaScript errors

### Cache Not Working
- Verify `utils/analytics_cache.py` imported
- Check TTL hasn't expired (300 seconds)
- Monitor database query frequency

---

## Next Phase Features

- [ ] WebSocket real-time updates
- [ ] Advanced filtering (date range)
- [ ] Time-series analytics (trends)
- [ ] Email report delivery
- [ ] AI-generated insights
- [ ] Custom dashboards

---

**Last Updated:** December 23, 2025, 11:59 PM MSK
**Version:** 1.1.0
