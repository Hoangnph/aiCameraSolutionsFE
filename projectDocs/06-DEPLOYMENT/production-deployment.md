# AI Camera System - Production Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [SSL Certificate Setup](#ssl-certificate-setup)
4. [Database Setup](#database-setup)
5. [Deployment Steps](#deployment-steps)
6. [Monitoring Setup](#monitoring-setup)
7. [Security Hardening](#security-hardening)
8. [Backup Configuration](#backup-configuration)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **CPU**: 4+ cores (8+ recommended for high load)
- **RAM**: 8GB+ (16GB+ recommended)
- **Storage**: 100GB+ SSD
- **Network**: Stable internet connection with static IP
- **OS**: Ubuntu 20.04 LTS or later

### Software Requirements
- Docker 20.10+
- Docker Compose 2.0+
- Git
- Nginx (for reverse proxy)
- Certbot (for SSL certificates)

### Domain and DNS
- Registered domain name
- DNS A record pointing to your server IP
- DNS CNAME records for subdomains (optional)

## Environment Setup

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y docker.io docker-compose git nginx certbot python3-certbot-nginx

# Add user to docker group
sudo usermod -aG docker $USER

# Create project directory
mkdir -p /opt/ai-camera-system
cd /opt/ai-camera-system
```

### 2. Clone Repository

```bash
git clone https://github.com/your-username/ai-camera-system.git .
git checkout main
```

### 3. Environment Configuration

```bash
# Copy environment template
cp env.production .env

# Edit environment variables
nano .env
```

**Required Environment Variables:**
```bash
# Database
DB_PASSWORD=your_secure_db_password_here
DATABASE_URL=postgresql://postgres:your_secure_db_password_here@postgres:5432/people_counting_db

# JWT
JWT_SECRET=your_super_secure_jwt_secret_key_here_minimum_32_characters

# Domain
DOMAIN=your-domain.com
PROTOCOL=https

# Email (for alerts)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here

# Monitoring
GRAFANA_PASSWORD=your_secure_grafana_password_here

# AI Model (if using external service)
AI_MODEL_API_KEY=your_openai_api_key_here
```

## SSL Certificate Setup

### 1. Configure Nginx for Certbot

```bash
# Create nginx configuration
sudo nano /etc/nginx/sites-available/ai-camera-system
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/ai-camera-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 2. Obtain SSL Certificate

```bash
# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### 3. Update Nginx Configuration

```bash
# Copy SSL certificates to project
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/

# Set proper permissions
sudo chown -R $USER:$USER nginx/ssl/
chmod 600 nginx/ssl/*
```

## Database Setup

### 1. Initialize Database

```bash
# Start database services
docker-compose -f docker-compose.prod.yml up -d postgres redis

# Wait for database to be ready
sleep 30

# Run database migrations
docker-compose -f docker-compose.prod.yml exec becamera python src/database/migrate.py

# Seed initial data (optional)
docker-compose -f docker-compose.prod.yml exec becamera python src/database/seed.py
```

### 2. Database Optimization

```sql
-- Connect to PostgreSQL and run optimizations
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -d people_counting_db

-- Create indexes for better performance
CREATE INDEX idx_cameras_status ON cameras(status);
CREATE INDEX idx_counts_camera_id ON counts(camera_id);
CREATE INDEX idx_counts_timestamp ON counts(timestamp);
CREATE INDEX idx_analytics_date ON analytics(date);

-- Optimize PostgreSQL settings
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Reload configuration
SELECT pg_reload_conf();
```

## Deployment Steps

### 1. Build and Deploy

```bash
# Build all services
docker-compose -f docker-compose.prod.yml build

# Deploy all services
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps
```

### 2. Verify Deployment

```bash
# Check health endpoints
curl -f https://your-domain.com/health
curl -f https://your-domain.com/api/v1/auth/health
curl -f https://your-domain.com/api/v1/cameras/health

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 3. Initial Setup

```bash
# Create admin user
curl -X POST https://your-domain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@your-domain.com",
    "password": "SecurePassword123!",
    "name": "Admin User",
    "role": "admin"
  }'
```

## Monitoring Setup

### 1. Access Monitoring Dashboards

- **Grafana**: https://your-domain.com:3001
  - Username: `admin`
  - Password: `your_secure_grafana_password_here`

- **Prometheus**: https://your-domain.com:9090

- **Kibana**: https://your-domain.com:5601

### 2. Configure Alerts

```bash
# Set up email notifications in Grafana
# Go to Alerting > Notification channels
# Add email channel with your SMTP settings
```

### 3. Set up Log Aggregation

```bash
# Configure log shipping to Elasticsearch
# Logs are automatically collected by the ELK stack
```

## Security Hardening

### 1. Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Security Headers

```bash
# Verify security headers are working
curl -I https://your-domain.com
```

### 3. Regular Security Updates

```bash
# Set up automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## Backup Configuration

### 1. Database Backup

```bash
# Create backup script
nano /opt/ai-camera-system/backup-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/opt/ai-camera-system/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="db_backup_$DATE.sql"

# Create backup
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U postgres people_counting_db > "$BACKUP_DIR/$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_DIR/$BACKUP_FILE"

# Remove backups older than 30 days
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

```bash
# Make script executable
chmod +x backup-db.sh

# Add to crontab for daily backups
crontab -e
# Add: 0 2 * * * /opt/ai-camera-system/backup-db.sh
```

### 2. Configuration Backup

```bash
# Backup configuration files
tar -czf config_backup_$(date +%Y%m%d).tar.gz .env nginx/ monitoring/ security/
```

## Troubleshooting

### Common Issues

#### 1. Service Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs [service_name]

# Check resource usage
docker stats

# Restart service
docker-compose -f docker-compose.prod.yml restart [service_name]
```

#### 2. Database Connection Issues

```bash
# Check database status
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U postgres

# Check connection pool
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -c "SELECT * FROM pg_stat_activity;"
```

#### 3. SSL Certificate Issues

```bash
# Check certificate validity
sudo certbot certificates

# Renew certificate manually
sudo certbot renew

# Check nginx configuration
sudo nginx -t
```

#### 4. Performance Issues

```bash
# Check resource usage
htop
docker stats

# Check slow queries
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -c "SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"
```

### Monitoring Commands

```bash
# Check all services health
curl -f https://your-domain.com/health

# Check specific service
curl -f https://your-domain.com/api/v1/cameras/health

# Monitor logs in real-time
docker-compose -f docker-compose.prod.yml logs -f --tail=100

# Check disk usage
df -h

# Check memory usage
free -h
```

### Emergency Procedures

#### 1. Service Recovery

```bash
# Restart all services
docker-compose -f docker-compose.prod.yml restart

# Restart specific service
docker-compose -f docker-compose.prod.yml restart [service_name]
```

#### 2. Database Recovery

```bash
# Restore from backup
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U postgres people_counting_db < backup_file.sql
```

#### 3. Rollback Deployment

```bash
# Rollback to previous version
git checkout [previous_commit]
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

## Maintenance Schedule

### Daily
- Check service health
- Review error logs
- Monitor resource usage

### Weekly
- Review security logs
- Update system packages
- Test backup restoration

### Monthly
- Review performance metrics
- Update SSL certificates
- Security audit
- Capacity planning

### Quarterly
- Full system backup
- Disaster recovery testing
- Security penetration testing
- Performance optimization review

## Support

For technical support:
- **Email**: support@your-domain.com
- **Documentation**: https://your-domain.com/docs
- **Issues**: GitHub Issues page
- **Emergency**: +1-555-EMERGENCY

---

**Last Updated**: December 2024
**Version**: 1.0.0 