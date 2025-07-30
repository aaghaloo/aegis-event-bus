# Deployment Guide

## Overview

This guide covers deploying the Aegis Event Bus in various environments, from development to production.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (for production)
- MQTT broker (Mosquitto)

## Environment Setup

### Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/aaghaloo/aegis-event-bus.git
   cd aegis-event-bus
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t aegis-event-bus .
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Check service status**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

### Production Deployment

#### Using Docker Compose

1. **Create production environment file**
   ```bash
   cp .env.example .env.production
   # Edit with production values
   ```

2. **Deploy with Docker Compose**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

#### Using Kubernetes

1. **Create namespace**
   ```bash
   kubectl create namespace aegis-event-bus
   ```

2. **Apply Kubernetes manifests**
   ```bash
   kubectl apply -f k8s/
   ```

3. **Check deployment status**
   ```bash
   kubectl get pods -n aegis-event-bus
   kubectl get services -n aegis-event-bus
   ```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | `sqlite:///eventbus.db` | No |
| `MQTT_HOST` | MQTT broker hostname | `localhost` | Yes |
| `MQTT_PORT` | MQTT broker port | `8883` | Yes |
| `JWT_SECRET_KEY` | JWT signing key | Auto-generated | No |
| `DEBUG` | Enable debug mode | `False` | No |

### Security Configuration

1. **Generate secure JWT secret**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Set up SSL certificates**
   ```bash
   # Generate self-signed certificates for development
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
   ```

3. **Configure firewall rules**
   ```bash
   # Allow necessary ports
   ufw allow 8000/tcp  # API
   ufw allow 8883/tcp  # MQTT
   ufw allow 5432/tcp  # PostgreSQL
   ```

## Monitoring and Observability

### Health Checks

- **API Health**: `GET /healthz`
- **Comprehensive Health**: `GET /healthz/comprehensive`
- **Metrics**: `GET /metrics/prometheus`

### Logging

The application uses structured logging with the following levels:
- `INFO`: Normal operations
- `WARNING`: Potential issues
- `ERROR`: Errors that need attention
- `CRITICAL`: System failures

### Metrics

Prometheus metrics are available at `/metrics/prometheus`:
- HTTP request metrics
- Database connection metrics
- Task and agent metrics
- System resource usage

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Check `DATABASE_URL` configuration
   - Verify database server is running
   - Check network connectivity

2. **MQTT connection errors**
   - Verify MQTT broker is running
   - Check certificate configuration
   - Validate hostname and port

3. **Authentication issues**
   - Verify JWT secret key
   - Check user credentials
   - Validate token expiration

### Debug Mode

Enable debug mode for detailed logging:
```bash
export DEBUG=true
uvicorn app.main:app --reload
```

### Log Analysis

View application logs:
```bash
# Docker
docker-compose logs -f app

# Kubernetes
kubectl logs -f deployment/aegis-event-bus -n aegis-event-bus
```

## Backup and Recovery

### Automated Backups

1. **Schedule database backups**
   ```bash
   # Add to crontab
   0 2 * * * /path/to/scripts/backup_database.py
   ```

2. **Full system backups**
   ```bash
   # Weekly full backup
   0 3 * * 0 /path/to/scripts/disaster_recovery.py --backup
   ```

### Recovery Procedures

1. **Database restore**
   ```bash
   python scripts/restore_database.py backup_file.sql
   ```

2. **Full system restore**
   ```bash
   python scripts/disaster_recovery.py --restore backup_directory
   ```

## Security Best Practices

1. **Use environment variables** for sensitive configuration
2. **Enable HTTPS** in production
3. **Regular security updates** for dependencies
4. **Monitor access logs** for suspicious activity
5. **Implement rate limiting** to prevent abuse
6. **Use strong passwords** and rotate regularly
7. **Enable security scanning** in CI/CD pipeline

## Performance Tuning

### Database Optimization

1. **Connection pooling**
   ```python
   # In app/config.py
   DB_POOL_SIZE = 20
   DB_MAX_OVERFLOW = 30
   DB_POOL_TIMEOUT = 30
   ```

2. **Query optimization**
   - Use database indexes
   - Monitor slow queries
   - Implement caching where appropriate

### Application Optimization

1. **Worker processes**
   ```bash
   uvicorn app.main:app --workers 4
   ```

2. **Memory management**
   - Monitor memory usage
   - Implement garbage collection tuning
   - Use connection pooling

## Scaling

### Horizontal Scaling

1. **Load balancer configuration**
   ```nginx
   upstream aegis_backend {
       server 127.0.0.1:8000;
       server 127.0.0.1:8001;
       server 127.0.0.1:8002;
   }
   ```

2. **Database scaling**
   - Read replicas for read-heavy workloads
   - Connection pooling
   - Query optimization

### Vertical Scaling

1. **Resource allocation**
   - Increase CPU and memory
   - Optimize garbage collection
   - Tune database parameters

## Maintenance

### Regular Tasks

1. **Security updates**
   ```bash
   pip install -r requirements.txt --upgrade
   docker-compose pull
   ```

2. **Log rotation**
   ```bash
   # Configure logrotate
   /var/log/aegis/*.log {
       daily
       rotate 30
       compress
       delaycompress
       missingok
       notifempty
   }
   ```

3. **Database maintenance**
   ```bash
   # PostgreSQL
   VACUUM ANALYZE;
   
   # SQLite
   VACUUM;
   ```

### Monitoring Alerts

Set up alerts for:
- High CPU/memory usage
- Database connection errors
- MQTT connectivity issues
- High error rates
- Certificate expiration

## Support

For issues and questions:
- Check the troubleshooting section
- Review application logs
- Consult the security policy
- Contact the development team 