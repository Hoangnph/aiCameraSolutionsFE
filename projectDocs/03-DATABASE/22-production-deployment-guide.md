# Hướng dẫn Triển khai Production - AI Camera Counting System

## 📊 Tổng quan

Hướng dẫn này cung cấp quy trình triển khai production hoàn chỉnh cho hệ thống AI Camera Counting, bao gồm các chiến lược deployment, rollback, monitoring và security hardening.

## 🎯 Mục tiêu

- **Zero-Downtime Deployment**: Triển khai không gián đoạn dịch vụ
- **Blue-Green Deployment**: Chiến lược deployment an toàn
- **Canary Deployment**: Triển khai AI model cẩn thận
- **Automated Rollback**: Khôi phục nhanh khi có sự cố
- **Security Hardening**: Tăng cường bảo mật production
- **Monitoring Setup**: Giám sát toàn diện

## 🏗️ Kiến trúc Production

### Production Environment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PRODUCTION ENVIRONMENT                             │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              LOAD BALANCER LAYER                            │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   NGINX     │  │   HAProxy   │  │   Cloud     │  │   CDN       │        │ │
│  │  │   Load      │  │   Load      │  │   Load      │  │   (CloudFlare)│       │ │
│  │  │   Balancer  │  │   Balancer  │  │   Balancer  │  │             │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              BLUE-GREEN DEPLOYMENT                          │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                              BLUE ENVIRONMENT                            │ │ │
│  │  │                                                                         │ │ │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │ │ │
│  │  │  │   Frontend  │  │   beAuth    │  │   beCamera  │  │   WebSocket │    │ │ │
│  │  │  │   (React)   │  │   Service   │  │   Service   │  │   Service   │    │ │ │
│  │  │  │   v1.2.0    │  │   v1.1.5    │  │   v1.3.2    │  │   v1.0.8    │    │ │ │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                    │                                         │ │
│  │                                    ▼                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                              GREEN ENVIRONMENT                           │ │ │
│  │  │                                                                         │ │ │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │ │ │
│  │  │  │   Frontend  │  │   beAuth    │  │   beCamera  │  │   WebSocket │    │ │ │
│  │  │  │   (React)   │  │   Service   │  │   Service   │  │   Service   │    │ │ │
│  │  │  │   v1.2.1    │  │   v1.1.6    │  │   v1.3.3    │  │   v1.0.9    │    │ │ │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │ │ │
│  │  └─────────────────────────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              INFRASTRUCTURE LAYER                           │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Primary   │  │   Cache     │  │   Message   │  │   File      │        │ │
│  │  │   Database  │  │   (Redis)   │  │   Queue     │  │   Storage   │        │ │
│  │  │   (PostgreSQL)│ │   Cluster   │  │   (RabbitMQ)│  │   (S3/MinIO)│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              MONITORING LAYER                               │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Prometheus│  │   Grafana   │  │   ELK Stack │  │   Alerting  │        │ │
│  │  │   (Metrics) │  │   (Dashboard)│  │   (Logging) │  │   (PagerDuty)│       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Quy trình Triển khai

### 1. Pre-Deployment Checklist

#### Environment Preparation
- [ ] **Infrastructure Ready**: Tất cả servers, databases, caches đã sẵn sàng
- [ ] **SSL Certificates**: SSL certificates đã được cấu hình
- [ ] **Domain Configuration**: DNS đã được cấu hình đúng
- [ ] **Monitoring Setup**: Prometheus, Grafana, ELK stack đã sẵn sàng
- [ ] **Backup Strategy**: Backup strategy đã được thiết lập
- [ ] **Security Hardening**: Security policies đã được áp dụng

#### Code Preparation
- [ ] **Code Review**: Tất cả code đã được review và approve
- [ ] **Testing Complete**: Unit tests, integration tests, E2E tests đã pass
- [ ] **Performance Testing**: Load testing đã được thực hiện
- [ ] **Security Scanning**: Security vulnerabilities đã được scan
- [ ] **Docker Images**: Docker images đã được build và test
- [ ] **Configuration**: Environment-specific configurations đã sẵn sàng

### 2. Blue-Green Deployment Strategy

#### Phase 1: Green Environment Setup
```bash
# 1. Deploy to Green Environment
kubectl apply -f k8s/green-environment/

# 2. Verify Green Environment Health
kubectl get pods -n green
kubectl logs -f deployment/beauth-service -n green
kubectl logs -f deployment/becamera-service -n green

# 3. Run Health Checks
./scripts/health-check.sh --environment=green
```

#### Phase 2: Traffic Migration
```bash
# 1. Start with 10% traffic to Green
kubectl patch service load-balancer -p '{"spec":{"selector":{"environment":"green"}}}'

# 2. Monitor metrics for 5 minutes
kubectl port-forward svc/prometheus 9090:9090 -n monitoring

# 3. Gradually increase traffic (25%, 50%, 75%, 100%)
./scripts/traffic-migration.sh --green-percentage=25
./scripts/traffic-migration.sh --green-percentage=50
./scripts/traffic-migration.sh --green-percentage=75
./scripts/traffic-migration.sh --green-percentage=100
```

#### Phase 3: Blue Environment Cleanup
```bash
# 1. Verify Green is stable
./scripts/verify-deployment.sh --environment=green

# 2. Scale down Blue environment
kubectl scale deployment beauth-service --replicas=0 -n blue
kubectl scale deployment becamera-service --replicas=0 -n blue

# 3. Keep Blue for rollback capability
kubectl label namespace blue rollback-version=v1.2.0
```

### 3. Canary Deployment for AI Models

#### AI Model Deployment Strategy
```python
# AI Model Canary Deployment
class AICanaryDeployment:
    def __init__(self):
        self.production_model = "yolo-v8-production"
        self.canary_model = "yolo-v8-canary"
        self.traffic_split = 0.1  # 10% traffic to canary
        
    def deploy_canary(self):
        # 1. Deploy canary model
        self.deploy_model(self.canary_model)
        
        # 2. Route 10% traffic to canary
        self.update_traffic_split(0.1)
        
        # 3. Monitor metrics
        self.monitor_canary_metrics()
        
        # 4. Gradually increase traffic
        for split in [0.25, 0.5, 0.75, 1.0]:
            self.update_traffic_split(split)
            time.sleep(300)  # 5 minutes between increases
            
    def rollback_if_needed(self):
        if self.detected_issues():
            self.rollback_to_production()
```

### 4. Health Check Implementation

#### Application Health Checks
```javascript
// Health Check Endpoints
app.get('/health', async (req, res) => {
  try {
    // Database connectivity check
    await db.query('SELECT 1');
    
    // Redis connectivity check
    await redis.ping();
    
    // External service checks
    await checkExternalServices();
    
    res.status(200).json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: process.env.APP_VERSION,
      uptime: process.uptime()
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Readiness Check
app.get('/ready', async (req, res) => {
  try {
    // Check if application is ready to receive traffic
    const isReady = await checkReadiness();
    
    if (isReady) {
      res.status(200).json({ status: 'ready' });
    } else {
      res.status(503).json({ status: 'not ready' });
    }
  } catch (error) {
    res.status(503).json({ status: 'not ready', error: error.message });
  }
});

// Liveness Check
app.get('/live', (req, res) => {
  res.status(200).json({ status: 'alive' });
});
```

#### Kubernetes Health Checks
```yaml
# Kubernetes Health Check Configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: beauth-service
spec:
  template:
    spec:
      containers:
      - name: beauth-service
        image: beauth:latest
        ports:
        - containerPort: 3000
        livenessProbe:
          httpGet:
            path: /live
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 30
```

## 🔄 Rollback Procedures

### 1. Quick Rollback Strategy

#### Automated Rollback Triggers
```yaml
# Rollback Triggers
rollback_triggers:
  - metric: error_rate
    threshold: 5.0
    window: 5m
    action: rollback
    
  - metric: response_time
    threshold: 2000ms
    window: 5m
    action: rollback
    
  - metric: cpu_usage
    threshold: 90%
    window: 10m
    action: rollback
    
  - metric: memory_usage
    threshold: 95%
    window: 10m
    action: rollback
```

#### Rollback Scripts
```bash
#!/bin/bash
# rollback.sh - Automated Rollback Script

ENVIRONMENT=$1
ROLLBACK_VERSION=$2

echo "Starting rollback to version $ROLLBACK_VERSION in $ENVIRONMENT"

# 1. Stop current deployment
kubectl rollout pause deployment/beauth-service -n $ENVIRONMENT
kubectl rollout pause deployment/becamera-service -n $ENVIRONMENT

# 2. Rollback to previous version
kubectl rollout undo deployment/beauth-service -n $ENVIRONMENT
kubectl rollout undo deployment/becamera-service -n $ENVIRONMENT

# 3. Resume deployment
kubectl rollout resume deployment/beauth-service -n $ENVIRONMENT
kubectl rollout resume deployment/becamera-service -n $ENVIRONMENT

# 4. Verify rollback
kubectl rollout status deployment/beauth-service -n $ENVIRONMENT
kubectl rollout status deployment/becamera-service -n $ENVIRONMENT

# 5. Run health checks
./scripts/health-check.sh --environment=$ENVIRONMENT

echo "Rollback completed successfully"
```

### 2. Database Rollback Strategy

#### Database Migration Rollback
```sql
-- Database Rollback Script
BEGIN;

-- 1. Check current migration version
SELECT version FROM schema_migrations ORDER BY version DESC LIMIT 1;

-- 2. Rollback to previous version
-- Example: Rollback from v1.3.0 to v1.2.0
DELETE FROM schema_migrations WHERE version = '202412190001';

-- 3. Drop new tables/columns
DROP TABLE IF EXISTS new_feature_table;
ALTER TABLE existing_table DROP COLUMN IF EXISTS new_column;

-- 4. Restore old data if needed
-- (Backup restoration procedures)

COMMIT;
```

## 🔒 Security Hardening

### 1. Network Security

#### Firewall Configuration
```bash
# UFW Firewall Configuration
ufw default deny incoming
ufw default allow outgoing

# Allow SSH
ufw allow ssh

# Allow HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Allow specific application ports
ufw allow 3000/tcp  # beAuth Service
ufw allow 8000/tcp  # beCamera Service
ufw allow 5432/tcp  # PostgreSQL
ufw allow 6379/tcp  # Redis
ufw allow 5672/tcp  # RabbitMQ

# Enable firewall
ufw enable
```

#### SSL/TLS Configuration
```nginx
# NGINX SSL Configuration
server {
    listen 443 ssl http2;
    server_name api.aicamera.com;
    
    ssl_certificate /etc/ssl/certs/aicamera.crt;
    ssl_certificate_key /etc/ssl/private/aicamera.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. Application Security

#### Security Headers
```javascript
// Security Headers Configuration
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "wss:", "https:"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"]
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));

// Rate Limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP',
  standardHeaders: true,
  legacyHeaders: false
});

app.use('/api/', limiter);
```

#### Input Validation
```javascript
// Input Validation Middleware
const validateInput = (schema) => {
  return (req, res, next) => {
    const { error } = schema.validate(req.body);
    if (error) {
      return res.status(400).json({
        error: 'Validation Error',
        details: error.details.map(detail => detail.message)
      });
    }
    next();
  };
};

// Joi Validation Schemas
const loginSchema = Joi.object({
  username: Joi.string().alphanum().min(3).max(30).required(),
  password: Joi.string().pattern(new RegExp('^[a-zA-Z0-9]{3,30}$')).required()
});

const cameraConfigSchema = Joi.object({
  cameraId: Joi.string().uuid().required(),
  streamUrl: Joi.string().uri().required(),
  aiModel: Joi.string().valid('yolo-v8', 'ssd-mobilenet').required(),
  confidence: Joi.number().min(0.1).max(1.0).default(0.5)
});

app.post('/api/auth/login', validateInput(loginSchema), authController.login);
app.post('/api/cameras/config', validateInput(cameraConfigSchema), cameraController.updateConfig);
```

## 📊 Monitoring Setup

### 1. Prometheus Configuration

#### Prometheus Config
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'beauth-service'
    static_configs:
      - targets: ['beauth-service:3000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'becamera-service'
    static_configs:
      - targets: ['becamera-service:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'postgresql'
    static_configs:
      - targets: ['postgresql:5432']
    metrics_path: '/metrics'

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
    metrics_path: '/metrics'
```

#### Alert Rules
```yaml
# alert_rules.yml
groups:
  - name: application_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors per second"

      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is {{ $value }} seconds"

      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is {{ $value }}%"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage is {{ $value }}%"
```

### 2. Grafana Dashboards

#### Application Dashboard
```json
{
  "dashboard": {
    "title": "AI Camera Counting - Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "5xx errors"
          }
        ]
      },
      {
        "title": "Active Users",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(active_users_total)",
            "legendFormat": "Active Users"
          }
        ]
      },
      {
        "title": "Camera Streams",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(active_camera_streams)",
            "legendFormat": "Active Streams"
          }
        ]
      },
      {
        "title": "AI Model Performance",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(ai_inference_duration_seconds_sum[5m]) / rate(ai_inference_duration_seconds_count[5m])",
            "legendFormat": "Average Inference Time"
          }
        ]
      }
    ]
  }
}
```

## 🔧 Deployment Scripts

### 1. Main Deployment Script
```bash
#!/bin/bash
# deploy-production.sh

set -e

# Configuration
ENVIRONMENT="production"
VERSION=$1
DEPLOYMENT_STRATEGY=$2  # blue-green, canary, rolling

if [ -z "$VERSION" ]; then
    echo "Usage: $0 <version> [deployment-strategy]"
    exit 1
fi

echo "Starting production deployment for version $VERSION"

# 1. Pre-deployment checks
echo "Running pre-deployment checks..."
./scripts/pre-deployment-check.sh

# 2. Backup current state
echo "Creating backup..."
./scripts/backup-production.sh

# 3. Deploy based on strategy
case $DEPLOYMENT_STRATEGY in
    "blue-green")
        echo "Using Blue-Green deployment strategy..."
        ./scripts/blue-green-deploy.sh $VERSION
        ;;
    "canary")
        echo "Using Canary deployment strategy..."
        ./scripts/canary-deploy.sh $VERSION
        ;;
    "rolling")
        echo "Using Rolling deployment strategy..."
        ./scripts/rolling-deploy.sh $VERSION
        ;;
    *)
        echo "Using default Blue-Green deployment strategy..."
        ./scripts/blue-green-deploy.sh $VERSION
        ;;
esac

# 4. Post-deployment verification
echo "Running post-deployment verification..."
./scripts/post-deployment-check.sh

# 5. Monitoring setup
echo "Setting up monitoring..."
./scripts/setup-monitoring.sh

echo "Production deployment completed successfully!"
```

### 2. Health Check Script
```bash
#!/bin/bash
# health-check.sh

ENVIRONMENT=$1
TIMEOUT=300  # 5 minutes timeout

echo "Running health checks for $ENVIRONMENT environment..."

# Check application health
check_app_health() {
    local service=$1
    local port=$2
    local endpoint=$3
    
    echo "Checking $service health..."
    
    for i in {1..60}; do
        if curl -f -s "http://localhost:$port$endpoint" > /dev/null; then
            echo "$service is healthy"
            return 0
        fi
        
        echo "Waiting for $service to be healthy... ($i/60)"
        sleep 5
    done
    
    echo "$service health check failed"
    return 1
}

# Check database connectivity
check_database() {
    echo "Checking database connectivity..."
    if kubectl exec -n $ENVIRONMENT deployment/postgresql -- pg_isready -U postgres; then
        echo "Database is healthy"
        return 0
    else
        echo "Database health check failed"
        return 1
    fi
}

# Check Redis connectivity
check_redis() {
    echo "Checking Redis connectivity..."
    if kubectl exec -n $ENVIRONMENT deployment/redis -- redis-cli ping; then
        echo "Redis is healthy"
        return 0
    else
        echo "Redis health check failed"
        return 1
    fi
}

# Run all health checks
check_app_health "beAuth" "3000" "/health" || exit 1
check_app_health "beCamera" "8000" "/health" || exit 1
check_database || exit 1
check_redis || exit 1

echo "All health checks passed!"
```

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] **Code Review**: Tất cả code đã được review và approve
- [ ] **Testing**: Unit tests, integration tests, E2E tests đã pass
- [ ] **Performance Testing**: Load testing đã được thực hiện
- [ ] **Security Scanning**: Security vulnerabilities đã được scan
- [ ] **Backup**: Production backup đã được tạo
- [ ] **Monitoring**: Monitoring tools đã được cấu hình
- [ ] **Rollback Plan**: Rollback plan đã được chuẩn bị

### During Deployment
- [ ] **Environment Setup**: Green environment đã được setup
- [ ] **Health Checks**: Tất cả services đã healthy
- [ ] **Traffic Migration**: Traffic đã được migrate từng bước
- [ ] **Monitoring**: Metrics đã được monitor liên tục
- [ ] **Testing**: Smoke tests đã được thực hiện

### Post-Deployment
- [ ] **Verification**: Tất cả functionality đã được verify
- [ ] **Performance**: Performance metrics đã được kiểm tra
- [ ] **Security**: Security checks đã được thực hiện
- [ ] **Documentation**: Deployment documentation đã được cập nhật
- [ ] **Team Notification**: Team đã được thông báo

## 🚨 Emergency Procedures

### 1. Emergency Rollback
```bash
#!/bin/bash
# emergency-rollback.sh

echo "EMERGENCY ROLLBACK INITIATED"

# Immediate traffic switch to Blue
kubectl patch service load-balancer -p '{"spec":{"selector":{"environment":"blue"}}}'

# Scale down Green environment
kubectl scale deployment beauth-service --replicas=0 -n green
kubectl scale deployment becamera-service --replicas=0 -n green

# Verify Blue is healthy
./scripts/health-check.sh --environment=blue

echo "Emergency rollback completed"
```

### 2. Emergency Contact List
- **DevOps Lead**: +84 123 456 789
- **System Administrator**: +84 987 654 321
- **Security Team**: security@aicamera.com
- **On-Call Engineer**: oncall@aicamera.com

---

**Tài liệu này cung cấp hướng dẫn triển khai production hoàn chỉnh cho hệ thống AI Camera Counting. Tất cả các quy trình đã được thiết kế để đảm bảo zero-downtime deployment và khả năng rollback nhanh chóng khi cần thiết.** 