# Service Level Agreement (SLA)
## mismatch-recruiter Recruitment Platform

### Effective Date: January 7, 2024

## Service Availability

### Uptime Guarantees
- **99.9% Uptime SLA** (99.99% target)
- Monthly downtime limit: 43 minutes
- Quarterly downtime limit: 2 hours 11 minutes

### Service Level Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Availability | 99.9% | Monthly |
| Response Time (P95) | <200ms | Real-time |
| Response Time (P99) | <500ms | Real-time |
| Error Rate | <0.1% | Daily |
| Data Loss | 0% | Never |

## Incident Response

### Severity Levels

**P1 - Critical**
- Complete service outage
- Data loss occurring
- Response: 15 minutes
- Resolution: 1 hour

**P2 - High**
- Partial service degradation
- API errors >5%
- Response: 30 minutes
- Resolution: 4 hours

**P3 - Medium**
- Minor feature unavailable
- Performance degradation
- Response: 2 hours
- Resolution: 8 hours

**P4 - Low**
- Cosmetic issues
- Documentation needs update
- Response: 1 business day
- Resolution: 5 business days

## Support Hours

- **24/7 Support**: Critical incidents (P1, P2)
- **Business Hours**: Standard support (M-F, 9 AM - 6 PM MSK)
- **Escalation**: Available during business hours

## Maintenance Windows

- **Scheduled Maintenance**: Sunday 2 AM - 4 AM UTC
- **Emergency Maintenance**: As needed with 1 hour notice
- **Excluded from SLA**: During scheduled maintenance

## Credits

If uptime drops below 99.9%, credits are provided:

| Availability | Credit |
|--------------|--------|
| 99.0% - 99.9% | 10% month fee |
| 98.0% - 99.0% | 25% month fee |
| <98.0% | 50% month fee |

