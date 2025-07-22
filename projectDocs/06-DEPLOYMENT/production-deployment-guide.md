# 🚀 **PRODUCTION DEPLOYMENT GUIDE**
## AI Camera Counting System

### 📅 **Version**: 1.0.0
### 📅 **Last Updated**: 2025-07-18
### 🎯 **Status**: Production Ready

---

## 📋 **PRE-DEPLOYMENT CHECKLIST**

### ✅ **System Requirements**
- [ ] Docker & Docker Compose installed
- [ ] PostgreSQL 13+ database
- [ ] Redis 6+ cache
- [ ] 4GB+ RAM available
- [ ] 10GB+ disk space
- [ ] Network access for RTSP cameras

### ✅ **AI Model Files**
- [ ] `MobileNetSSD_deploy.caffemodel` - AI model file
- [ ] `MobileNetSSD_deploy.prototxt` - Model configuration
- [ ] Files placed in `beCamera/refrenCode/People-Counting-in-Real-Time-master/detector/`

### ✅ **Environment Configuration**
- [ ] Production environment variables set
- [ ] Database credentials configured
- [ ] JWT secrets configured
- [ ] CORS settings updated
- [ ] SSL certificates ready (if needed)

---

## 🏗️ **DEPLOYMENT STEPS**

### **Step 1: Environment Setup**

```bash
# Clone repository
git clone <repository-url>
cd feMain

# Copy environment files
cp env.example env.production

# Edit production environment
nano env.production
```

**Production Environment Variables**:
```env
# Database
POSTGRES_DB=people_counting_db
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=secure_password_here
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# JWT Secrets
JWT_SECRET=your_very_secure_jwt_secret_here
JWT_REFRESH_SECRET=your_very_secure_refresh_secret_here

# API Configuration
API_PORT=3001
CAMERA_API_PORT=3002
WEBSOCKET_PORT=3003
FRONTEND_PORT=3000

# AI Model Configuration
AI_MODEL_PATH=refrenCode/People-Counting-in-Real-Time-master/detector/
AI_CONFIDENCE_THRESHOLD=0.4
AI_SKIP_FRAMES=30

# Worker Pool Configuration
WORKER_POOL_SIZE=4
WORKER_TIMEOUT=30

# Security
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=900
```

### **Step 2: Database Setup**

```bash
# Start database container
docker-compose up -d postgres

# Wait for database to be ready
sleep 10

# Run database migrations
docker-compose exec postgres psql -U postgres -d people_counting_db -f /docker-entrypoint-initdb.d/init.sql

# Create production user
docker-compose exec postgres psql -U postgres -d people_counting_db -c "
INSERT INTO users (username, email, password_hash, role, created_at) 
VALUES ('admin', 'admin@yourdomain.com', '\$2b\$12\$your_hashed_password_here', 'admin', NOW())
ON CONFLICT (username) DO NOTHING;
"
```

### **Step 3: Build and Deploy**

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### **Step 4: Health Check**

```bash
# Test all services
curl http://yourdomain.com:3001/health
curl http://yourdomain.com:3002/health
curl http://yourdomain.com:3000

# Test AI model
curl -X POST http://yourdomain.com:3002/api/v1/test/ai-processing \
  -H "Authorization: Bearer your_jwt_token"

# Test worker pool
curl http://yourdomain.com:3002/api/v1/workers/status \
  -H "Authorization: Bearer your_jwt_token"
```

---

## 🔧 **CONFIGURATION OPTIONS**

### **AI Model Configuration**

```python
# beCamera/src/services/ai_model_service.py
class AIModelService:
    def __init__(self):
        self.confidence_threshold = 0.4  # Adjust for accuracy vs speed
        self.skip_frames = 30  # Process every 30th frame
        self.max_disappeared = 40  # Track objects for 40 frames
        self.max_distance = 50  # Maximum distance for object tracking
```

### **Worker Pool Configuration**

```python
# beCamera/worker_pool.py
class CameraWorkerPool:
    def __init__(self, max_workers: int = 4):  # Adjust based on CPU cores
        self.max_workers = max_workers
        self.task_timeout = 30  # Seconds
        self.retry_attempts = 3
```

### **Database Configuration**

```sql
-- PostgreSQL optimization
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Reload configuration
SELECT pg_reload_conf();
```

---

## 📊 **MONITORING & LOGGING**

### **Service Monitoring**

```bash
# Check service health
docker-compose -f docker-compose.prod.yml ps

# Monitor logs
docker-compose -f docker-compose.prod.yml logs -f beauth
docker-compose -f docker-compose.prod.yml logs -f becamera
docker-compose -f docker-compose.prod.yml logs -f frontend

# Check resource usage
docker stats
```

### **Application Monitoring**

```python
# Health check endpoints
GET /health - Service health
GET /api/v1/workers/status - Worker pool status
GET /api/v1/cameras - Camera list
POST /api/v1/test/ai-processing - AI model test
```

### **Log Management**

```bash
# Configure log rotation
sudo nano /etc/logrotate.d/ai-camera-system

# Log rotation configuration
/var/log/ai-camera/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        docker-compose -f docker-compose.prod.yml restart
    endscript
}
```

---

## 🔒 **SECURITY CONFIGURATION**

### **SSL/TLS Setup**

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/v1/ {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/v1/cameras/ {
        proxy_pass http://localhost:3002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **Firewall Configuration**

```bash
# UFW firewall setup
sudo ufw enable
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp # HTTPS
sudo ufw allow 3000/tcp # Frontend
sudo ufw allow 3001/tcp # beAuth API
sudo ufw allow 3002/tcp # beCamera API
sudo ufw allow 3003/tcp # WebSocket
sudo ufw allow 5432/tcp # PostgreSQL
sudo ufw allow 6379/tcp # Redis
```

### **JWT Security**

```javascript
// JWT configuration
const jwtConfig = {
    accessToken: {
        secret: process.env.JWT_SECRET,
        expiresIn: '15m'  // Short expiration for security
    },
    refreshToken: {
        secret: process.env.JWT_REFRESH_SECRET,
        expiresIn: '7d'   // Longer expiration for refresh
    }
};
```

---

## 📈 **PERFORMANCE OPTIMIZATION**

### **Database Optimization**

```sql
-- Create indexes for better performance
CREATE INDEX idx_cameras_user_id ON cameras(user_id);
CREATE INDEX idx_cameras_status ON cameras(status);
CREATE INDEX idx_count_data_camera_id ON count_data(camera_id);
CREATE INDEX idx_count_data_timestamp ON count_data(timestamp);

-- Analyze table statistics
ANALYZE cameras;
ANALYZE count_data;
ANALYZE users;
```

### **Redis Caching**

```python
# Cache configuration
REDIS_CONFIG = {
    'host': 'redis',
    'port': 6379,
    'db': 0,
    'max_connections': 20,
    'socket_timeout': 5,
    'socket_connect_timeout': 5
}

# Cache keys
CACHE_KEYS = {
    'camera_list': 'cameras:list:{user_id}',
    'camera_status': 'camera:status:{camera_id}',
    'worker_status': 'workers:status',
    'ai_model_status': 'ai:model:status'
}
```

### **Worker Pool Optimization**

```python
# Worker pool tuning
WORKER_CONFIG = {
    'max_workers': 4,  # Adjust based on CPU cores
    'task_timeout': 30,
    'retry_attempts': 3,
    'health_check_interval': 60,
    'max_memory_usage': '512MB'
}
```

---

## 🚨 **TROUBLESHOOTING**

### **Common Issues**

#### **1. AI Model Not Loading**
```bash
# Check model files
ls -la beCamera/refrenCode/People-Counting-in-Real-Time-master/detector/

# Check logs
docker-compose logs becamera | grep "AI model"

# Solution: Ensure model files are present and accessible
```

#### **2. Database Connection Issues**
```bash
# Check database status
docker-compose exec postgres pg_isready

# Check connection logs
docker-compose logs postgres

# Solution: Restart database container
docker-compose restart postgres
```

#### **3. Worker Pool Issues**
```bash
# Check worker status
curl http://localhost:3002/api/v1/workers/status

# Check worker logs
docker-compose logs becamera | grep "worker"

# Solution: Restart beCamera service
docker-compose restart becamera
```

#### **4. Authentication Issues**
```bash
# Check JWT configuration
echo $JWT_SECRET

# Test authentication
curl -X POST http://localhost:3001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Solution: Regenerate JWT secrets
```

### **Performance Issues**

#### **1. Slow AI Processing**
- Increase `skip_frames` value
- Reduce `confidence_threshold`
- Add more workers
- Optimize frame resolution

#### **2. Database Slowdown**
- Add database indexes
- Optimize queries
- Increase database memory
- Use connection pooling

#### **3. Memory Issues**
- Monitor memory usage: `docker stats`
- Increase container memory limits
- Optimize AI model parameters
- Implement garbage collection

---

## 📞 **SUPPORT & MAINTENANCE**

### **Regular Maintenance**

```bash
# Daily health checks
#!/bin/bash
# health_check.sh
curl -f http://localhost:3001/health || echo "beAuth down"
curl -f http://localhost:3002/health || echo "beCamera down"
curl -f http://localhost:3000 || echo "Frontend down"

# Weekly database maintenance
docker-compose exec postgres psql -U postgres -d people_counting_db -c "VACUUM ANALYZE;"

# Monthly log cleanup
find /var/log/ai-camera -name "*.log.*" -mtime +30 -delete
```

### **Backup Strategy**

```bash
# Database backup
docker-compose exec postgres pg_dump -U postgres people_counting_db > backup_$(date +%Y%m%d).sql

# Configuration backup
tar -czf config_backup_$(date +%Y%m%d).tar.gz env.production docker-compose.prod.yml

# AI model backup
tar -czf ai_model_backup_$(date +%Y%m%d).tar.gz beCamera/refrenCode/
```

### **Update Process**

```bash
# Update system
git pull origin main
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Verify update
./health_check.sh
```

---

## 🎯 **DEPLOYMENT VERIFICATION**

### **Post-Deployment Checklist**

- [ ] All services running: `docker-compose ps`
- [ ] Health checks passing: All `/health` endpoints return 200
- [ ] Authentication working: Can login and get JWT token
- [ ] AI model loaded: `/api/v1/test/ai-processing` returns success
- [ ] Worker pool active: `/api/v1/workers/status` shows 4 workers
- [ ] Camera creation works: Can create test camera
- [ ] Database accessible: Can query camera data
- [ ] WebSocket working: Real-time updates functional
- [ ] SSL configured: HTTPS accessible
- [ ] Monitoring active: Logs and metrics available

### **Performance Benchmarks**

- **Response Time**: < 200ms for API calls
- **AI Processing**: < 1s per frame
- **Database Queries**: < 100ms
- **Memory Usage**: < 2GB total
- **CPU Usage**: < 80% under load

---

## 📚 **ADDITIONAL RESOURCES**

- **API Documentation**: `/api/docs` (Swagger UI)
- **System Architecture**: `projectDocs/01-ARCHITECTURE/`
- **Testing Guide**: `projectDocs/07-TESTING/`
- **Troubleshooting**: `taskNow/troubleshooting_guide.md`
- **User Manual**: `projectDocs/04-FRONTEND/`

---

**🎉 CONGRATULATIONS! Your AI Camera Counting System is now production ready!** 