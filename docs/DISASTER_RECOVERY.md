# Disaster Recovery & Business Continuity Plan

## Recovery Time Objectives (RTO)

| Component | RTO | RPO |
|-----------|-----|-----|
| Database | 15 min | 5 min |
| Application | 5 min | N/A |
| Frontend | 5 min | N/A |
| Full Stack | 20 min | 5 min |

## Backup Strategy

### Database Backups
```bash
# Daily backups at 2 AM UTC
0 2 * * * /scripts/backup-database.sh

# Weekly full backup
0 0 * * 0 /scripts/full-backup.sh

# Retention: 30 days
```

### Application Backup
- Git repository as primary backup
- Docker image registry for container snapshots
- Configuration files backed up to secure storage

### Backup Storage
- Primary: Yandex Cloud Storage
- Secondary: GitHub Releases
- Encryption: AES-256

## Disaster Recovery Procedures

### Database Failure
1. Detect failure via health checks
2. Trigger automated failover to standby
3. Restore from backup if needed
4. Validate data integrity
5. Update DNS/load balancer
6. Notify stakeholders

### Application Failure
1. Kubernetes automatically restarts pod
2. Service mesh routes to healthy instances
3. If critical: deploy from backup image
4. Monitor logs for issues
5. Rollback if necessary

### Complete Outage
1. Failover to disaster recovery site
2. Restore database from latest backup
3. Deploy application from backup
4. Verify all services operational
5. Perform full system test

## Testing
- Monthly DR drills
- Quarterly full failover tests
- Annual comprehensive test

## Contact
- On-Call: +7 (915) XXX-XXXX
- Escalation: manager@company.ru
