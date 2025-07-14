# Production Monitoring & Observability - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này trình bày chiến lược monitoring và observability toàn diện cho hệ thống AI Camera Counting trong môi trường production.

## 🎯 Mục tiêu Monitoring

- **Real-time Visibility**: Giám sát real-time tất cả components
- **Proactive Alerting**: Phát hiện sự cố trước khi ảnh hưởng users
- **Performance Optimization**: Tối ưu hóa hiệu năng dựa trên metrics
- **Capacity Planning**: Lập kế hoạch mở rộng dựa trên trends

## 🏗️ Monitoring Architecture

### Overall Monitoring Stack

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              MONITORING ARCHITECTURE                            │
│                                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Database  │  │   Cache     │  │   Queue     │  │   Application│            │
│  │   Metrics   │  │   Metrics   │  │   Metrics   │  │   Metrics   │            │
│  │             │  │             │  │             │  │             │            │
│  │ • PostgreSQL│  │ • Redis     │  │ • RabbitMQ  │  │ • Node.js   │            │
│  │ • pg_exporter│  │ • redis_exporter│  │ • rabbitmq_exporter│  │ • Custom    │            │
│  │ • Custom    │  │ • INFO      │  │ • Management│  │ • Metrics   │            │
│  │   Metrics   │  │ • MEMORY    │  │ • API       │  │ • Health    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘            │
│         │                   │                   │                   │            │
│         └───────────────────┼───────────────────┼───────────────────┘            │
│                             │                   │                               │
│                             ▼                   ▼                               │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PROMETHEUS CLUSTER                             │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Prometheus│  │   Prometheus│  │   Prometheus│  │   Prometheus│        │ │
│  │  │   Server 1  │  │   Server 2  │  │   Server 3  │  │   Server 4  │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Metrics   │  │ • Metrics   │  │ • Metrics   │  │ • Metrics   │        │ │
│  │  │   Storage   │  │   Storage   │  │   Storage   │  │   Storage   │        │ │
│  │  │ • Query     │  │ • Query     │  │ • Query     │  │ • Query     │        │ │
│  │  │   Engine    │  │   Engine    │  │   Engine    │  │   Engine    │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              VISUALIZATION LAYER                            │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Grafana   │  │   Grafana   │  │   Grafana   │  │   Grafana   │        │ │
│  │  │   Dashboard │  │   Alerts    │  │   Reports   │  │   API       │        │ │
│  │  │             │  │             │  │             │  │             │        │ │
│  │  │ • Database  │  │ • Alert     │  │ • Scheduled │  │ • REST API  │        │ │
│  │  │   Overview  │  │   Rules     │  │ • Reports   │  │ • Metrics   │        │ │
│  │  │ • Performance│  │ • Notifications│  │ • Export    │  │ • Queries   │        │ │
│  │  │ • Health    │  │ • Escalation│  │ • Custom    │  │ • Dashboards│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📊 Key Metrics & KPIs

### Database Metrics

#### Performance Metrics
```sql
-- Connection Metrics
SELECT 
    count(*) as total_connections,
    count(*) FILTER (WHERE state = 'active') as active_connections,
    count(*) FILTER (WHERE state = 'idle') as idle_connections
FROM pg_stat_activity;

-- Query Performance Metrics
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;

-- Replication Lag
SELECT 
    client_addr,
    state,
    pg_wal_lsn_diff(sent_lsn, replay_lsn) as lag_bytes
FROM pg_stat_replication;
```

#### Health Metrics
```sql
-- Database Size
SELECT 
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database;

-- Table Sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Cache Metrics

#### Redis Performance Metrics
```bash
# Memory Usage
redis-cli info memory

# Performance Stats
redis-cli info stats

# Client Connections
redis-cli info clients

# Replication Info
redis-cli info replication
```

#### Key Cache Metrics
- **Hit Ratio**: `keyspace_hits / (keyspace_hits + keyspace_misses)`
- **Memory Usage**: `used_memory / maxmemory`
- **Connection Count**: `connected_clients`
- **Command Rate**: `total_commands_processed / uptime_in_seconds`
- **Eviction Rate**: `evicted_keys / uptime_in_seconds`

### Queue Metrics

#### RabbitMQ Performance Metrics
```bash
# Queue Status
rabbitmqctl list_queues name messages consumers

# Connection Status
rabbitmqctl list_connections

# Channel Status
rabbitmqctl list_channels
```

#### Key Queue Metrics
- **Queue Depth**: Number of messages in queue
- **Consumer Count**: Number of active consumers
- **Message Rate**: Messages per second
- **Acknowledgment Rate**: Messages acknowledged per second
- **Error Rate**: Failed message processing rate

## 🚨 Alert Configuration

### Database Alerts

#### Critical Alerts
```yaml
# Critical Database Alerts
alerts:
  - name: "Database Connection Pool Exhausted"
    condition: "pg_stat_activity_total > 180"
    severity: "critical"
    notification: ["email", "slack", "pagerduty"]
    
  - name: "Database Replication Lag High"
    condition: "pg_replication_lag_seconds > 60"
    severity: "critical"
    notification: ["email", "slack", "pagerduty"]
    
  - name: "Database Disk Space Low"
    condition: "pg_database_size_bytes / pg_database_max_size_bytes > 0.9"
    severity: "critical"
    notification: ["email", "slack", "pagerduty"]
```

#### Warning Alerts
```yaml
# Warning Database Alerts
alerts:
  - name: "High CPU Usage"
    condition: "cpu_usage_percent > 80"
    severity: "warning"
    notification: ["email", "slack"]
    
  - name: "High Memory Usage"
    condition: "memory_usage_percent > 85"
    severity: "warning"
    notification: ["email", "slack"]
    
  - name: "Long Running Queries"
    condition: "pg_stat_activity_max_duration > 300"
    severity: "warning"
    notification: ["email", "slack"]
```

### Cache Alerts

#### Redis Alerts
```yaml
# Redis Cache Alerts
alerts:
  - name: "Redis Memory Usage High"
    condition: "redis_memory_used_bytes / redis_memory_max_bytes > 0.9"
    severity: "critical"
    notification: ["email", "slack", "pagerduty"]
    
  - name: "Redis Hit Ratio Low"
    condition: "redis_hit_ratio < 0.8"
    severity: "warning"
    notification: ["email", "slack"]
    
  - name: "Redis Connection Count High"
    condition: "redis_connected_clients > 1000"
    severity: "warning"
    notification: ["email", "slack"]
```

### Queue Alerts

#### RabbitMQ Alerts
```yaml
# RabbitMQ Queue Alerts
alerts:
  - name: "Queue Depth High"
    condition: "rabbitmq_queue_messages > 10000"
    severity: "critical"
    notification: ["email", "slack", "pagerduty"]
    
  - name: "No Active Consumers"
    condition: "rabbitmq_queue_consumers == 0"
    severity: "critical"
    notification: ["email", "slack", "pagerduty"]
    
  - name: "Message Processing Rate Low"
    condition: "rabbitmq_queue_messages_delivered_total < 100"
    severity: "warning"
    notification: ["email", "slack"]
```

## 📋 Logging Strategy

### Database Logging

#### PostgreSQL Log Configuration
```conf
# postgresql.conf
log_destination = 'csvlog'
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_rotation_age = 1d
log_rotation_size = 100MB
log_min_duration_statement = 1000
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_error_verbosity = verbose
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
```

#### Log Analysis Queries
```sql
-- Slow Query Analysis
SELECT 
    log_time,
    user_name,
    database_name,
    application_name,
    client_addr,
    duration,
    message
FROM postgres_log 
WHERE duration > 1000
ORDER BY duration DESC;

-- Error Analysis
SELECT 
    log_time,
    user_name,
    database_name,
    message
FROM postgres_log 
WHERE log_level = 'ERROR'
ORDER BY log_time DESC;
```

### Cache Logging

#### Redis Log Configuration
```conf
# redis.conf
loglevel notice
logfile /var/log/redis/redis-server.log
syslog-enabled yes
syslog-ident redis
slowlog-log-slower-than 10000
slowlog-max-len 128
```

### Queue Logging

#### RabbitMQ Log Configuration
```conf
# rabbitmq.conf
log.console = true
log.console.level = info
log.file = true
log.file.level = info
log.file.rotation.date = $D0
log.file.rotation.size = 10485760
```

## 🔧 Implementation Guidelines

### Prometheus Configuration

#### Database Exporter Setup
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'postgresql'
    static_configs:
      - targets: ['postgres-exporter:9187']
    metrics_path: /metrics
    scrape_interval: 30s
    
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
    metrics_path: /metrics
    scrape_interval: 30s
    
  - job_name: 'rabbitmq'
    static_configs:
      - targets: ['rabbitmq-exporter:9419']
    metrics_path: /metrics
    scrape_interval: 30s
```

#### Custom Metrics Collection
```python
# Custom Database Metrics Collector
import psycopg2
from prometheus_client import Gauge, Counter, Histogram

# Define metrics
db_connections = Gauge('db_connections_total', 'Total database connections')
db_query_duration = Histogram('db_query_duration_seconds', 'Database query duration')
db_errors = Counter('db_errors_total', 'Total database errors')

def collect_metrics():
    try:
        conn = psycopg2.connect("dbname=test user=postgres password=secret")
        cursor = conn.cursor()
        
        # Collect connection metrics
        cursor.execute("SELECT count(*) FROM pg_stat_activity")
        connections = cursor.fetchone()[0]
        db_connections.set(connections)
        
    except Exception as e:
        db_errors.inc()
        print(f"Error collecting metrics: {e}")
    finally:
        if conn:
            conn.close()
```

## 📊 Dashboard Configuration

### Database Dashboard

#### Overview Dashboard
```yaml
# Grafana Dashboard Configuration
dashboard:
  title: "Database Overview"
  panels:
    - title: "Connection Pool"
      type: "graph"
      metrics:
        - "pg_stat_activity_total"
        - "pg_stat_activity_active"
        - "pg_stat_activity_idle"
    
    - title: "Query Performance"
      type: "graph"
      metrics:
        - "pg_stat_statements_total_time"
        - "pg_stat_statements_mean_time"
        - "pg_stat_statements_calls"
    
    - title: "Database Size"
      type: "stat"
      metrics:
        - "pg_database_size_bytes"
    
    - title: "Replication Lag"
      type: "graph"
      metrics:
        - "pg_replication_lag_bytes"
        - "pg_replication_lag_seconds"
```

### Cache Dashboard

#### Redis Overview Dashboard
```yaml
# Redis Monitoring Dashboard
dashboard:
  title: "Redis Overview"
  panels:
    - title: "Memory Usage"
      type: "graph"
      metrics:
        - "redis_memory_used_bytes"
        - "redis_memory_max_bytes"
        - "redis_memory_peak_bytes"
    
    - title: "Hit/Miss Ratio"
      type: "graph"
      metrics:
        - "redis_keyspace_hits_total"
        - "redis_keyspace_misses_total"
        - "redis_hit_ratio"
    
    - title: "Connection Count"
      type: "stat"
      metrics:
        - "redis_connected_clients"
```

### Queue Dashboard

#### RabbitMQ Overview Dashboard
```yaml
# RabbitMQ Monitoring Dashboard
dashboard:
  title: "Queue Overview"
  panels:
    - title: "Queue Depth"
      type: "graph"
      metrics:
        - "rabbitmq_queue_messages"
        - "rabbitmq_queue_messages_ready"
        - "rabbitmq_queue_messages_unacknowledged"
    
    - title: "Message Rate"
      type: "graph"
      metrics:
        - "rabbitmq_queue_messages_published_total"
        - "rabbitmq_queue_messages_delivered_total"
        - "rabbitmq_queue_messages_acknowledged_total"
    
    - title: "Consumer Count"
      type: "stat"
      metrics:
        - "rabbitmq_queue_consumers"
```

## 📊 Reporting & Analytics

### Automated Reports

#### Daily Health Report
```python
# Daily Health Report Generator
def generate_daily_report():
    # Collect metrics
    metrics = {
        'database_connections': get_db_connections(),
        'cache_hit_ratio': get_cache_hit_ratio(),
        'queue_depth': get_queue_depth(),
        'error_rate': get_error_rate(),
        'response_time': get_avg_response_time()
    }
    
    # Generate report
    report = f"""
    Daily Health Report - {datetime.now().strftime('%Y-%m-%d')}
    
    Database Metrics:
    - Total Connections: {metrics['database_connections']}
    - Cache Hit Ratio: {metrics['cache_hit_ratio']:.2%}
    - Queue Depth: {metrics['queue_depth']}
    - Error Rate: {metrics['error_rate']:.2%}
    - Avg Response Time: {metrics['response_time']}ms
    
    Recommendations:
    {generate_recommendations(metrics)}
    """
    
    # Send report
    send_email_report(report)
```

### Performance Analytics

#### Trend Analysis
```sql
-- Performance Trend Analysis
WITH daily_metrics AS (
    SELECT 
        DATE(timestamp) as date,
        AVG(response_time) as avg_response_time,
        COUNT(*) as total_requests,
        COUNT(*) FILTER (WHERE status_code >= 400) as error_count
    FROM api_requests 
    WHERE timestamp >= NOW() - INTERVAL '30 days'
    GROUP BY DATE(timestamp)
)
SELECT 
    date,
    avg_response_time,
    total_requests,
    error_count,
    (error_count::float / total_requests) as error_rate
FROM daily_metrics
ORDER BY date DESC;
```

---

**Tài liệu này cung cấp framework hoàn chỉnh cho monitoring và observability trong môi trường production, đảm bảo khả năng giám sát, phát hiện sự cố và tối ưu hóa hiệu năng hệ thống.** 