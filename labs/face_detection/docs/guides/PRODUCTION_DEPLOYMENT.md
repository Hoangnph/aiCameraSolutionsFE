# Face Detection System - Production Deployment Guide

## 🚀 Overview

This guide provides comprehensive instructions for deploying the Face Detection System to production environments.

## 📋 Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+ recommended)
- **CPU**: 4+ cores
- **RAM**: 8GB+ (16GB recommended)
- **Storage**: 50GB+ SSD
- **Docker**: 20.10+
- **Docker Compose**: 2.0+

### Network Requirements
- **Ports**: 8000 (API), 80/443 (Reverse Proxy)
- **Firewall**: Configure to allow required ports
- **SSL Certificate**: For HTTPS (recommended)

## 🔧 Installation Steps

### 1. Clone Repository
```bash
git clone <repository-url>
cd labs/face_detection
```

### 2. Environment Setup
```bash
# Create environment file
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Build and Deploy
```bash
# Make deployment script executable
chmod +x deploy.sh

# Deploy the application
./deploy.sh deploy
```

## 🐳 Docker Deployment

### Using Docker Compose
```bash
# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Deployment Script
```bash
# Deploy
./deploy.sh deploy

# Check status
./deploy.sh status

# Run tests
./deploy.sh test

# View logs
./deploy.sh logs
```

## 🔒 Security Configuration

### 1. Environment Variables
```bash
# Production environment variables
DEBUG=false
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///./data/metadata.db
CHROMA_DB_PATH=./data/vector_db
UPLOAD_DIR=./uploads
LOG_LEVEL=INFO
```

### 2. Security Headers
Add to your reverse proxy (nginx/apache):
```nginx
# Security headers
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options DENY;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
```

### 3. Rate Limiting
Implement rate limiting in your reverse proxy:
```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

## 📊 Monitoring & Logging

### 1. Health Checks
```bash
# Manual health check
curl -f http://localhost:8000/health

# Automated health check
./manage_resources.sh health
```

### 2. Log Monitoring
```bash
# View application logs
docker-compose logs -f face-detection-api

# View resource management logs
tail -f logs/resource_management.log
```

### 3. Performance Monitoring
```bash
# Run performance tests
python performance_test.py

# Monitor system resources
./manage_resources.sh status
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy Face Detection System

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          python automation_test/run_system_tests.py
          python performance_test.py
          python security_test.py

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          ./deploy.sh deploy
```

## 📈 Scaling Considerations

### 1. Horizontal Scaling
```yaml
# docker-compose.yml with scaling
services:
  face-detection-api:
    deploy:
      replicas: 3
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/face_detection
```

### 2. Database Scaling
- **Development**: SQLite (current)
- **Production**: PostgreSQL with connection pooling
- **Caching**: Redis for session management

### 3. Load Balancing
```nginx
# Nginx load balancer configuration
upstream face_detection {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}
```

## 🛠️ Maintenance

### 1. Backup Strategy
```bash
# Database backup
sqlite3 data/metadata.db ".backup backup/metadata_$(date +%Y%m%d).db"

# Upload files backup
tar -czf backup/uploads_$(date +%Y%m%d).tar.gz uploads/

# Automated backup script
./backup.sh
```

### 2. Update Process
```bash
# Pull latest changes
git pull origin main

# Rebuild and redeploy
./deploy.sh restart

# Run tests after update
./deploy.sh test
```

### 3. Rollback Procedure
```bash
# Rollback to previous version
git checkout <previous-commit>
./deploy.sh restart
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Service Not Starting
```bash
# Check Docker status
docker ps -a

# Check logs
docker-compose logs face-detection-api

# Check resource usage
./manage_resources.sh status
```

#### 2. Performance Issues
```bash
# Run performance tests
python performance_test.py

# Check system resources
docker stats

# Monitor API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health
```

#### 3. Security Issues
```bash
# Run security tests
python security_test.py

# Check for vulnerabilities
docker scan face-detection-system:latest
```

## 📞 Support

### Logs Location
- **Application logs**: `logs/`
- **Docker logs**: `docker-compose logs`
- **Test reports**: `automation_test/reports/`

### Health Check Endpoints
- **Health**: `GET /health`
- **API Docs**: `GET /docs`
- **Root**: `GET /`

### Contact Information
- **Documentation**: See `README.md` and `RESOURCES_README.md`
- **Issues**: Create GitHub issue
- **Support**: Contact development team

## 🎯 Success Metrics

### Performance Targets
- **Response Time**: < 500ms (average)
- **Uptime**: > 99.9%
- **Error Rate**: < 1%
- **Security Score**: > 80%

### Monitoring Checklist
- [ ] Health checks passing
- [ ] Performance within targets
- [ ] Security tests passing
- [ ] Logs being collected
- [ ] Backups running
- [ ] Updates tested

---

**Last Updated**: 2025-07-31
**Version**: 1.0.0
**Status**: Production Ready 