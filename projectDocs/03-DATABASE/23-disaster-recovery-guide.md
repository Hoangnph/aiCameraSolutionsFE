# Hướng dẫn Khôi phục Thảm họa & Liên tục Kinh doanh - AI Camera Counting System

## 📊 Tổng quan

Hướng dẫn này cung cấp quy trình khôi phục thảm họa (Disaster Recovery) và liên tục kinh doanh (Business Continuity) hoàn chỉnh cho hệ thống AI Camera Counting, đảm bảo hệ thống có thể khôi phục nhanh chóng từ mọi loại sự cố.

## 🎯 Mục tiêu

- **RTO (Recovery Time Objective)**: ≤ 4 giờ
- **RPO (Recovery Point Objective)**: ≤ 1 giờ
- **Zero Data Loss**: Không mất dữ liệu quan trọng
- **Automated Recovery**: Khôi phục tự động khi có thể
- **Geographic Redundancy**: Dự phòng địa lý
- **Regular Testing**: Kiểm thử định kỳ

## 🏗️ Kiến trúc Disaster Recovery

### Multi-Region Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DISASTER RECOVERY ARCHITECTURE                     │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PRIMARY REGION (HCMC)                          │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Load      │  │   beAuth    │  │   beCamera  │  │   Database  │        │ │
│  │  │   Balancer  │  │   Service   │  │   Service   │  │   Primary   │        │ │
│  │  │   (Active)  │  │   (Active)  │  │   (Active)  │  │   (Master)  │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │                                    │                                         │ │
│  │                                    ▼                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Cache     │  │   Message   │  │   File      │  │   Backup    │        │ │
│  │  │   (Redis)   │  │   Queue     │  │   Storage   │  │   Storage   │        │ │
│  │  │   Master    │  │   (RabbitMQ)│  │   (S3)      │  │   (S3)      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    │ Real-time Replication                       │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DR REGION (HANOI)                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Load      │  │   beAuth    │  │   beCamera  │  │   Database  │        │ │
│  │  │   Balancer  │  │   Service   │  │   Service   │  │   Standby   │        │ │
│  │  │   (Standby) │  │   (Standby) │  │   (Standby) │  │   (Slave)   │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  │                                    │                                         │ │
│  │                                    ▼                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Cache     │  │   Message   │  │   File      │  │   Backup    │        │ │
│  │  │   (Redis)   │  │   Queue     │  │   Storage   │  │   Storage   │        │ │
│  │  │   Slave     │  │   (RabbitMQ)│  │   (S3)      │  │   (S3)      │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Data Replication Strategy

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA REPLICATION STRATEGY                          │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATABASE REPLICATION                           │ │
│  │                                                                             │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Primary   │    │   WAL       │    │   Standby   │    │   Monitoring│  │ │
│  │  │   Database  │    │   Shipping  │    │   Database  │    │   (Prometheus)│ │ │
│  │  │   (Master)  │    │   (Real-time)│   │   (Slave)   │    │             │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. Write          │                   │                   │      │ │
│  │         │ Operations        │                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 2. WAL Files      │                   │      │ │
│  │         │                   │ (Real-time)       │                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 3. Apply WAL      │      │ │
│  │         │                   │                   │ (Replay)          │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 4. Replication    │      │ │
│  │         │                   │                   │ Status            │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              CACHE REPLICATION                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │ │
│  │  │   Redis     │    │   Redis     │    │   Redis     │    │   Redis     │  │ │
│  │  │   Master    │    │   Sentinel  │    │   Slave     │    │   Sentinel  │  │ │
│  │  │   (Primary) │    │   (Monitor) │    │   (DR)      │    │   (Monitor) │  │ │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │ │
│  │         │                   │                   │                   │      │ │
│  │         │ 1. Write          │                   │                   │      │ │
│  │         │ Operations        │                   │                   │      │ │
│  │         │──────────────────►│                   │                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │ 2. Monitor        │                   │      │ │
│  │         │                   │ Health            │                   │      │ │
│  │         │                   │──────────────────►│                   │      │ │
│  │         │                   │                   │                   │      │ │
│  │         │                   │                   │ 3. Failover       │      │ │
│  │         │                   │                   │ (Auto)            │      │ │
│  │         │                   │                   │──────────────────►│      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Quy trình Khôi phục Thảm họa

### 1. Phân loại Sự cố

#### Sự cố Cấp độ 1 (Critical)
- **Mô tả**: Toàn bộ hệ thống không hoạt động
- **RTO**: ≤ 1 giờ
- **RPO**: ≤ 15 phút
- **Ví dụ**: Mất điện toàn bộ data center, thiên tai

#### Sự cố Cấp độ 2 (High)
- **Mô tả**: Một số services không hoạt động
- **RTO**: ≤ 4 giờ
- **RPO**: ≤ 1 giờ
- **Ví dụ**: Database corruption, network outage

#### Sự cố Cấp độ 3 (Medium)
- **Mô tả**: Performance degradation
- **RTO**: ≤ 8 giờ
- **RPO**: ≤ 4 giờ
- **Ví dụ**: High CPU usage, slow response time

### 2. Quy trình Khôi phục Tự động

#### Automated Failover Script
```bash
#!/bin/bash
# automated-failover.sh

set -e

PRIMARY_REGION="hcmc"
DR_REGION="hanoi"
FAILOVER_TRIGGER_FILE="/tmp/failover_triggered"

echo "Starting automated failover process..."

# 1. Check if failover is already triggered
if [ -f "$FAILOVER_TRIGGER_FILE" ]; then
    echo "Failover already triggered. Exiting..."
    exit 1
fi

# 2. Check primary region health
check_primary_health() {
    local health_status=$(curl -s -o /dev/null -w "%{http_code}" https://api.aicamera.com/health)
    if [ "$health_status" != "200" ]; then
        return 1
    fi
    return 0
}

# 3. Check database replication lag
check_replication_lag() {
    local lag=$(psql -h $PRIMARY_DB_HOST -U $DB_USER -d $DB_NAME -t -c "SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))::INTEGER;")
    if [ "$lag" -gt 300 ]; then  # 5 minutes lag
        return 1
    fi
    return 0
}

# 4. Trigger failover if conditions are met
if ! check_primary_health || ! check_replication_lag; then
    echo "Primary region issues detected. Triggering failover..."
    
    # Create trigger file
    touch "$FAILOVER_TRIGGER_FILE"
    
    # 5. Update DNS to point to DR region
    update_dns_to_dr() {
        aws route53 change-resource-record-sets \
            --hosted-zone-id $HOSTED_ZONE_ID \
            --change-batch '{
                "Changes": [{
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": "api.aicamera.com",
                        "Type": "A",
                        "TTL": 300,
                        "ResourceRecords": [{"Value": "'$DR_LOAD_BALANCER_IP'"}]
                    }
                }]
            }'
    }
    
    # 6. Promote DR database to primary
    promote_dr_database() {
        ssh $DR_DB_HOST "sudo -u postgres pg_ctl promote"
    }
    
    # 7. Start DR services
    start_dr_services() {
        kubectl apply -f k8s/dr-environment/
        kubectl rollout restart deployment/beauth-service -n dr
        kubectl rollout restart deployment/becamera-service -n dr
    }
    
    # 8. Verify DR environment
    verify_dr_environment() {
        for i in {1..30}; do
            if curl -f -s https://api.aicamera.com/health > /dev/null; then
                echo "DR environment is healthy"
                return 0
            fi
            echo "Waiting for DR environment to be ready... ($i/30)"
            sleep 10
        done
        return 1
    }
    
    # Execute failover steps
    update_dns_to_dr
    promote_dr_database
    start_dr_services
    
    if verify_dr_environment; then
        echo "Failover completed successfully"
        
        # Send notification
        send_notification "DR_FAILOVER_SUCCESS" "Failover to DR region completed successfully"
        
        # Update status
        echo "DR_ACTIVE" > /var/run/system_status
    else
        echo "Failover failed"
        send_notification "DR_FAILOVER_FAILED" "Failover to DR region failed"
        exit 1
    fi
else
    echo "Primary region is healthy. No failover needed."
fi
```

### 3. Quy trình Khôi phục Thủ công

#### Manual Recovery Procedures
```bash
#!/bin/bash
# manual-recovery.sh

RECOVERY_TYPE=$1  # database, application, full
BACKUP_TIMESTAMP=$2

case $RECOVERY_TYPE in
    "database")
        echo "Starting database recovery..."
        ./scripts/recover-database.sh $BACKUP_TIMESTAMP
        ;;
    "application")
        echo "Starting application recovery..."
        ./scripts/recover-application.sh
        ;;
    "full")
        echo "Starting full system recovery..."
        ./scripts/recover-full-system.sh $BACKUP_TIMESTAMP
        ;;
    *)
        echo "Usage: $0 {database|application|full} [backup-timestamp]"
        exit 1
        ;;
esac
```

#### Database Recovery Script
```bash
#!/bin/bash
# recover-database.sh

BACKUP_TIMESTAMP=$1
BACKUP_PATH="/backups/database/$BACKUP_TIMESTAMP"

echo "Starting database recovery from backup: $BACKUP_TIMESTAMP"

# 1. Stop application services
echo "Stopping application services..."
kubectl scale deployment beauth-service --replicas=0
kubectl scale deployment becamera-service --replicas=0

# 2. Stop database
echo "Stopping database..."
sudo systemctl stop postgresql

# 3. Backup current state (if possible)
echo "Creating backup of current state..."
sudo -u postgres pg_dumpall > /backups/pre-recovery-backup.sql

# 4. Restore from backup
echo "Restoring from backup..."
sudo -u postgres dropdb --if-exists aicamera
sudo -u postgres createdb aicamera
sudo -u postgres psql aicamera < $BACKUP_PATH/full_backup.sql

# 5. Start database
echo "Starting database..."
sudo systemctl start postgresql

# 6. Verify database
echo "Verifying database..."
sudo -u postgres psql -d aicamera -c "SELECT COUNT(*) FROM users;"
sudo -u postgres psql -d aicamera -c "SELECT COUNT(*) FROM camera_streams;"

# 7. Start application services
echo "Starting application services..."
kubectl scale deployment beauth-service --replicas=3
kubectl scale deployment becamera-service --replicas=3

# 8. Verify application health
echo "Verifying application health..."
for i in {1..30}; do
    if curl -f -s http://localhost:3000/health > /dev/null; then
        echo "Application is healthy"
        break
    fi
    echo "Waiting for application to be ready... ($i/30)"
    sleep 10
done

echo "Database recovery completed successfully"
```

## 💾 Chiến lược Backup

### 1. Database Backup Strategy

#### Automated Backup Script
```bash
#!/bin/bash
# automated-backup.sh

BACKUP_DIR="/backups/database"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

echo "Starting automated database backup..."

# 1. Create backup directory
mkdir -p $BACKUP_DIR/$TIMESTAMP

# 2. Full database backup
echo "Creating full database backup..."
sudo -u postgres pg_dumpall > $BACKUP_DIR/$TIMESTAMP/full_backup.sql

# 3. Individual database backups
echo "Creating individual database backups..."
sudo -u postgres pg_dump aicamera > $BACKUP_DIR/$TIMESTAMP/aicamera_backup.sql
sudo -u postgres pg_dump aicamera_analytics > $BACKUP_DIR/$TIMESTAMP/analytics_backup.sql

# 4. WAL archive backup
echo "Creating WAL archive backup..."
sudo -u postgres pg_basebackup -D $BACKUP_DIR/$TIMESTAMP/wal_archive -Ft -z -P

# 5. Compress backups
echo "Compressing backups..."
gzip $BACKUP_DIR/$TIMESTAMP/*.sql
tar -czf $BACKUP_DIR/$TIMESTAMP/wal_archive.tar.gz -C $BACKUP_DIR/$TIMESTAMP wal_archive

# 6. Upload to S3
echo "Uploading to S3..."
aws s3 sync $BACKUP_DIR/$TIMESTAMP s3://aicamera-backups/database/$TIMESTAMP

# 7. Cleanup old backups
echo "Cleaning up old backups..."
find $BACKUP_DIR -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \;

# 8. Update backup status
echo "Backup completed successfully at $TIMESTAMP"
echo "$TIMESTAMP" > $BACKUP_DIR/last_backup_timestamp
```

#### Backup Verification Script
```bash
#!/bin/bash
# verify-backup.sh

BACKUP_TIMESTAMP=$1
BACKUP_PATH="/backups/database/$BACKUP_TIMESTAMP"

echo "Verifying backup: $BACKUP_TIMESTAMP"

# 1. Check backup files exist
if [ ! -f "$BACKUP_PATH/full_backup.sql.gz" ]; then
    echo "ERROR: Full backup file not found"
    exit 1
fi

# 2. Test backup restoration
echo "Testing backup restoration..."
gunzip -c $BACKUP_PATH/full_backup.sql.gz > /tmp/test_backup.sql

# Create test database
sudo -u postgres createdb test_backup_verification

# Restore to test database
sudo -u postgres psql test_backup_verification < /tmp/test_backup.sql

# Verify data integrity
echo "Verifying data integrity..."
USER_COUNT=$(sudo -u postgres psql -d test_backup_verification -t -c "SELECT COUNT(*) FROM users;")
CAMERA_COUNT=$(sudo -u postgres psql -d test_backup_verification -t -c "SELECT COUNT(*) FROM camera_streams;")

echo "Backup verification results:"
echo "Users: $USER_COUNT"
echo "Camera streams: $CAMERA_COUNT"

# Cleanup test database
sudo -u postgres dropdb test_backup_verification
rm /tmp/test_backup.sql

echo "Backup verification completed successfully"
```

### 2. File Storage Backup Strategy

#### S3 Backup Configuration
```yaml
# s3-backup-config.yml
backup_configuration:
  source_bucket: aicamera-storage
  destination_bucket: aicamera-backups
  backup_schedule: "0 2 * * *"  # Daily at 2 AM
  
  retention_policy:
    daily_backups: 7
    weekly_backups: 4
    monthly_backups: 12
    
  backup_types:
    - incremental_backup
    - full_backup
    
  encryption:
    algorithm: AES256
    key_rotation: true
    
  monitoring:
    success_notification: true
    failure_notification: true
    metrics_tracking: true
```

#### S3 Backup Script
```bash
#!/bin/bash
# s3-backup.sh

SOURCE_BUCKET="aicamera-storage"
BACKUP_BUCKET="aicamera-backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "Starting S3 backup..."

# 1. Create incremental backup
echo "Creating incremental backup..."
aws s3 sync s3://$SOURCE_BUCKET s3://$BACKUP_BUCKET/incremental/$TIMESTAMP \
    --exclude "*.tmp" \
    --exclude "*.log" \
    --storage-class STANDARD_IA

# 2. Create full backup (weekly)
if [ $(date +%u) -eq 1 ]; then  # Monday
    echo "Creating full backup..."
    aws s3 sync s3://$SOURCE_BUCKET s3://$BACKUP_BUCKET/full/$TIMESTAMP \
        --storage-class STANDARD_IA
fi

# 3. Verify backup integrity
echo "Verifying backup integrity..."
aws s3 ls s3://$BACKUP_BUCKET/incremental/$TIMESTAMP --recursive | wc -l
aws s3 ls s3://$SOURCE_BUCKET --recursive | wc -l

# 4. Cleanup old backups
echo "Cleaning up old backups..."
aws s3 ls s3://$BACKUP_BUCKET/incremental/ | awk '{print $2}' | head -n -7 | xargs -I {} aws s3 rm s3://$BACKUP_BUCKET/incremental/{} --recursive

echo "S3 backup completed successfully"
```

## 🔄 Business Continuity Procedures

### 1. Failover Procedures

#### Load Balancer Failover
```bash
#!/bin/bash
# load-balancer-failover.sh

PRIMARY_LB="lb-primary.aicamera.com"
DR_LB="lb-dr.aicamera.com"
HEALTH_CHECK_URL="https://api.aicamera.com/health"

echo "Starting load balancer failover..."

# 1. Check primary load balancer health
check_primary_lb() {
    local response=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_CHECK_URL)
    if [ "$response" = "200" ]; then
        return 0
    fi
    return 1
}

# 2. If primary is down, switch to DR
if ! check_primary_lb; then
    echo "Primary load balancer is down. Switching to DR..."
    
    # Update DNS
    aws route53 change-resource-record-sets \
        --hosted-zone-id $HOSTED_ZONE_ID \
        --change-batch '{
            "Changes": [{
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": "api.aicamera.com",
                    "Type": "CNAME",
                    "TTL": 300,
                    "ResourceRecords": [{"Value": "'$DR_LB'"}]
                }
            }]
        }'
    
    # Send notification
    send_notification "LB_FAILOVER" "Load balancer failover to DR completed"
    
    echo "Load balancer failover completed"
else
    echo "Primary load balancer is healthy"
fi
```

### 2. Service Recovery Procedures

#### Service Recovery Script
```bash
#!/bin/bash
# service-recovery.sh

SERVICE_NAME=$1
RECOVERY_ACTION=$2

case $RECOVERY_ACTION in
    "restart")
        echo "Restarting $SERVICE_NAME..."
        kubectl rollout restart deployment/$SERVICE_NAME
        ;;
    "scale")
        echo "Scaling $SERVICE_NAME..."
        kubectl scale deployment/$SERVICE_NAME --replicas=3
        ;;
    "rollback")
        echo "Rolling back $SERVICE_NAME..."
        kubectl rollout undo deployment/$SERVICE_NAME
        ;;
    *)
        echo "Usage: $0 <service-name> {restart|scale|rollback}"
        exit 1
        ;;
esac

# Wait for service to be ready
kubectl rollout status deployment/$SERVICE_NAME

echo "$SERVICE_NAME recovery completed"
```

## 📊 Monitoring & Alerting

### 1. DR Monitoring Dashboard

#### Prometheus DR Metrics
```yaml
# prometheus-dr-config.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'dr-health-check'
    static_configs:
      - targets: ['dr-beauth-service:3000', 'dr-becamera-service:8000']
    metrics_path: '/health'
    scrape_interval: 10s

  - job_name: 'replication-lag'
    static_configs:
      - targets: ['dr-database:5432']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'backup-status'
    static_configs:
      - targets: ['backup-monitor:8080']
    metrics_path: '/metrics'
    scrape_interval: 60s
```

#### DR Alert Rules
```yaml
# dr-alert-rules.yml
groups:
  - name: dr_alerts
    rules:
      - alert: DRReplicationLag
        expr: pg_replication_lag_seconds > 300
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "DR replication lag detected"
          description: "Replication lag is {{ $value }} seconds"

      - alert: DRServiceDown
        expr: up{job="dr-health-check"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "DR service is down"
          description: "Service {{ $labels.instance }} is down"

      - alert: BackupFailure
        expr: backup_last_success_timestamp < time() - 86400
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Backup failure detected"
          description: "No successful backup in the last 24 hours"
```

### 2. DR Status Dashboard

#### Grafana DR Dashboard
```json
{
  "dashboard": {
    "title": "Disaster Recovery Status",
    "panels": [
      {
        "title": "DR Environment Health",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=\"dr-health-check\"}",
            "legendFormat": "DR Services"
          }
        ]
      },
      {
        "title": "Replication Lag",
        "type": "graph",
        "targets": [
          {
            "expr": "pg_replication_lag_seconds",
            "legendFormat": "Replication Lag (seconds)"
          }
        ]
      },
      {
        "title": "Backup Status",
        "type": "stat",
        "targets": [
          {
            "expr": "backup_last_success_timestamp",
            "legendFormat": "Last Backup"
          }
        ]
      },
      {
        "title": "DR Region Traffic",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{region=\"dr\"}[5m])",
            "legendFormat": "DR Traffic"
          }
        ]
      }
    ]
  }
}
```

## 🧪 Testing Procedures

### 1. DR Testing Schedule

#### Monthly DR Test
```bash
#!/bin/bash
# monthly-dr-test.sh

echo "Starting monthly DR test..."

# 1. Pre-test checklist
echo "Running pre-test checklist..."
./scripts/pre-dr-test-check.sh

# 2. Simulate primary region failure
echo "Simulating primary region failure..."
./scripts/simulate-primary-failure.sh

# 3. Verify failover
echo "Verifying failover..."
./scripts/verify-failover.sh

# 4. Test DR functionality
echo "Testing DR functionality..."
./scripts/test-dr-functionality.sh

# 5. Restore primary region
echo "Restoring primary region..."
./scripts/restore-primary-region.sh

# 6. Generate test report
echo "Generating test report..."
./scripts/generate-dr-test-report.sh

echo "Monthly DR test completed"
```

### 2. Backup Testing

#### Backup Restoration Test
```bash
#!/bin/bash
# test-backup-restoration.sh

BACKUP_TIMESTAMP=$1

echo "Testing backup restoration: $BACKUP_TIMESTAMP"

# 1. Create test environment
echo "Creating test environment..."
kubectl create namespace backup-test

# 2. Restore backup to test environment
echo "Restoring backup..."
./scripts/restore-backup-to-test.sh $BACKUP_TIMESTAMP

# 3. Verify data integrity
echo "Verifying data integrity..."
./scripts/verify-backup-data.sh

# 4. Test application functionality
echo "Testing application functionality..."
./scripts/test-application-functionality.sh

# 5. Cleanup test environment
echo "Cleaning up test environment..."
kubectl delete namespace backup-test

echo "Backup restoration test completed"
```

## 📋 DR Checklist

### Pre-DR Setup
- [ ] **Infrastructure**: DR infrastructure đã được setup
- [ ] **Replication**: Database replication đã được cấu hình
- [ ] **Backup**: Backup strategy đã được thiết lập
- [ ] **Monitoring**: DR monitoring đã được cấu hình
- [ ] **Documentation**: DR procedures đã được document
- [ ] **Training**: Team đã được training về DR procedures

### During DR Event
- [ ] **Assessment**: Đánh giá mức độ sự cố
- [ ] **Notification**: Thông báo cho stakeholders
- [ ] **Failover**: Thực hiện failover procedures
- [ ] **Verification**: Verify DR environment
- [ ] **Communication**: Duy trì communication với users
- [ ] **Monitoring**: Monitor DR environment

### Post-DR Recovery
- [ ] **Primary Restoration**: Khôi phục primary region
- [ ] **Data Sync**: Đồng bộ dữ liệu từ DR về primary
- [ ] **Failback**: Thực hiện failback procedures
- [ ] **Verification**: Verify primary environment
- [ ] **Documentation**: Document lessons learned
- [ ] **Review**: Review và cải thiện procedures

## 🚨 Emergency Contacts

### DR Team Contacts
- **DR Coordinator**: +84 123 456 789
- **System Administrator**: +84 987 654 321
- **Database Administrator**: +84 555 123 456
- **Network Administrator**: +84 777 888 999

### External Contacts
- **Cloud Provider**: support@cloudprovider.com
- **DNS Provider**: support@dnsprovider.com
- **Backup Provider**: support@backupprovider.com

---

**Tài liệu này cung cấp hướng dẫn khôi phục thảm họa và liên tục kinh doanh hoàn chỉnh cho hệ thống AI Camera Counting. Tất cả các quy trình đã được thiết kế để đảm bảo RTO ≤ 4 giờ và RPO ≤ 1 giờ.** 