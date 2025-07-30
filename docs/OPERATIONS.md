# Operations Guide

## Overview

This guide covers day-to-day operations, monitoring, and incident response for the Aegis Event Bus.

## System Architecture

### Components

1. **API Server** (FastAPI)
   - Handles HTTP requests
   - Manages authentication
   - Coordinates agent activities

2. **Database** (PostgreSQL/SQLite)
   - Stores agent registry
   - Manages task queue
   - Tracks system state

3. **MQTT Broker** (Mosquitto)
   - Handles agent communication
   - Manages message routing
   - Ensures message delivery

4. **Monitoring Stack**
   - Prometheus metrics
   - Structured logging
   - Health checks

## Daily Operations

### Health Checks

#### Automated Health Monitoring

1. **API Health Check**
   ```bash
   curl -f http://localhost:8000/healthz
   ```

2. **Comprehensive Health Check**
   ```bash
   curl -f http://localhost:8000/healthz/comprehensive
   ```

3. **Database Health**
   ```bash
   # Check database connectivity
   python -c "from app.db import engine_rw; print('Database OK')"
   ```

4. **MQTT Health**
   ```bash
   # Check MQTT connectivity
   mosquitto_pub -h localhost -p 8883 -t test/health -m "test"
   ```

#### Manual Health Checks

1. **Service Status**
   ```bash
   # Docker
   docker-compose ps
   
   # Kubernetes
   kubectl get pods -n aegis-event-bus
   ```

2. **Log Analysis**
   ```bash
   # Recent errors
   docker-compose logs --tail=100 app | grep ERROR
   
   # Slow requests
   docker-compose logs app | grep "slow_request"
   ```

3. **Resource Usage**
   ```bash
   # System metrics
   curl http://localhost:8000/metrics/system
   
   # Performance metrics
   curl http://localhost:8000/metrics/performance
   ```

### Monitoring Alerts

#### Critical Alerts

1. **Service Down**
   - API server not responding
   - Database connection failed
   - MQTT broker offline

2. **High Error Rate**
   - HTTP 5xx errors > 5%
   - Authentication failures
   - Database connection errors

3. **Resource Exhaustion**
   - CPU usage > 80%
   - Memory usage > 85%
   - Disk space < 10%

#### Warning Alerts

1. **Performance Degradation**
   - Response time > 2 seconds
   - Database query time > 1 second
   - High connection pool usage

2. **Security Issues**
   - Failed authentication attempts
   - Rate limit violations
   - Certificate expiration warnings

### Log Management

#### Log Levels

- **DEBUG**: Detailed debugging information
- **INFO**: General operational messages
- **WARNING**: Potential issues
- **ERROR**: Error conditions
- **CRITICAL**: System failures

#### Log Rotation

```bash
# Configure logrotate
/var/log/aegis/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    postrotate
        systemctl reload aegis-event-bus
    endscript
}
```

#### Log Analysis

1. **Error Patterns**
   ```bash
   # Find common errors
   grep ERROR /var/log/aegis/app.log | cut -d' ' -f4 | sort | uniq -c | sort -nr
   ```

2. **Performance Issues**
   ```bash
   # Find slow requests
   grep "slow_request" /var/log/aegis/app.log
   ```

3. **Security Events**
   ```bash
   # Authentication failures
   grep "auth_failed" /var/log/aegis/app.log
   ```

## Incident Response

### Incident Classification

#### P0 - Critical
- Complete service outage
- Data loss or corruption
- Security breach

#### P1 - High
- Partial service degradation
- Performance issues affecting users
- Database connectivity problems

#### P2 - Medium
- Non-critical feature failures
- Monitoring alerts
- Performance degradation

#### P3 - Low
- Minor bugs
- Documentation updates
- Enhancement requests

### Response Procedures

#### P0/P1 Incident Response

1. **Immediate Actions**
   ```bash
   # Check service status
   docker-compose ps
   
   # Check logs
   docker-compose logs --tail=50 app
   
   # Check health endpoints
   curl -f http://localhost:8000/healthz/comprehensive
   ```

2. **Service Recovery**
   ```bash
   # Restart services
   docker-compose restart app
   
   # Check database
   alembic current
   
   # Verify MQTT
   mosquitto_pub -h localhost -p 8883 -t test/health -m "test"
   ```

3. **Communication**
   - Notify stakeholders
   - Update status page
   - Document incident

#### P2/P3 Incident Response

1. **Investigation**
   - Review logs and metrics
   - Identify root cause
   - Plan resolution

2. **Resolution**
   - Implement fix
   - Test solution
   - Deploy changes

3. **Post-Incident**
   - Document lessons learned
   - Update procedures
   - Monitor for recurrence

### Recovery Procedures

#### Database Recovery

1. **Connection Issues**
   ```bash
   # Check database status
   python -c "from app.db import engine_rw; print('DB OK')"
   
   # Restart database
   docker-compose restart postgres
   ```

2. **Data Corruption**
   ```bash
   # Restore from backup
   python scripts/restore_database.py backup_file.sql
   ```

3. **Migration Issues**
   ```bash
   # Check migration status
   alembic current
   
   # Run migrations
   alembic upgrade head
   ```

#### MQTT Recovery

1. **Connection Issues**
   ```bash
   # Check MQTT status
   mosquitto_pub -h localhost -p 8883 -t test/health -m "test"
   
   # Restart MQTT
   docker-compose restart mosquitto
   ```

2. **Certificate Issues**
   ```bash
   # Check certificate validity
   openssl x509 -in mosquitto/certs/server.crt -text -noout
   
   # Regenerate certificates
   python -m app.cert_manager
   ```

#### Application Recovery

1. **Service Restart**
   ```bash
   # Restart application
   docker-compose restart app
   
   # Check health
   curl -f http://localhost:8000/healthz
   ```

2. **Configuration Issues**
   ```bash
   # Validate configuration
   python -c "from app.config import settings; print('Config OK')"
   
   # Check environment variables
   docker-compose exec app env | grep -E "(DATABASE|MQTT|JWT)"
   ```

## Maintenance Procedures

### Regular Maintenance

#### Weekly Tasks

1. **Security Updates**
   ```bash
   # Update dependencies
   pip install -r requirements.txt --upgrade
   
   # Security scan
   bandit -r app/
   safety check
   ```

2. **Database Maintenance**
   ```bash
   # PostgreSQL
   VACUUM ANALYZE;
   
   # SQLite
   VACUUM;
   ```

3. **Log Cleanup**
   ```bash
   # Remove old logs
   find /var/log/aegis -name "*.log.*" -mtime +30 -delete
   ```

#### Monthly Tasks

1. **Certificate Rotation**
   ```bash
   # Check certificate expiration
   openssl x509 -in mosquitto/certs/server.crt -noout -dates
   
   # Regenerate if needed
   python -m app.cert_manager
   ```

2. **Backup Verification**
   ```bash
   # Test backup restore
   python scripts/disaster_recovery.py --restore test_backup
   ```

3. **Performance Review**
   ```bash
   # Analyze metrics
   curl http://localhost:8000/metrics/performance
   
   # Review slow queries
   grep "slow_request" /var/log/aegis/app.log
   ```

### Emergency Procedures

#### Complete System Failure

1. **Immediate Response**
   ```bash
   # Stop all services
   docker-compose down
   
   # Check system resources
   df -h
   free -h
   top
   ```

2. **Recovery Steps**
   ```bash
   # Restore from backup
   python scripts/disaster_recovery.py --restore latest_backup
   
   # Start services
   docker-compose up -d
   
   # Verify recovery
   curl -f http://localhost:8000/healthz/comprehensive
   ```

#### Data Loss

1. **Assessment**
   ```bash
   # Check database integrity
   python -c "from app.db import engine_rw; print('DB integrity check')"
   ```

2. **Recovery**
   ```bash
   # Restore from backup
   python scripts/restore_database.py backup_file.sql
   
   # Verify data
   python -c "from app.models import Agent, Task; print('Data verification')"
   ```

## Performance Optimization

### Monitoring Performance

1. **Key Metrics**
   - Response time (target: < 500ms)
   - Throughput (requests/second)
   - Error rate (target: < 1%)
   - Resource usage (CPU, memory, disk)

2. **Performance Alerts**
   - Response time > 2 seconds
   - Error rate > 5%
   - CPU usage > 80%
   - Memory usage > 85%

### Optimization Strategies

1. **Database Optimization**
   ```sql
   -- Add indexes
   CREATE INDEX idx_tasks_job_id ON tasks(job_id);
   CREATE INDEX idx_agents_status ON agents(status);
   
   -- Optimize queries
   EXPLAIN ANALYZE SELECT * FROM tasks WHERE job_id = ?;
   ```

2. **Application Optimization**
   ```python
   # Connection pooling
   DB_POOL_SIZE = 20
   DB_MAX_OVERFLOW = 30
   
   # Caching
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def get_agent_info(agent_id):
       # Cached agent lookup
       pass
   ```

3. **Infrastructure Optimization**
   ```bash
   # Load balancing
   nginx -s reload
   
   # Resource allocation
   docker-compose up --scale app=3
   ```

## Security Operations

### Security Monitoring

1. **Access Monitoring**
   ```bash
   # Monitor authentication
   grep "auth" /var/log/aegis/app.log | grep ERROR
   
   # Check rate limiting
   grep "rate_limit" /var/log/aegis/app.log
   ```

2. **Security Scans**
   ```bash
   # Code security
   bandit -r app/
   
   # Dependency security
   safety check
   pip-audit
   ```

3. **Certificate Management**
   ```bash
   # Check certificate expiration
   openssl x509 -in mosquitto/certs/server.crt -noout -dates
   
   # Rotate certificates
   python -m app.cert_manager
   ```

### Incident Response

1. **Security Breach**
   - Isolate affected systems
   - Preserve evidence
   - Notify stakeholders
   - Implement containment

2. **Data Breach**
   - Assess scope
   - Notify authorities
   - Implement remediation
   - Review procedures

## Documentation

### Runbooks

1. **Service Restart**
   ```bash
   # Standard restart procedure
   docker-compose restart app
   sleep 30
   curl -f http://localhost:8000/healthz
   ```

2. **Database Recovery**
   ```bash
   # Database recovery procedure
   python scripts/restore_database.py backup_file.sql
   alembic upgrade head
   ```

3. **Certificate Rotation**
   ```bash
   # Certificate rotation procedure
   python -m app.cert_manager
   docker-compose restart mosquitto
   ```

### Checklists

#### Daily Checklist
- [ ] Health checks pass
- [ ] No critical alerts
- [ ] Logs reviewed
- [ ] Performance metrics normal

#### Weekly Checklist
- [ ] Security updates applied
- [ ] Backups verified
- [ ] Performance review
- [ ] Documentation updated

#### Monthly Checklist
- [ ] Certificate expiration check
- [ ] Disaster recovery test
- [ ] Security audit
- [ ] Capacity planning review

## Support and Escalation

### Support Levels

1. **L1 - Basic Support**
   - Service restart
   - Log analysis
   - Basic troubleshooting

2. **L2 - Advanced Support**
   - Performance optimization
   - Security incidents
   - Complex troubleshooting

3. **L3 - Expert Support**
   - Architecture changes
   - Security breaches
   - Critical incidents

### Escalation Procedures

1. **P0/P1 Incidents**
   - Immediate escalation to L3
   - 24/7 on-call response
   - Stakeholder notification

2. **P2 Incidents**
   - Escalation within 4 hours
   - Business hours response
   - Regular updates

3. **P3 Incidents**
   - Standard support process
   - Next business day response
   - Documentation updates 