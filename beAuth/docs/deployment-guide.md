# Deployment Guide - Authentication Service

## Tổng quan

Hướng dẫn triển khai Backend Authentication Service lên các môi trường khác nhau, từ development đến production.

## Môi trường triển khai

### 1. Development Environment
- **Purpose**: Phát triển và testing
- **Database**: PostgreSQL local
- **Port**: 3001
- **Log Level**: debug

### 2. Staging Environment
- **Purpose**: Testing trước production
- **Database**: PostgreSQL staging server
- **Port**: 3001
- **Log Level**: info

### 3. Production Environment
- **Purpose**: Live system
- **Database**: PostgreSQL production cluster
- **Port**: 3001
- **Log Level**: warn

## Prerequisites

### System Requirements

#### Minimum Requirements
- **CPU**: 1 core
- **RAM**: 512MB
- **Storage**: 10GB
- **OS**: Ubuntu 20.04+, CentOS 8+, macOS 10.15+

#### Recommended Requirements
- **CPU**: 2 cores
- **RAM**: 2GB
- **Storage**: 50GB SSD
- **OS**: Ubuntu 22.04 LTS

### Software Dependencies

#### Node.js
```bash
# Install Node.js 18+ (LTS)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version  # Should be v18.x.x
npm --version   # Should be 8.x.x
```

#### PostgreSQL
```bash
# Install PostgreSQL 14+
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify installation
psql --version
```

#### Docker (Optional)
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

#### PM2 (Production)
```bash
# Install PM2 globally
npm install -g pm2

# Verify installation
pm2 --version
```

## Local Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd feMain/beAuth
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Configuration
```bash
# Copy environment template
cp env.example .env

# Edit environment variables
nano .env
```

**Development Environment Variables:**
```env
NODE_ENV=development
PORT=3001
API_VERSION=v1

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=people_counting_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_SSL=false

# JWT
JWT_SECRET=your_super_secret_jwt_key_here
JWT_ACCESS_TOKEN_EXPIRY=15m
JWT_REFRESH_TOKEN_EXPIRY=7d

# Security
BCRYPT_ROUNDS=12
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# CORS
CORS_ORIGIN=http://localhost:3000

# Logging
LOG_LEVEL=debug
```

### 4. Database Setup
```bash
# Create database
sudo -u postgres createdb people_counting_db

# Run migrations
npm run migrate

# Seed data (optional)
npm run seed
```

### 5. Start Development Server
```bash
# Start with nodemon (auto-restart)
npm run dev

# Or start normally
npm start
```

### 6. Verify Installation
```bash
# Health check
curl http://localhost:3001/health

# API test
curl http://localhost:3001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123!",
    "confirmPassword": "Test123!"
  }'
```

## Docker Deployment

### 1. Docker Compose Setup

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3001:3001"
    environment:
      - NODE_ENV=production
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=people_counting_db
      - DB_USER=postgres
      - DB_PASSWORD=postgres_password
      - JWT_SECRET=your_jwt_secret_here
    depends_on:
      - postgres
    restart: unless-stopped
    networks:
      - app-network

  postgres:
    image: postgres:14-alpine
    environment:
      - POSTGRES_DB=people_counting_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

### 2. Build and Run
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### 3. Production Docker Setup
```bash
# Create production environment file
cp env.example .env.production

# Build production image
docker build -t auth-service:latest .

# Run with production environment
docker run -d \
  --name auth-service \
  --env-file .env.production \
  -p 3001:3001 \
  --restart unless-stopped \
  auth-service:latest
```

## Production Deployment

### 1. Server Preparation

#### Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git nginx certbot python3-certbot-nginx
```

#### Create Application User
```bash
# Create user
sudo adduser --disabled-password --gecos "" appuser
sudo usermod -aG sudo appuser

# Switch to user
sudo su - appuser
```

#### Install Node.js
```bash
# Install Node.js 18 LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2
sudo npm install -g pm2
```

### 2. Application Deployment

#### Clone and Setup
```bash
# Clone repository
git clone <repository-url> /home/appuser/app
cd /home/appuser/app/beAuth

# Install dependencies
npm install --production

# Create environment file
cp env.example .env.production
nano .env.production
```

#### Production Environment Variables
```env
NODE_ENV=production
PORT=3001
API_VERSION=v1

# Database
DB_HOST=your_db_host
DB_PORT=5432
DB_NAME=people_counting_db
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_SSL=true

# JWT (Use strong secret)
JWT_SECRET=your_very_long_and_secure_jwt_secret_key_here_minimum_32_chars
JWT_ACCESS_TOKEN_EXPIRY=15m
JWT_REFRESH_TOKEN_EXPIRY=7d

# Security
BCRYPT_ROUNDS=12
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100

# CORS
CORS_ORIGIN=https://yourdomain.com

# Logging
LOG_LEVEL=warn
```

### 3. Database Setup

#### PostgreSQL Installation
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql

CREATE DATABASE people_counting_db;
CREATE USER your_db_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE people_counting_db TO your_db_user;
\q
```

#### Run Migrations
```bash
# Set environment
export NODE_ENV=production

# Run migrations
npm run migrate

# Seed data (if needed)
npm run seed
```

### 4. PM2 Process Management

#### Create PM2 Configuration
```bash
# Create ecosystem file
nano ecosystem.config.js
```

**ecosystem.config.js:**
```javascript
module.exports = {
  apps: [{
    name: 'auth-service',
    script: 'src/index.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3001
    },
    env_file: '.env.production',
    log_file: './logs/combined.log',
    error_file: './logs/error.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    max_memory_restart: '1G',
    node_args: '--max-old-space-size=1024',
    watch: false,
    ignore_watch: ['node_modules', 'logs'],
    autorestart: true,
    max_restarts: 10,
    min_uptime: '10s'
  }]
};
```

#### Start Application
```bash
# Create logs directory
mkdir -p logs

# Start with PM2
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Setup PM2 startup script
pm2 startup

# Monitor application
pm2 monit
```

### 5. Nginx Configuration

#### Install and Configure Nginx
```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/auth-service
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    # API Routes
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health Check
    location /health {
        proxy_pass http://localhost:3001/health;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files (if any)
    location / {
        root /var/www/html;
        try_files $uri $uri/ =404;
    }
}
```

#### Enable Site and SSL
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/auth-service /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Test SSL
sudo certbot renew --dry-run
```

### 6. Firewall Configuration
```bash
# Configure UFW
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Check status
sudo ufw status
```

## Monitoring and Logging

### 1. Application Monitoring

#### PM2 Monitoring
```bash
# Monitor processes
pm2 monit

# View logs
pm2 logs auth-service

# Check status
pm2 status
```

#### Health Checks
```bash
# Create health check script
nano health-check.sh
```

**health-check.sh:**
```bash
#!/bin/bash

# Health check URL
HEALTH_URL="https://yourdomain.com/health"

# Check response
response=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $response -eq 200 ]; then
    echo "Service is healthy"
    exit 0
else
    echo "Service is unhealthy (HTTP $response)"
    exit 1
fi
```

```bash
# Make executable
chmod +x health-check.sh

# Add to crontab for monitoring
crontab -e

# Add this line to check every 5 minutes
*/5 * * * * /home/appuser/app/beAuth/health-check.sh
```

### 2. Log Management

#### Log Rotation
```bash
# Install logrotate
sudo apt install logrotate

# Create logrotate configuration
sudo nano /etc/logrotate.d/auth-service
```

**Logrotate Configuration:**
```
/home/appuser/app/beAuth/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 appuser appuser
    postrotate
        pm2 reloadLogs
    endscript
}
```

### 3. Database Monitoring

#### PostgreSQL Monitoring
```bash
# Enable pg_stat_statements
sudo -u postgres psql

CREATE EXTENSION pg_stat_statements;

# Monitor slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

## Backup and Recovery

### 1. Database Backup

#### Automated Backup Script
```bash
# Create backup script
nano backup-db.sh
```

**backup-db.sh:**
```bash
#!/bin/bash

# Configuration
DB_NAME="people_counting_db"
DB_USER="your_db_user"
BACKUP_DIR="/home/appuser/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Create backup
pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/backup_$DATE.sql

# Remove backups older than 30 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup completed: backup_$DATE.sql.gz"
```

```bash
# Make executable
chmod +x backup-db.sh

# Add to crontab (daily backup at 2 AM)
crontab -e

# Add this line
0 2 * * * /home/appuser/app/beAuth/backup-db.sh
```

### 2. Application Backup

#### Code Backup
```bash
# Create application backup script
nano backup-app.sh
```

**backup-app.sh:**
```bash
#!/bin/bash

APP_DIR="/home/appuser/app"
BACKUP_DIR="/home/appuser/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz -C $APP_DIR .

# Remove backups older than 7 days
find $BACKUP_DIR -name "app_backup_*.tar.gz" -mtime +7 -delete

echo "Application backup completed: app_backup_$DATE.tar.gz"
```

### 3. Recovery Procedures

#### Database Recovery
```bash
# Restore database
gunzip -c backup_20240101_120000.sql.gz | psql -U your_db_user -h localhost people_counting_db
```

#### Application Recovery
```bash
# Restore application
tar -xzf app_backup_20240101_120000.tar.gz -C /home/appuser/app/

# Restart application
pm2 restart auth-service
```

## Security Hardening

### 1. System Security

#### Update System Regularly
```bash
# Create update script
nano update-system.sh
```

**update-system.sh:**
```bash
#!/bin/bash

# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Node.js
sudo npm update -g

# Update PM2
sudo npm update -g pm2

# Restart services
pm2 restart all
```

### 2. Application Security

#### Environment Security
```bash
# Secure environment file
chmod 600 .env.production

# Use strong passwords
# Generate secure JWT secret
openssl rand -base64 64
```

#### SSL/TLS Configuration
```bash
# Test SSL configuration
curl -I https://yourdomain.com/health

# Check SSL grade
# Visit: https://www.ssllabs.com/ssltest/
```

### 3. Database Security

#### PostgreSQL Security
```bash
# Edit PostgreSQL configuration
sudo nano /etc/postgresql/14/main/postgresql.conf

# Add security settings
ssl = on
ssl_cert_file = '/etc/ssl/certs/ssl-cert-snakeoil.pem'
ssl_key_file = '/etc/ssl/private/ssl-cert-snakeoil.key'

# Restart PostgreSQL
sudo systemctl restart postgresql
```

## Troubleshooting

### Common Issues

#### 1. Application Won't Start
```bash
# Check logs
pm2 logs auth-service

# Check environment
pm2 env auth-service

# Restart application
pm2 restart auth-service
```

#### 2. Database Connection Issues
```bash
# Test database connection
psql -U your_db_user -h localhost -d people_counting_db

# Check PostgreSQL status
sudo systemctl status postgresql

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

#### 3. Nginx Issues
```bash
# Test Nginx configuration
sudo nginx -t

# Check Nginx status
sudo systemctl status nginx

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

#### 4. SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Renew certificate
sudo certbot renew

# Check certificate expiry
openssl x509 -in /etc/letsencrypt/live/yourdomain.com/cert.pem -text -noout | grep "Not After"
```

### Performance Issues

#### 1. High Memory Usage
```bash
# Check memory usage
free -h

# Check Node.js memory
pm2 monit

# Restart with more memory
pm2 restart auth-service --max-memory-restart 2G
```

#### 2. Slow Database Queries
```bash
# Check slow queries
sudo -u postgres psql -c "
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
"
```

#### 3. High CPU Usage
```bash
# Check CPU usage
htop

# Check Node.js processes
pm2 monit

# Scale application
pm2 scale auth-service 4
```

## Maintenance Schedule

### Daily Tasks
- Monitor application logs
- Check system resources
- Verify backups completed

### Weekly Tasks
- Update system packages
- Review security logs
- Check SSL certificate status
- Analyze slow queries

### Monthly Tasks
- Review and update dependencies
- Check disk space usage
- Review backup retention
- Update SSL certificates

### Quarterly Tasks
- Security audit
- Performance review
- Update Node.js version
- Review monitoring alerts

## Support and Documentation

### Useful Commands
```bash
# Application management
pm2 start ecosystem.config.js
pm2 stop auth-service
pm2 restart auth-service
pm2 delete auth-service
pm2 logs auth-service
pm2 monit

# Database management
sudo -u postgres psql
pg_dump -U your_db_user -h localhost people_counting_db > backup.sql
psql -U your_db_user -h localhost people_counting_db < backup.sql

# System monitoring
htop
df -h
free -h
sudo systemctl status postgresql
sudo systemctl status nginx
```

### Log Locations
- Application logs: `/home/appuser/app/beAuth/logs/`
- PM2 logs: `pm2 logs auth-service`
- Nginx logs: `/var/log/nginx/`
- PostgreSQL logs: `/var/log/postgresql/`
- System logs: `/var/log/syslog`

### Emergency Contacts
- System Administrator: admin@yourdomain.com
- Database Administrator: dba@yourdomain.com
- Security Team: security@yourdomain.com 