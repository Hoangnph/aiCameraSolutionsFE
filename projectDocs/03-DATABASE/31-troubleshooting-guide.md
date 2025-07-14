# Troubleshooting Guide - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này cung cấp hướng dẫn troubleshooting cho AI Camera Counting System, bao gồm common database issues, performance troubleshooting, connection issues và data corruption recovery.

## 🎯 Troubleshooting Objectives

- **Quick Issue Resolution**: Giải quyết issues nhanh chóng
- **Root Cause Analysis**: Phân tích nguyên nhân gốc rễ
- **Prevention Strategies**: Chiến lược phòng ngừa issues
- **Recovery Procedures**: Quy trình khôi phục hệ thống
- **Performance Optimization**: Tối ưu hóa performance

## 🔍 Common Database Issues

### 1. Connection Issues

**Symptoms**:
- Database connection timeouts
- Connection pool exhaustion
- High connection wait times

**Diagnostic Queries**:
```sql
-- Check active connections
SELECT 
    COUNT(*) as total_connections,
    COUNT(*) FILTER (WHERE state = 'active') as active_connections,
    COUNT(*) FILTER (WHERE state = 'idle') as idle_connections
FROM pg_stat_activity;

-- Check connection limits
SELECT name, setting FROM pg_settings 
WHERE name IN ('max_connections', 'shared_preload_libraries');
```

**Solutions**:
```sql
-- Increase connection pool size
ALTER SYSTEM SET max_connections = 200;
SELECT pg_reload_conf();

-- Kill long-running queries
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'active'
  AND query_start < NOW() - INTERVAL '5 minutes';
```

### 2. Performance Issues

**Symptoms**:
- Slow query execution
- High CPU usage
- Memory pressure
- Disk I/O bottlenecks

**Diagnostic Queries**:
```sql
-- Find slow queries
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Check table bloat
SELECT schemaname, tablename, attname, n_distinct
FROM pg_stats
WHERE schemaname = 'public'
ORDER BY n_distinct DESC;
```

**Solutions**:
```sql
-- Create missing indexes
CREATE INDEX CONCURRENTLY idx_camera_configurations_status 
ON camera_configurations(camera_status);

-- Analyze tables for better statistics
ANALYZE camera_configurations;
ANALYZE detection_data;
```

### 3. Camera System Issues

**Symptoms**:
- Camera offline
- Poor stream quality
- Detection failures
- Processing delays

**Diagnostic Queries**:
```sql
-- Check camera health
SELECT camera_id, camera_status, last_heartbeat, error_count
FROM camera_health_monitoring
WHERE metric_timestamp > NOW() - INTERVAL '1 hour'
ORDER BY error_count DESC;

-- Check stream quality issues
SELECT camera_id, quality_score, latency_ms, error_count
FROM stream_quality_monitoring
WHERE quality_score < 0.7
  AND metric_timestamp > NOW() - INTERVAL '1 hour';
```

**Solutions**:
```sql
-- Reset camera status
UPDATE camera_configurations
SET camera_status = 'online',
    last_heartbeat = NOW()
WHERE camera_id = 'camera_001';

-- Clear error counts
UPDATE camera_health_monitoring
SET error_count = 0,
    last_error_message = NULL
WHERE camera_id = 'camera_001';
```

## 🔧 Performance Troubleshooting

### 1. Query Performance Analysis

**Step 1: Identify Slow Queries**
```sql
-- Find queries with high execution time
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements
WHERE mean_time > 100
ORDER BY mean_time DESC
LIMIT 20;
```

**Step 2: Analyze Query Plans**
```sql
-- Get execution plan for slow query
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM detection_data 
WHERE camera_id = 'camera_001' 
  AND detection_timestamp > NOW() - INTERVAL '1 day';
```

**Step 3: Optimize Queries**
```sql
-- Add composite indexes for common query patterns
CREATE INDEX CONCURRENTLY idx_detection_camera_timestamp_type
ON detection_data(camera_id, detection_timestamp, detection_type);

-- Partition large tables
CREATE TABLE detection_data_2024 PARTITION OF detection_data
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Update statistics
ANALYZE detection_data;
```

### 2. Memory and Cache Issues

**Diagnostic Queries**:
```sql
-- Check buffer cache hit ratio
SELECT SUM(heap_blks_hit) * 100.0 / (SUM(heap_blks_hit) + SUM(heap_blks_read)) AS buffer_hit_ratio
FROM pg_statio_user_tables;

-- Check shared buffer usage
SELECT name, setting, unit FROM pg_settings 
WHERE name IN ('shared_buffers', 'effective_cache_size', 'work_mem');
```

**Solutions**:
```sql
-- Increase shared buffers
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';

-- Increase work memory for complex queries
ALTER SYSTEM SET work_mem = '16MB';

-- Reload configuration
SELECT pg_reload_conf();
```

## 🔌 Connection Troubleshooting

### 1. Connection Pool Issues

**Diagnostic Queries**:
```sql
-- Check connection pool status
SELECT 
    COUNT(*) as total_connections,
    COUNT(*) FILTER (WHERE state = 'active') as active_connections,
    COUNT(*) FILTER (WHERE state = 'idle') as idle_connections
FROM pg_stat_activity;

-- Kill long-running connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'active'
  AND query_start < NOW() - INTERVAL '10 minutes';
```

**Solutions**:
```sql
-- Reset idle connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
  AND pid != pg_backend_pid();

-- Increase connection limits
ALTER SYSTEM SET max_connections = 200;
SELECT pg_reload_conf();
```

### 2. Network Connectivity Issues

**Diagnostic Steps**:
```bash
# Test database connectivity
psql -h localhost -p 5432 -U username -d database_name -c "SELECT 1;"

# Check network latency
ping database_host

# Test port connectivity
telnet database_host 5432

# Check SSL connectivity
openssl s_client -connect database_host:5432 -servername database_host
```

**Solutions**:
```sql
-- Check SSL configuration
SHOW ssl;
SHOW ssl_cert_file;
SHOW ssl_key_file;

-- Enable SSL if needed
ALTER SYSTEM SET ssl = on;
SELECT pg_reload_conf();

-- Check connection parameters
SHOW listen_addresses;
SHOW port;
SHOW max_connections;
```

## 🔄 Data Corruption Recovery

### 1. Data Integrity Checks

**Diagnostic Queries**:
```sql
-- Check for data corruption
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats
WHERE schemaname = 'public'
  AND n_distinct < 0;  -- Negative values indicate corruption

-- Check for orphaned records
SELECT COUNT(*) as orphaned_detections
FROM detection_data dd
LEFT JOIN camera_configurations cc ON dd.camera_id = cc.camera_id
WHERE cc.camera_id IS NULL;

-- Check for duplicate records
SELECT 
    camera_id,
    detection_timestamp,
    COUNT(*) as duplicate_count
FROM detection_data
GROUP BY camera_id, detection_timestamp
HAVING COUNT(*) > 1;
```

**Recovery Procedures**:
```sql
-- Remove orphaned records
DELETE FROM detection_data dd
WHERE NOT EXISTS (
    SELECT 1 FROM camera_configurations cc 
    WHERE cc.camera_id = dd.camera_id
);

-- Remove duplicate records (keep latest)
DELETE FROM detection_data dd1
USING detection_data dd2
WHERE dd1.id < dd2.id
  AND dd1.camera_id = dd2.camera_id
  AND dd1.detection_timestamp = dd2.detection_timestamp;

-- Rebuild corrupted indexes
REINDEX INDEX CONCURRENTLY idx_detection_data_camera_timestamp;
REINDEX INDEX CONCURRENTLY idx_camera_configurations_camera_id;
```

### 2. Backup and Recovery

**Backup Procedures**:
```bash
# Create full backup
pg_dump -h localhost -U username -d camera_system -f backup_$(date +%Y%m%d_%H%M%S).sql

# Create compressed backup
pg_dump -h localhost -U username -d camera_system | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Create incremental backup
pg_dump -h localhost -U username -d camera_system --data-only --table=detection_data > detection_data_backup.sql
```

**Recovery Procedures**:
```bash
# Restore from backup
psql -h localhost -U username -d camera_system < backup_20241201_120000.sql

# Restore specific table
psql -h localhost -U username -d camera_system -c "TRUNCATE detection_data;"
psql -h localhost -U username -d camera_system < detection_data_backup.sql
```

## 📊 Monitoring and Alerting

### 1. Health Check Queries

```sql
-- System health check
WITH health_checks AS (
    SELECT 
        'Connection Pool' as check_name,
        CASE 
            WHEN COUNT(*) < 100 THEN 'OK'
            WHEN COUNT(*) < 150 THEN 'WARNING'
            ELSE 'CRITICAL'
        END as status,
        COUNT(*) as value
    FROM pg_stat_activity
    
    UNION ALL
    
    SELECT 
        'Active Cameras' as check_name,
        CASE 
            WHEN COUNT(*) > 10 THEN 'OK'
            WHEN COUNT(*) > 5 THEN 'WARNING'
            ELSE 'CRITICAL'
        END as status,
        COUNT(*) as value
    FROM camera_health_monitoring
    WHERE camera_status = 'online'
      AND metric_timestamp > NOW() - INTERVAL '5 minutes'
)
SELECT 
    check_name,
    status,
    value,
    CASE status
        WHEN 'OK' THEN '🟢'
        WHEN 'WARNING' THEN '🟡'
        ELSE '🔴'
    END as status_icon
FROM health_checks
ORDER BY check_name;
```

### 2. Automated Recovery Procedures

```sql
-- Auto-recovery function for common issues
CREATE OR REPLACE FUNCTION auto_recovery_procedures()
RETURNS TABLE(
    procedure_name VARCHAR(200),
    action_taken TEXT,
    success BOOLEAN
) AS $$
DECLARE
    connection_count INTEGER;
    cache_hit_ratio DECIMAL(5,2);
    offline_cameras INTEGER;
BEGIN
    -- Check and fix connection pool issues
    SELECT COUNT(*) INTO connection_count
    FROM pg_stat_activity
    WHERE state = 'idle in transaction';
    
    IF connection_count > 10 THEN
        -- Kill idle in transaction connections
        PERFORM pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE state = 'idle in transaction'
          AND query_start < NOW() - INTERVAL '5 minutes';
        
        RETURN QUERY SELECT 
            'Connection Pool Cleanup'::VARCHAR(200),
            'Killed ' || connection_count || ' idle in transaction connections'::TEXT,
            TRUE;
    END IF;
    
    -- Check and fix cache issues
    SELECT ROUND((SUM(heap_blks_hit) * 100.0) / (SUM(heap_blks_hit) + SUM(heap_blks_read)), 2)
    INTO cache_hit_ratio
    FROM pg_statio_user_tables;
    
    IF cache_hit_ratio < 80 THEN
        -- Analyze tables to update statistics
        ANALYZE camera_configurations;
        ANALYZE detection_data;
        ANALYZE video_streams;
        
        RETURN QUERY SELECT 
            'Cache Optimization'::VARCHAR(200),
            'Updated table statistics to improve cache hit ratio'::TEXT,
            TRUE;
    END IF;
    
    -- Check and fix camera issues
    SELECT COUNT(*) INTO offline_cameras
    FROM camera_health_monitoring
    WHERE camera_status = 'offline'
      AND last_heartbeat < NOW() - INTERVAL '10 minutes';
    
    IF offline_cameras > 0 THEN
        -- Reset camera status for cameras offline too long
        UPDATE camera_configurations
        SET camera_status = 'maintenance'
        WHERE camera_id IN (
            SELECT camera_id 
            FROM camera_health_monitoring 
            WHERE camera_status = 'offline'
              AND last_heartbeat < NOW() - INTERVAL '10 minutes'
        );
        
        RETURN QUERY SELECT 
            'Camera Status Reset'::VARCHAR(200),
            'Reset status for ' || offline_cameras || ' offline cameras'::TEXT,
            TRUE;
    END IF;
    
    -- Return success if no issues found
    IF connection_count <= 10 AND cache_hit_ratio >= 80 AND offline_cameras = 0 THEN
        RETURN QUERY SELECT 
            'System Health Check'::VARCHAR(200),
            'All systems operating normally'::TEXT,
            TRUE;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

---

**Tài liệu này cung cấp comprehensive troubleshooting guide cho AI Camera Counting System với diagnostic queries, recovery procedures và automated monitoring capabilities.** 