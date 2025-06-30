# Deployment Guide - People Counting Dashboard

## Tổng quan Deployment

Hướng dẫn triển khai hệ thống People Counting Dashboard từ development đến production environment.

## Prerequisites

### 1. System Requirements

#### Frontend (React)
- **Node.js**: 18.x or higher
- **npm**: 9.x or higher
- **Memory**: 2GB RAM minimum
- **Storage**: 10GB free space

#### Backend (Python)
- **Python**: 3.9+ or 3.10+
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 50GB free space
- **GPU**: NVIDIA GPU with CUDA support (optional, for AI processing)

#### Database
- **PostgreSQL**: 14+ or 15+
- **Memory**: 4GB RAM minimum
- **Storage**: 100GB+ (depending on data retention)

#### Infrastructure
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Nginx**: 1.20+
- **SSL Certificate**: Let's Encrypt or commercial

### 2. Development Environment Setup

#### Install Dependencies
```bash
# Frontend
cd feMain
npm install

# Backend
cd ../backend
pip install -r requirements.txt

# Database
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

#### Environment Variables
```bash
# Frontend (.env)
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_ENV=development

# Backend (.env)
DATABASE_URL=postgresql://user:password@localhost:5432/people_counting
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
REDIS_URL=redis://localhost:6379
```

## Development Deployment

### 1. Local Development

#### Start Frontend
```bash
cd feMain
npm start
# Access at http://localhost:3000
```

#### Start Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# Access at http://localhost:8000
```

#### Start Database
```bash
# Using Docker
docker run --name postgres-dev \
  -e POSTGRES_DB=people_counting \
  -e POSTGRES_USER=dev_user \
  -e POSTGRES_PASSWORD=dev_password \
  -p 5432:5432 \
  -d postgres:15

# Or using local PostgreSQL
sudo systemctl start postgresql
sudo -u postgres createdb people_counting
```

### 2. Docker Development

#### Docker Compose Setup
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./feMain
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./feMain:/app
      - /app/node_modules
    environment:
      - REACT_APP_API_URL=http://localhost:8000/api/v1
      - REACT_APP_WS_URL=ws://localhost:8000/ws
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://dev_user:dev_password@postgres:5432/people_counting
      - SECRET_KEY=dev-secret-key
      - JWT_SECRET=dev-jwt-secret
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=people_counting
      - POSTGRES_USER=dev_user
      - POSTGRES_PASSWORD=dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

#### Start Development Environment
```bash
docker-compose -f docker-compose.dev.yml up --build
```

## Production Deployment

### 1. Production Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx         │    │   Load Balancer │    │   CDN           │
│   (Reverse      │    │   (Optional)    │    │   (Optional)    │
│    Proxy)       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│   Frontend      │◄─────────────┘
                        │   (React)       │
                        └─────────────────┘
                                │
                        ┌─────────────────┐
                        │   Backend       │
                        │   (FastAPI)     │
                        └─────────────────┘
                                │
                        ┌─────────────────┐
                        │   Database      │
                        │   (PostgreSQL)  │
                        └─────────────────┘
```

### 2. Production Docker Setup

#### Production Dockerfile (Frontend)
```dockerfile
# feMain/Dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Production Dockerfile (Backend)
```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Production Docker Compose
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
      - frontend_build:/usr/share/nginx/html
    depends_on:
      - frontend
      - backend

  frontend:
    build:
      context: ./feMain
      dockerfile: Dockerfile
    environment:
      - REACT_APP_API_URL=https://api.yourdomain.com/api/v1
      - REACT_APP_WS_URL=wss://api.yourdomain.com/ws
    volumes:
      - frontend_build:/app/build

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://prod_user:prod_password@postgres:5432/people_counting
      - SECRET_KEY=${SECRET_KEY}
      - JWT_SECRET=${JWT_SECRET}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=people_counting
      - POSTGRES_USER=prod_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  backup:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    command: |
      sh -c '
        while true; do
          pg_dump -h postgres -U prod_user people_counting > /backups/backup_$$(date +%Y%m%d_%H%M%S).sql
          sleep 86400
        done
      '

volumes:
  postgres_data:
  redis_data:
  frontend_build:
```

### 3. Nginx Configuration

#### Nginx Config
```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }

    upstream backend {
        server backend:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

    server {
        listen 80;
        server_name yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

        # Frontend
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
            
            # Cache static assets
            location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
                expires 1y;
                add_header Cache-Control "public, immutable";
            }
        }

        # API endpoints
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # WebSocket
        location /ws {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Login rate limiting
        location /api/auth/login {
            limit_req zone=login burst=5 nodelay;
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### 4. Environment Configuration

#### Production Environment Variables
```bash
# .env.production
# Database
DATABASE_URL=postgresql://prod_user:secure_password@postgres:5432/people_counting
DB_PASSWORD=secure_password

# Security
SECRET_KEY=your-super-secure-secret-key-here
JWT_SECRET=your-super-secure-jwt-secret-here

# Redis
REDIS_URL=redis://redis:6379

# External Services
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO

# AI Model
AI_MODEL_PATH=/app/models/ssd_model.pth
CUDA_VISIBLE_DEVICES=0
```

### 5. SSL Certificate Setup

#### Let's Encrypt with Certbot
```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Logging

### 1. Application Monitoring

#### Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'people-counting-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:80']
    metrics_path: '/nginx_status'
```

#### Grafana Dashboard
```json
{
  "dashboard": {
    "title": "People Counting Dashboard",
    "panels": [
      {
        "title": "API Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_request_duration_seconds_sum[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Active Users",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(active_users_total)"
          }
        ]
      }
    ]
  }
}
```

### 2. Logging Configuration

#### Logging Setup
```python
# backend/logging_config.py
import logging
import logging.handlers
import os

def setup_logging():
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler(
                '/var/log/app/app.log',
                maxBytes=10485760,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
```

#### Log Rotation
```bash
# /etc/logrotate.d/people-counting
/var/log/app/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 appuser appuser
    postrotate
        systemctl reload nginx
    endscript
}
```

## Backup and Recovery

### 1. Database Backup

#### Automated Backup Script
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
DB_NAME="people_counting"
DB_USER="prod_user"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
pg_dump -h localhost -U $DB_USER $DB_NAME > $BACKUP_DIR/backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/backup_$DATE.sql

# Remove old backups (keep last 30 days)
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

# Upload to cloud storage (optional)
aws s3 cp $BACKUP_DIR/backup_$DATE.sql.gz s3://your-backup-bucket/
```

#### Backup Cron Job
```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
```

### 2. Disaster Recovery

#### Recovery Script
```bash
#!/bin/bash
# recovery.sh

BACKUP_FILE=$1
DB_NAME="people_counting"
DB_USER="prod_user"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Stop application
docker-compose -f docker-compose.prod.yml stop backend

# Restore database
gunzip -c $BACKUP_FILE | psql -h localhost -U $DB_USER $DB_NAME

# Start application
docker-compose -f docker-compose.prod.yml start backend
```

## Security Hardening

### 1. Network Security

#### Firewall Configuration
```bash
# UFW configuration
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

#### Docker Security
```yaml
# docker-compose.prod.yml (security additions)
services:
  backend:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
      - /var/tmp
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETGID
      - SETUID
```

### 2. Application Security

#### Security Headers
```python
# backend/security.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

def setup_security(app: FastAPI):
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://yourdomain.com"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    # Trusted hosts
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["yourdomain.com", "www.yourdomain.com"]
    )
```

## Performance Optimization

### 1. Database Optimization

#### PostgreSQL Tuning
```sql
-- postgresql.conf optimizations
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
```

#### Index Optimization
```sql
-- Create indexes for common queries
CREATE INDEX CONCURRENTLY idx_count_data_camera_timestamp 
ON count_data(camera_id, timestamp DESC);

CREATE INDEX CONCURRENTLY idx_alerts_unread_created 
ON alerts(created_at DESC) WHERE is_read = false;
```

### 2. Application Optimization

#### Caching Strategy
```python
# backend/cache.py
import redis
from functools import wraps

redis_client = redis.Redis.from_url(os.getenv('REDIS_URL'))

def cache_result(expire_time=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expire_time, json.dumps(result))
            
            return result
        return wrapper
    return decorator
```

## Deployment Checklist

### Pre-deployment
- [ ] All tests passing
- [ ] Security scan completed
- [ ] Performance testing done
- [ ] Backup strategy in place
- [ ] SSL certificates obtained
- [ ] Domain DNS configured
- [ ] Environment variables set
- [ ] Database migrations ready

### Deployment
- [ ] Infrastructure provisioned
- [ ] Docker images built
- [ ] Database initialized
- [ ] Application deployed
- [ ] SSL certificates installed
- [ ] Monitoring configured
- [ ] Backup jobs scheduled
- [ ] Security measures implemented

### Post-deployment
- [ ] Application health check
- [ ] Performance monitoring
- [ ] Error tracking setup
- [ ] User acceptance testing
- [ ] Documentation updated
- [ ] Team training completed
- [ ] Support procedures established

## Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database connectivity
docker exec -it postgres psql -U prod_user -d people_counting -c "SELECT 1;"

# Check database logs
docker logs postgres
```

#### Application Startup Issues
```bash
# Check application logs
docker logs backend

# Check environment variables
docker exec -it backend env | grep -E "(DATABASE|SECRET|JWT)"
```

#### Performance Issues
```bash
# Check resource usage
docker stats

# Check database performance
docker exec -it postgres psql -U prod_user -d people_counting -c "
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;
"
```

### Emergency Procedures

#### Rollback Deployment
```bash
# Rollback to previous version
docker-compose -f docker-compose.prod.yml down
docker tag previous-image:tag current-image:tag
docker-compose -f docker-compose.prod.yml up -d
```

#### Database Recovery
```bash
# Restore from backup
./recovery.sh /backups/backup_20240101_120000.sql.gz
```

#### Emergency Maintenance Mode
```bash
# Enable maintenance mode
echo "MAINTENANCE_MODE=true" >> .env.production
docker-compose -f docker-compose.prod.yml restart nginx
``` 