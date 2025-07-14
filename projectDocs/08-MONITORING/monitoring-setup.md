# Monitoring Setup Guide
## AI Camera Counting System

### 📊 Tổng quan

Tài liệu này hướng dẫn thiết lập monitoring, logging, và alerting cho hệ thống AI Camera Counting, đảm bảo system reliability và performance visibility.

### 🎯 Mục tiêu
- Đảm bảo system visibility và observability
- Tự động hóa alerting và incident response
- Monitor performance và resource usage
- Track business metrics và user behavior

### 🛠️ Monitoring Architecture

#### System Monitoring Stack
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_USERS_ALLOW_SIGN_UP=false

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.ignored-mount-points=^/(sys|proc|dev|host|etc)($$|/)'

volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:
```

### 📊 Application Monitoring

#### Prometheus Configuration
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'auth-service'
    static_configs:
      - targets: ['beAuth:3000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'camera-service'
    static_configs:
      - targets: ['beCamera:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'frontend'
    static_configs:
      - targets: ['localhost:3000']
    metrics_path: '/metrics'
    scrape_interval: 15s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

#### Alert Rules
```yaml
# monitoring/alert_rules.yml
groups:
  - name: system_alerts
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is above 80% for more than 5 minutes"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is above 85% for more than 5 minutes"

      - alert: HighDiskUsage
        expr: (node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes * 100 > 90
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High disk usage on {{ $labels.instance }}"
          description: "Disk usage is above 90% for more than 5 minutes"

  - name: application_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is above 5% for more than 2 minutes"

      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is above 500ms"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "Service has been down for more than 1 minute"

  - name: business_alerts
    rules:
      - alert: LowCameraCount
        expr: camera_active_count < 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "No active cameras detected"
          description: "No cameras are currently active"

      - alert: HighCountRate
        expr: rate(count_data_total[5m]) > 1000
        for: 5m
        labels:
          severity: info
        annotations:
          summary: "High count rate detected"
          description: "Count rate is above 1000 per 5 minutes"
```

### 📈 Metrics Collection

#### Node.js Application Metrics
```javascript
// beAuth/src/monitoring/metrics.js
const prometheus = require('prom-client');
const express = require('express');

// Create metrics
const httpRequestDurationMicroseconds = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 0.5, 1, 2, 5]
});

const httpRequestsTotal = new prometheus.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});

const activeConnections = new prometheus.Gauge({
  name: 'active_connections',
  help: 'Number of active connections'
});

const userLoginTotal = new prometheus.Counter({
  name: 'user_login_total',
  help: 'Total number of user logins',
  labelNames: ['status']
});

const cameraOperationsTotal = new prometheus.Counter({
  name: 'camera_operations_total',
  help: 'Total number of camera operations',
  labelNames: ['operation', 'status']
});

// Middleware to collect metrics
const metricsMiddleware = (req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    
    httpRequestDurationMicroseconds
      .labels(req.method, req.route?.path || req.path, res.statusCode)
      .observe(duration / 1000);
    
    httpRequestsTotal
      .labels(req.method, req.route?.path || req.path, res.statusCode)
      .inc();
  });
  
  next();
};

// Metrics endpoint
const metricsEndpoint = (req, res) => {
  res.set('Content-Type', prometheus.register.contentType);
  res.end(prometheus.register.metrics());
};

module.exports = {
  httpRequestDurationMicroseconds,
  httpRequestsTotal,
  activeConnections,
  userLoginTotal,
  cameraOperationsTotal,
  metricsMiddleware,
  metricsEndpoint
};
```

#### Python Application Metrics
```python
# beCamera/src/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
import time
from typing import Callable

# Define metrics
http_request_duration = Histogram(
    'http_request_duration_seconds',
    'Duration of HTTP requests in seconds',
    ['method', 'endpoint', 'status_code']
)

http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

camera_operations_total = Counter(
    'camera_operations_total',
    'Total number of camera operations',
    ['operation', 'status']
)

ai_processing_duration = Histogram(
    'ai_processing_duration_seconds',
    'Duration of AI processing in seconds',
    ['model', 'input_type']
)

count_data_total = Counter(
    'count_data_total',
    'Total number of count data records',
    ['camera_id', 'object_type']
)

active_cameras = Gauge(
    'active_cameras',
    'Number of active cameras'
)

processing_queue_size = Gauge(
    'processing_queue_size',
    'Number of items in processing queue'
)

class MetricsMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            start_time = time.time()
            
            # Create a custom send function to capture response
            async def custom_send(message):
                if message['type'] == 'http.response.start':
                    duration = time.time() - start_time
                    
                    # Record metrics
                    http_request_duration.labels(
                        method=scope['method'],
                        endpoint=scope['path'],
                        status_code=message['status']
                    ).observe(duration)
                    
                    http_requests_total.labels(
                        method=scope['method'],
                        endpoint=scope['path'],
                        status_code=message['status']
                    ).inc()
                
                await send(message)
            
            await self.app(scope, receive, custom_send)
        else:
            await self.app(scope, receive, send)

def metrics_endpoint(request: Request) -> Response:
    """Metrics endpoint for Prometheus"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

# Utility functions for recording business metrics
def record_camera_operation(operation: str, status: str):
    """Record camera operation metrics"""
    camera_operations_total.labels(operation=operation, status=status).inc()

def record_ai_processing(model: str, input_type: str, duration: float):
    """Record AI processing metrics"""
    ai_processing_duration.labels(model=model, input_type=input_type).observe(duration)

def record_count_data(camera_id: str, object_type: str):
    """Record count data metrics"""
    count_data_total.labels(camera_id=camera_id, object_type=object_type).inc()

def update_active_cameras(count: int):
    """Update active cameras gauge"""
    active_cameras.set(count)

def update_processing_queue_size(size: int):
    """Update processing queue size gauge"""
    processing_queue_size.set(size)
```

### 📊 Logging Setup

#### Structured Logging
```python
# beCamera/src/logging/logger.py
import logging
import json
from datetime import datetime
from typing import Dict, Any
import traceback

class StructuredLogger:
    def __init__(self, name: str, level: str = 'INFO'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Create JSON formatter
        self.formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        )
        
        # Add handler
        handler = logging.StreamHandler()
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)
    
    def _format_message(self, message: str, **kwargs) -> str:
        """Format message with additional context"""
        log_data = {
            'message': message,
            **kwargs
        }
        return json.dumps(log_data)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(self._format_message(message, **kwargs))
    
    def error(self, message: str, error: Exception = None, **kwargs):
        """Log error message with exception details"""
        error_data = {}
        if error:
            error_data = {
                'error_type': type(error).__name__,
                'error_message': str(error),
                'traceback': traceback.format_exc()
            }
        
        self.logger.error(self._format_message(message, error=error_data, **kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(self._format_message(message, **kwargs))

# Usage example
logger = StructuredLogger('camera_service')

def process_camera_frame(camera_id: str, frame_data: bytes):
    try:
        logger.info('Processing camera frame', camera_id=camera_id, frame_size=len(frame_data))
        
        # Process frame
        result = ai_model.process(frame_data)
        
        logger.info('Frame processed successfully', 
                   camera_id=camera_id, 
                   count=result['count'], 
                   confidence=result['confidence'])
        
        return result
    except Exception as e:
        logger.error('Frame processing failed', 
                    camera_id=camera_id, 
                    error=e)
        raise
```

#### Log Aggregation
```yaml
# docker-compose.logging.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:7.17.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch

  logstash:
    image: docker.elastic.co/logstash/logstash:7.17.0
    ports:
      - "5044:5044"
    volumes:
      - ./monitoring/logstash/pipeline:/usr/share/logstash/pipeline
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:7.17.0
    user: root
    volumes:
      - ./monitoring/filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/log/docker:/var/log/docker:ro
    depends_on:
      - logstash

volumes:
  elasticsearch_data:
```

### 🔔 Alerting Configuration

#### AlertManager Setup
```yaml
# monitoring/alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/YOUR_SLACK_WEBHOOK'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'slack-notifications'
  routes:
    - match:
        severity: critical
      receiver: 'pager-duty-critical'
      continue: true
    - match:
        severity: warning
      receiver: 'slack-notifications'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - channel: '#alerts'
        title: '{{ template "slack.title" . }}'
        text: '{{ template "slack.text" . }}'
        send_resolved: true

  - name: 'pager-duty-critical'
    pagerduty_configs:
      - routing_key: 'YOUR_PAGERDUTY_KEY'
        description: '{{ template "pagerduty.description" . }}'
        severity: '{{ if eq .GroupLabels.severity "critical" }}critical{{ else }}warning{{ end }}'

templates:
  - '/etc/alertmanager/template/*.tmpl'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'dev', 'instance']
```

#### Slack Alert Templates
```yaml
# monitoring/templates/slack.tmpl
{{ define "slack.title" }}
[{{ .Status | toUpper }}{{ if eq .Status "firing" }}:{{ .Alerts.Firing | len }}{{ end }}] {{ .CommonAnnotations.summary }}
{{ end }}

{{ define "slack.text" }}
{{ range .Alerts }}
*Alert:* {{ .Annotations.summary }}
*Description:* {{ .Annotations.description }}
*Severity:* {{ .Labels.severity }}
*Instance:* {{ .Labels.instance }}
*Started:* {{ .StartsAt | since }}
{{ if .EndsAt }}*Ended:* {{ .EndsAt | since }}{{ end }}
{{ end }}
{{ end }}
```

### 📊 Dashboard Configuration

#### Grafana Dashboards
```json
// monitoring/grafana/dashboards/system-overview.json
{
  "dashboard": {
    "id": null,
    "title": "System Overview",
    "tags": ["system", "overview"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "100 - (avg by(instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "{{instance}}"
          }
        ],
        "yAxes": [
          {
            "min": 0,
            "max": 100,
            "label": "CPU %"
          }
        ]
      },
      {
        "id": 2,
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100",
            "legendFormat": "{{instance}}"
          }
        ],
        "yAxes": [
          {
            "min": 0,
            "max": 100,
            "label": "Memory %"
          }
        ]
      },
      {
        "id": 3,
        "title": "HTTP Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{route}}"
          }
        ],
        "yAxes": [
          {
            "min": 0,
            "label": "Requests/sec"
          }
        ]
      },
      {
        "id": 4,
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ],
        "yAxes": [
          {
            "min": 0,
            "label": "Seconds"
          }
        ]
      }
    ]
  }
}
```

### 📋 Monitoring Checklist

#### Setup Phase
- [ ] Install monitoring stack (Prometheus, Grafana, AlertManager)
- [ ] Configure metrics collection
- [ ] Set up logging aggregation
- [ ] Configure alerting rules
- [ ] Create dashboards

#### Configuration
- [ ] Configure application metrics
- [ ] Set up business metrics
- [ ] Configure alert thresholds
- [ ] Set up notification channels
- [ ] Test alerting system

#### Maintenance
- [ ] Monitor system performance
- [ ] Review and adjust thresholds
- [ ] Update dashboards as needed
- [ ] Maintain log retention policies
- [ ] Regular backup of monitoring data

### 🎯 Monitoring Targets

#### System Metrics
- **CPU Usage**: < 80% average, < 95% peak
- **Memory Usage**: < 85% average, < 95% peak
- **Disk Usage**: < 90% average, < 95% peak
- **Network I/O**: Monitor for anomalies

#### Application Metrics
- **Response Time**: < 200ms (95th percentile)
- **Error Rate**: < 1% (5xx errors)
- **Throughput**: > 1000 requests/second
- **Availability**: > 99.9% uptime

#### Business Metrics
- **Active Cameras**: Track number of active cameras
- **Count Accuracy**: Monitor AI model accuracy
- **User Activity**: Track user engagement
- **System Utilization**: Monitor resource usage

---

**Document Version**: 1.0  
**Last Updated**: 2025-07-03  
**Next Review**: 2025-07-10  
**Status**: Ready for Implementation 