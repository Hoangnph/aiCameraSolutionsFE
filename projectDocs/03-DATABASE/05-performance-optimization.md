# Performance Optimization Guide - AI Camera Counting System

## 📊 Tổng quan

Tài liệu này cung cấp hướng dẫn chi tiết về tối ưu hóa hiệu năng database cho hệ thống AI Camera Counting, bao gồm các chiến lược indexing, query optimization, partitioning, và monitoring với focus đặc biệt vào camera-specific use cases.

## 🎯 Mục tiêu hiệu năng

- **Response Time**: < 100ms cho real-time queries
- **Throughput**: > 1000 queries/second
- **Concurrent Users**: > 1000 users đồng thời
- **Data Volume**: > 1TB data với growth 100GB/month
- **Uptime**: 99.9% availability
- **Camera-specific**: < 50ms cho real-time counting queries
- **Stream Processing**: < 200ms cho video stream data ingestion
- **AI Model Integration**: < 100ms cho inference result storage

## 🏗️ Performance Architecture

### Database Performance Layers

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PERFORMANCE ARCHITECTURE                           │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              APPLICATION LAYER                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Query     │  │   Connection│  │   Caching   │  │   Monitoring│        │ │
│  │  │   Optimization│  │   Pooling   │  │   Layer     │  │   & Alerting│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              DATABASE LAYER                                 │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┘        │ │
│  │  │   Indexing  │  │   Partitioning│  │   Query     │  │   Resource  │        │ │
│  │  │   Strategy  │  │   Strategy   │  │   Planning  │  │   Management│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              INFRASTRUCTURE LAYER                           │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │   Hardware  │  │   Storage   │  │   Network   │  │   Monitoring│        │ │
│  │  │   Resources │  │   Optimization│  │   Optimization│  │   & Alerting│        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📹 Camera-Specific Performance Optimizations

### 1. Camera Data Query Optimization

**Mục đích**: Tối ưu hóa queries cho camera management và real-time data access.

```sql
-- Camera Configuration Optimization
CREATE INDEX idx_camera_configurations_active_tenant 
ON camera_configurations(is_active, tenant_id) WHERE is_active = TRUE;

CREATE INDEX idx_camera_configurations_location_type 
ON camera_configurations(location_id, camera_type);

-- Camera Health Monitoring Optimization
CREATE INDEX idx_camera_health_status_timestamp 
ON camera_health(status, last_heartbeat) WHERE status != 'online';

CREATE INDEX idx_camera_health_quality_score 
ON camera_health(stream_quality_score) WHERE stream_quality_score < 0.8;

-- Real-time Camera Data Access
CREATE INDEX idx_video_streams_camera_active 
ON video_streams(camera_id, is_active, last_frame_timestamp) 
WHERE is_active = TRUE;

CREATE INDEX idx_frame_queue_processing_priority 
ON frame_queue(processing_status, processing_priority DESC, frame_timestamp)
WHERE processing_status = 'pending';
```

### 2. Video Stream Data Indexing

**Mục đích**: Tối ưu hóa cho video stream processing và metadata access.

```sql
-- Stream Quality Metrics Optimization
CREATE INDEX idx_stream_quality_metrics_stream_timestamp 
ON stream_quality_metrics(stream_id, metric_timestamp DESC);

CREATE INDEX idx_stream_quality_metrics_quality_threshold 
ON stream_quality_metrics(stream_id, quality_score, metric_timestamp)
WHERE quality_score < 0.8;

-- Stream Events Optimization
CREATE INDEX idx_stream_events_stream_type_timestamp 
ON stream_events(stream_id, event_type, event_timestamp DESC);

CREATE INDEX idx_stream_events_unresolved 
ON stream_events(stream_id, is_resolved, event_timestamp)
WHERE is_resolved = FALSE;

-- Frame Processing Optimization
CREATE INDEX idx_frame_queue_stream_status_priority 
ON frame_queue(stream_id, processing_status, processing_priority DESC, frame_timestamp);

CREATE INDEX idx_frame_queue_batch_processing 
ON frame_queue(processing_status, frame_timestamp)
WHERE processing_status = 'pending'
  AND frame_timestamp > NOW() - INTERVAL '1 hour';
```

### 3. Real-time Counting Performance

**Mục đích**: Tối ưu hóa cho real-time people counting và analytics.

```sql
-- Detection Results Optimization
CREATE INDEX idx_person_detections_camera_timestamp 
ON person_detections(camera_id, frame_timestamp DESC);

CREATE INDEX idx_person_detections_confidence_threshold 
ON person_detections(camera_id, confidence_score, frame_timestamp)
WHERE confidence_score > 0.7;

-- Tracking Results Optimization
CREATE INDEX idx_person_tracking_track_id_timestamp 
ON person_tracking(track_id, frame_timestamp DESC);

CREATE INDEX idx_person_tracking_camera_status 
ON person_tracking(camera_id, tracking_status, frame_timestamp)
WHERE tracking_status = 'active';

-- Counting Events Optimization
CREATE INDEX idx_counting_events_camera_type_timestamp 
ON counting_events(camera_id, event_type, event_timestamp DESC);

CREATE INDEX idx_counting_events_realtime 
ON counting_events(camera_id, event_timestamp)
WHERE event_timestamp > NOW() - INTERVAL '1 hour';

-- Real-time Counting Results
CREATE INDEX idx_counting_results_camera_timestamp 
ON counting_results(camera_id, result_timestamp DESC);

CREATE INDEX idx_counting_results_current_counts 
ON counting_results(camera_id, current_count_in, current_count_out, result_timestamp)
WHERE result_timestamp > NOW() - INTERVAL '1 day';
```

### 4. Analytics Query Optimization

**Mục đích**: Tối ưu hóa cho analytics và reporting queries.

```sql
-- Real-time Analytics Optimization
CREATE INDEX idx_realtime_analytics_camera_timestamp 
ON realtime_analytics(camera_id, metric_timestamp DESC);

CREATE INDEX idx_realtime_analytics_trend_indicators 
ON realtime_analytics(camera_id, count_trend, density_trend, metric_timestamp)
WHERE metric_timestamp > NOW() - INTERVAL '1 hour';

-- Historical Analytics Optimization
CREATE INDEX idx_historical_analytics_camera_date 
ON historical_analytics(camera_id, data_date DESC);

CREATE INDEX idx_historical_analytics_period_type 
ON historical_analytics(camera_id, time_period, data_date DESC);

-- Time-series Data Optimization
CREATE INDEX idx_timeseries_data_camera_metric_timestamp 
ON timeseries_data(camera_id, metric_name, metric_timestamp DESC);

CREATE INDEX idx_timeseries_aggregations_camera_type_timestamp 
ON timeseries_aggregations(camera_id, aggregation_type, aggregation_timestamp DESC);
```

## 📋 Indexing Strategy

### 1. Primary Indexes

**Mục đích**: Tối ưu hóa queries trên primary keys và foreign keys.

```sql
-- Primary Key Indexes (Auto-created)
-- users(id)
-- cameras(id)
-- zones(id)
-- ai_models(id)
-- counting_results(id)
-- analytics(id)

-- Foreign Key Indexes
CREATE INDEX idx_cameras_ai_model_id ON cameras(ai_model_id);
CREATE INDEX idx_zones_camera_id ON zones(camera_id);
CREATE INDEX idx_counting_results_camera_id ON counting_results(camera_id);
CREATE INDEX idx_counting_results_zone_id ON counting_results(zone_id);
CREATE INDEX idx_analytics_camera_id ON analytics(camera_id);
CREATE INDEX idx_analytics_zone_id ON analytics(zone_id);
```

### 2. Composite Indexes

**Mục đích**: Tối ưu hóa queries với multiple conditions.

```sql
-- Time-based Composite Indexes
CREATE INDEX idx_counting_results_camera_timestamp 
ON counting_results(camera_id, timestamp DESC);

CREATE INDEX idx_counting_results_zone_timestamp 
ON counting_results(zone_id, timestamp DESC);

CREATE INDEX idx_analytics_camera_period 
ON analytics(camera_id, period_type, period_start DESC);

-- Status-based Composite Indexes
CREATE INDEX idx_cameras_status_active 
ON cameras(status, is_active) WHERE is_active = true;

CREATE INDEX idx_alerts_unresolved 
ON alerts(is_resolved, created_at) WHERE is_resolved = false;
```

### 3. Partial Indexes

**Mục đích**: Tối ưu hóa queries với specific conditions.

```sql
-- Active Cameras Only
CREATE INDEX idx_cameras_active_only 
ON cameras(id, name, status) WHERE is_active = true;

-- Recent Events Only
CREATE INDEX idx_camera_events_recent 
ON camera_events(camera_id, event_type, timestamp) 
WHERE timestamp >= NOW() - INTERVAL '7 days';

-- High Priority Alerts
CREATE INDEX idx_alerts_high_priority 
ON alerts(severity, created_at) 
WHERE severity IN ('high', 'critical');
```

### 4. Functional Indexes

**Mục đích**: Tối ưu hóa queries với functions và expressions.

```sql
-- Date-based Indexes
CREATE INDEX idx_counting_results_date 
ON counting_results(DATE(timestamp));

CREATE INDEX idx_analytics_period_date 
ON analytics(DATE(period_start));

-- Text Search Indexes
CREATE INDEX idx_cameras_name_lower 
ON cameras(LOWER(name));

CREATE INDEX idx_alerts_title_search 
ON alerts USING gin(to_tsvector('english', title));
```

## 🔄 Partitioning Strategy

### 1. Time-based Partitioning

**Mục đích**: Phân chia dữ liệu theo thời gian để tối ưu hóa queries và maintenance.

```sql
-- Counting Results Partitioning
CREATE TABLE counting_results (
    id SERIAL,
    camera_id INTEGER NOT NULL,
    zone_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    count_in INTEGER DEFAULT 0,
    count_out INTEGER DEFAULT 0,
    total_count INTEGER DEFAULT 0,
    confidence DECIMAL(5,4),
    frame_data JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (timestamp);

-- Monthly Partitions
CREATE TABLE counting_results_y2024m01 
PARTITION OF counting_results
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE counting_results_y2024m02 
PARTITION OF counting_results
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Auto-create Partitions Function
CREATE OR REPLACE FUNCTION create_monthly_partition(table_name text, start_date date)
RETURNS void AS $$
DECLARE
    partition_name text;
    end_date date;
BEGIN
    partition_name := table_name || '_y' || to_char(start_date, 'YYYY') || 'm' || to_char(start_date, 'MM');
    end_date := start_date + INTERVAL '1 month';
    
    EXECUTE format('CREATE TABLE IF NOT EXISTS %I PARTITION OF %I FOR VALUES FROM (%L) TO (%L)',
                   partition_name, table_name, start_date, end_date);
END;
$$ LANGUAGE plpgsql;
```

### 2. Camera-specific Partitioning

**Mục đích**: Phân chia dữ liệu theo camera để optimize cho multi-tenant environments.

```sql
-- Camera Events Partitioning by Camera ID
CREATE TABLE camera_events (
    id SERIAL,
    camera_id INTEGER NOT NULL,
    event_type event_type NOT NULL,
    severity event_severity DEFAULT 'info',
    message TEXT,
    data JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY HASH (camera_id);

-- Create hash partitions
CREATE TABLE camera_events_p0 PARTITION OF camera_events FOR VALUES WITH (modulus 4, remainder 0);
CREATE TABLE camera_events_p1 PARTITION OF camera_events FOR VALUES WITH (modulus 4, remainder 1);
CREATE TABLE camera_events_p2 PARTITION OF camera_events FOR VALUES WITH (modulus 4, remainder 2);
CREATE TABLE camera_events_p3 PARTITION OF camera_events FOR VALUES WITH (modulus 4, remainder 3);

-- Person Detections Partitioning
CREATE TABLE person_detections (
    id SERIAL,
    camera_id INTEGER NOT NULL,
    frame_timestamp TIMESTAMP NOT NULL,
    detection_id VARCHAR(100) UNIQUE NOT NULL,
    confidence_score DECIMAL(3,2) NOT NULL,
    bbox_x INTEGER NOT NULL,
    bbox_y INTEGER NOT NULL,
    bbox_width INTEGER NOT NULL,
    bbox_height INTEGER NOT NULL,
    object_attributes JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (frame_timestamp);

-- Daily partitions for recent data
CREATE TABLE person_detections_2024_01_15 
PARTITION OF person_detections
FOR VALUES FROM ('2024-01-15 00:00:00') TO ('2024-01-16 00:00:00');
```

## 🔍 Query Optimization

### 1. Camera Data Query Patterns

**Mục đích**: Tối ưu hóa queries cho camera management và monitoring.

```sql
-- Optimized Camera Status Query
-- Before optimization
SELECT c.*, ch.status, ch.last_heartbeat
FROM camera_configurations c
LEFT JOIN camera_health ch ON c.camera_id = ch.camera_id
WHERE c.tenant_id = $1 AND c.is_active = true;

-- After optimization (using covering index)
CREATE INDEX idx_camera_status_covering 
ON camera_configurations(tenant_id, is_active, camera_id, camera_name, camera_type, location_id)
WHERE is_active = true;

-- Optimized Real-time Counting Query
-- Before optimization
SELECT cr.*, c.camera_name, z.zone_name
FROM counting_results cr
JOIN camera_configurations c ON cr.camera_id = c.camera_id
JOIN counting_zones z ON cr.zone_id = z.id
WHERE cr.camera_id = $1 
  AND cr.result_timestamp > NOW() - INTERVAL '1 hour'
ORDER BY cr.result_timestamp DESC
LIMIT 100;

-- After optimization (using materialized view)
CREATE MATERIALIZED VIEW realtime_counting_summary AS
SELECT 
    cr.camera_id,
    c.camera_name,
    cr.zone_id,
    z.zone_name,
    cr.current_count_in,
    cr.current_count_out,
    cr.current_total,
    cr.result_timestamp
FROM counting_results cr
JOIN camera_configurations c ON cr.camera_id = c.camera_id
JOIN counting_zones z ON cr.zone_id = z.id
WHERE cr.result_timestamp > NOW() - INTERVAL '1 hour';

CREATE UNIQUE INDEX idx_realtime_counting_summary_camera_timestamp 
ON realtime_counting_summary(camera_id, result_timestamp DESC);

-- Refresh materialized view every 30 seconds
SELECT cron.schedule('refresh-counting-summary', '*/30 * * * * *', 
    'REFRESH MATERIALIZED VIEW CONCURRENTLY realtime_counting_summary;');
```

### 2. Stream Processing Query Optimization

**Mục đích**: Tối ưu hóa queries cho video stream processing.

```sql
-- Optimized Frame Queue Processing
-- Before optimization
SELECT fq.*, vs.stream_url
FROM frame_queue fq
JOIN video_streams vs ON fq.stream_id = vs.stream_id
WHERE fq.processing_status = 'pending'
  AND fq.processing_priority > 0
ORDER BY fq.processing_priority DESC, fq.frame_timestamp ASC
LIMIT 50;

-- After optimization (using covering index)
CREATE INDEX idx_frame_queue_processing_covering 
ON frame_queue(processing_status, processing_priority DESC, frame_timestamp, id, stream_id, frame_data)
WHERE processing_status = 'pending';

-- Optimized Stream Quality Monitoring
-- Before optimization
SELECT sqm.*, vs.camera_id
FROM stream_quality_metrics sqm
JOIN video_streams vs ON sqm.stream_id = vs.stream_id
WHERE sqm.metric_timestamp > NOW() - INTERVAL '1 hour'
  AND sqm.quality_score < 0.8
ORDER BY sqm.metric_timestamp DESC;

-- After optimization (using partial index)
CREATE INDEX idx_stream_quality_alerting 
ON stream_quality_metrics(stream_id, quality_score, metric_timestamp)
WHERE quality_score < 0.8;
```

### 3. Analytics Query Optimization

**Mục đích**: Tối ưu hóa queries cho analytics và reporting.

```sql
-- Optimized Historical Analytics Query
-- Before optimization
SELECT 
    camera_id,
    DATE(period_start) as date,
    SUM(total_count_in) as daily_in,
    SUM(total_count_out) as daily_out,
    AVG(avg_count) as avg_daily_count
FROM historical_analytics
WHERE camera_id = $1 
  AND period_start >= $2 
  AND period_start < $3
  AND time_period = 'day'
GROUP BY camera_id, DATE(period_start)
ORDER BY date;

-- After optimization (using pre-aggregated data)
CREATE MATERIALIZED VIEW daily_analytics_summary AS
SELECT 
    camera_id,
    DATE(period_start) as date,
    SUM(total_count_in) as daily_in,
    SUM(total_count_out) as daily_out,
    AVG(avg_count) as avg_daily_count,
    MAX(peak_count) as daily_peak
FROM historical_analytics
WHERE time_period = 'day'
GROUP BY camera_id, DATE(period_start);

CREATE INDEX idx_daily_analytics_summary_camera_date 
ON daily_analytics_summary(camera_id, date DESC);

-- Refresh daily at 2 AM
SELECT cron.schedule('refresh-daily-analytics', '0 2 * * *', 
    'REFRESH MATERIALIZED VIEW CONCURRENTLY daily_analytics_summary;');
```

## 🚀 Performance Monitoring

### 1. Camera-specific Performance Metrics

```sql
-- Camera Performance Monitoring Table
CREATE TABLE camera_performance_metrics (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(100) NOT NULL,
    metric_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Query Performance
    avg_query_time_ms INTEGER,
    max_query_time_ms INTEGER,
    query_count INTEGER,
    
    -- Data Processing Performance
    detection_processing_time_ms INTEGER,
    tracking_processing_time_ms INTEGER,
    counting_processing_time_ms INTEGER,
    
    -- Stream Performance
    stream_ingestion_rate_fps DECIMAL(8,2),
    stream_processing_latency_ms INTEGER,
    frame_drop_rate DECIMAL(5,2),
    
    -- Database Performance
    database_connection_count INTEGER,
    database_query_count INTEGER,
    database_cache_hit_ratio DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance Alerting Function
CREATE OR REPLACE FUNCTION check_camera_performance()
RETURNS TABLE(
    camera_id VARCHAR(100),
    alert_type VARCHAR(50),
    alert_message TEXT,
    alert_severity VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        cpm.camera_id,
        'high_query_time'::VARCHAR(50) as alert_type,
        'Average query time is above 100ms'::TEXT as alert_message,
        'warning'::VARCHAR(20) as alert_severity
    FROM camera_performance_metrics cpm
    WHERE cpm.metric_timestamp > NOW() - INTERVAL '5 minutes'
      AND cpm.avg_query_time_ms > 100
    
    UNION ALL
    
    SELECT 
        cpm.camera_id,
        'high_processing_latency'::VARCHAR(50),
        'Detection processing latency is above 200ms'::TEXT,
        'error'::VARCHAR(20)
    FROM camera_performance_metrics cpm
    WHERE cpm.metric_timestamp > NOW() - INTERVAL '5 minutes'
      AND cpm.detection_processing_time_ms > 200;
END;
$$ LANGUAGE plpgsql;
```

### 2. Real-time Performance Monitoring

```sql
-- Real-time Performance Dashboard Query
WITH camera_performance AS (
    SELECT 
        camera_id,
        AVG(avg_query_time_ms) as avg_query_time,
        AVG(detection_processing_time_ms) as avg_detection_time,
        AVG(stream_ingestion_rate_fps) as avg_ingestion_rate,
        COUNT(*) as metric_count
    FROM camera_performance_metrics
    WHERE metric_timestamp > NOW() - INTERVAL '1 hour'
    GROUP BY camera_id
)
SELECT 
    cp.camera_id,
    cc.camera_name,
    cp.avg_query_time,
    cp.avg_detection_time,
    cp.avg_ingestion_rate,
    CASE 
        WHEN cp.avg_query_time > 100 THEN 'critical'
        WHEN cp.avg_query_time > 50 THEN 'warning'
        ELSE 'normal'
    END as performance_status
FROM camera_performance cp
JOIN camera_configurations cc ON cp.camera_id = cc.camera_id
WHERE cc.is_active = true
ORDER BY cp.avg_query_time DESC;
```

## 📊 Performance Benchmarks

### 1. Camera Data Query Benchmarks

```sql
-- Benchmark Camera Status Query
EXPLAIN (ANALYZE, BUFFERS) 
SELECT c.*, ch.status, ch.last_heartbeat
FROM camera_configurations c
LEFT JOIN camera_health ch ON c.camera_id = ch.camera_id
WHERE c.tenant_id = 1 AND c.is_active = true;

-- Expected Results:
-- Planning Time: < 1ms
-- Execution Time: < 5ms
-- Buffers: < 10 shared hits

-- Benchmark Real-time Counting Query
EXPLAIN (ANALYZE, BUFFERS)
SELECT cr.*, c.camera_name
FROM counting_results cr
JOIN camera_configurations c ON cr.camera_id = c.camera_id
WHERE cr.camera_id = 'cam_001'
  AND cr.result_timestamp > NOW() - INTERVAL '1 hour'
ORDER BY cr.result_timestamp DESC
LIMIT 100;

-- Expected Results:
-- Planning Time: < 1ms
-- Execution Time: < 10ms
-- Buffers: < 20 shared hits
```

### 2. Stream Processing Benchmarks

```sql
-- Benchmark Frame Queue Processing
EXPLAIN (ANALYZE, BUFFERS)
SELECT fq.*
FROM frame_queue fq
WHERE fq.processing_status = 'pending'
  AND fq.processing_priority > 0
ORDER BY fq.processing_priority DESC, fq.frame_timestamp ASC
LIMIT 50;

-- Expected Results:
-- Planning Time: < 1ms
-- Execution Time: < 5ms
-- Buffers: < 15 shared hits

-- Benchmark Stream Quality Monitoring
EXPLAIN (ANALYZE, BUFFERS)
SELECT sqm.*
FROM stream_quality_metrics sqm
WHERE sqm.metric_timestamp > NOW() - INTERVAL '1 hour'
  AND sqm.quality_score < 0.8
ORDER BY sqm.metric_timestamp DESC;

-- Expected Results:
-- Planning Time: < 1ms
-- Execution Time: < 8ms
-- Buffers: < 25 shared hits
```

## 🔧 Performance Tuning

### 1. Database Configuration Tuning

```sql
-- PostgreSQL Configuration for Camera System
-- postgresql.conf optimizations

-- Memory Configuration
shared_buffers = 2GB                    -- 25% of RAM
effective_cache_size = 6GB              -- 75% of RAM
work_mem = 16MB                         -- For complex queries
maintenance_work_mem = 256MB            -- For maintenance operations

-- Connection Configuration
max_connections = 200                   -- Based on expected load
max_worker_processes = 8                -- For parallel queries
max_parallel_workers_per_gather = 4     -- Parallel query workers

-- Write-Ahead Logging
wal_buffers = 16MB                      -- WAL buffer size
checkpoint_completion_target = 0.9      -- Spread checkpoint writes
wal_writer_delay = 200ms                -- WAL writer frequency

-- Query Planning
random_page_cost = 1.1                  -- SSD optimization
effective_io_concurrency = 200          -- Parallel I/O operations
default_statistics_target = 100         -- Better query planning
```

### 2. Connection Pooling Configuration

```sql
-- PgBouncer Configuration for Camera System
-- pgbouncer.ini optimizations

[databases]
camera_system = host=localhost port=5432 dbname=camera_system

[pgbouncer]
listen_port = 6432
listen_addr = 0.0.0.0
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

-- Pool Configuration
pool_mode = transaction                 -- Transaction-level pooling
max_client_conn = 1000                 -- Maximum client connections
default_pool_size = 20                 -- Default pool size per database
max_db_connections = 50                -- Maximum connections per database
max_user_connections = 50              -- Maximum connections per user

-- Performance Settings
server_reset_query = DISCARD ALL       -- Reset server connections
server_check_query = SELECT 1          -- Health check query
server_check_delay = 30                -- Health check interval
```

## 📈 Performance Monitoring Dashboard

### 1. Real-time Performance Metrics

```sql
-- Performance Dashboard Query
WITH performance_summary AS (
    SELECT 
        'query_performance' as metric_type,
        AVG(avg_query_time_ms) as avg_value,
        MAX(max_query_time_ms) as max_value,
        COUNT(*) as sample_count
    FROM camera_performance_metrics
    WHERE metric_timestamp > NOW() - INTERVAL '1 hour'
    
    UNION ALL
    
    SELECT 
        'detection_performance' as metric_type,
        AVG(detection_processing_time_ms) as avg_value,
        MAX(detection_processing_time_ms) as max_value,
        COUNT(*) as sample_count
    FROM camera_performance_metrics
    WHERE metric_timestamp > NOW() - INTERVAL '1 hour'
    
    UNION ALL
    
    SELECT 
        'stream_performance' as metric_type,
        AVG(stream_ingestion_rate_fps) as avg_value,
        MAX(stream_ingestion_rate_fps) as max_value,
        COUNT(*) as sample_count
    FROM camera_performance_metrics
    WHERE metric_timestamp > NOW() - INTERVAL '1 hour'
)
SELECT 
    metric_type,
    ROUND(avg_value, 2) as average,
    ROUND(max_value, 2) as maximum,
    sample_count,
    CASE 
        WHEN metric_type = 'query_performance' AND avg_value > 100 THEN 'critical'
        WHEN metric_type = 'query_performance' AND avg_value > 50 THEN 'warning'
        WHEN metric_type = 'detection_performance' AND avg_value > 200 THEN 'critical'
        WHEN metric_type = 'detection_performance' AND avg_value > 100 THEN 'warning'
        WHEN metric_type = 'stream_performance' AND avg_value < 25 THEN 'critical'
        WHEN metric_type = 'stream_performance' AND avg_value < 30 THEN 'warning'
        ELSE 'normal'
    END as status
FROM performance_summary
ORDER BY metric_type;
```

---

**Tài liệu này cung cấp hướng dẫn tối ưu hóa hiệu năng hoàn chỉnh cho hệ thống AI Camera Counting, bao gồm camera-specific optimizations, query optimization, partitioning strategies, và performance monitoring với benchmarks cụ thể cho production deployment.** 